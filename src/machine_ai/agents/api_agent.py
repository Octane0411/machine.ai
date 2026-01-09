"""
API-based agents that use external language models for decision making.

This module implements agents that call external APIs (like Ollama, Groq, Together AI)
to make strategic decisions about which CS player to guess next.
"""

import json
import re
import requests
from typing import List, Dict, Any, Optional
import time

from .base import BaseAgent, AgentDecision
from ..game import GameState, Player


class OllamaAgent(BaseAgent):
    """Agent that uses Ollama local API for decision making."""

    def __init__(
        self,
        name: str = "Ollama-Llama3",
        model: str = "llama3:8b",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.1,
        max_tokens: int = 512
    ):
        """
        Initialize the Ollama agent.

        Args:
            name: Agent name
            model: Ollama model to use
            base_url: Ollama server URL
            temperature: Sampling temperature (0.0 = deterministic)
            max_tokens: Maximum response tokens
        """
        super().__init__(name)
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        self.max_tokens = max_tokens

    def make_decision(self, game_state: GameState, possible_players: List[Player]) -> AgentDecision:
        """Make a decision using Ollama API."""
        start_time = time.time()

        # Build the prompt
        prompt = self._build_strategic_prompt(game_state, possible_players)

        try:
            # Call Ollama API
            response = self._call_ollama(prompt)

            # Parse the response
            decision = self._parse_response(response, possible_players)
            decision.decision_time = time.time() - start_time

            self._record_decision(decision)
            return decision

        except Exception as e:
            # Fallback decision
            fallback_decision = self._make_fallback_decision(possible_players, str(e))
            fallback_decision.decision_time = time.time() - start_time
            self._record_decision(fallback_decision)
            return fallback_decision

    def _build_strategic_prompt(self, game_state: GameState, possible_players: List[Player]) -> str:
        """Build a strategic prompt for the language model."""
        prompt_parts = [
            "You are an expert CS:GO esports analyst playing a player guessing game.",
            "Your goal is to guess the target CS player in as few guesses as possible.",
            "",
            "GAME RULES:",
            "- You get feedback on 6 dimensions: name, team, nationality, age, role, major_appearances",
            "- Feedback types: ✅ (correct), ❌ (wrong), ⬆️ (target higher), ⬇️ (target lower)",
            "- Use information theory: choose guesses that maximize information gain",
            "",
            "CURRENT GAME STATE:",
            f"Target: Unknown player",
            f"Guesses made: {game_state.guess_count}/{game_state.max_guesses}",
            f"Remaining possible players: {len(possible_players)}",
            ""
        ]

        # Add feedback history
        if game_state.feedback_history:
            prompt_parts.append("PREVIOUS GUESSES AND FEEDBACK:")
            for i, feedback in enumerate(game_state.feedback_history, 1):
                prompt_parts.append(f"\nGuess {i}: {feedback.guess_player.name}")
                for dim, dim_feedback in feedback.dimension_feedback.items():
                    prompt_parts.append(f"  {dim}: {dim_feedback.guess_value} {dim_feedback.feedback_type.value}")

            prompt_parts.append("")

        # Add constraints analysis
        if game_state.feedback_history:
            prompt_parts.append("CONSTRAINTS FROM FEEDBACK:")
            # We could add constraint analysis here, but let's keep it simple for now
            prompt_parts.append("- Analyze the feedback above to understand what we know about the target")
            prompt_parts.append("")

        # Add possible players (limit to avoid token overflow)
        max_players_to_show = min(20, len(possible_players))
        prompt_parts.append(f"POSSIBLE PLAYERS ({len(possible_players)} total, showing top {max_players_to_show}):")

        for player in possible_players[:max_players_to_show]:
            prompt_parts.append(
                f"- {player.name}: {player.team}, {player.nationality}, {player.age}y, "
                f"{player.role}, {player.major_appearances} majors"
            )

        if len(possible_players) > max_players_to_show:
            prompt_parts.append(f"... and {len(possible_players) - max_players_to_show} more players")

        prompt_parts.extend([
            "",
            "STRATEGY:",
            "1. Analyze previous feedback to understand constraints",
            "2. Choose a player that maximizes information gain",
            "3. Consider both elimination potential and probability of being correct",
            "",
            "Respond with EXACTLY this format:",
            "PLAYER: [exact player name from the list]",
            "CONFIDENCE: [0.0-1.0]",
            "REASONING: [your strategic reasoning in 1-2 sentences]",
            "",
            "Choose your next guess:"
        ])

        return "\n".join(prompt_parts)

    def _call_ollama(self, prompt: str) -> str:
        """Call the Ollama API."""
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()
            return result.get("response", "")

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama API call failed: {e}")

    def _parse_response(self, response: str, possible_players: List[Player]) -> AgentDecision:
        """Parse the model's response into an AgentDecision."""
        # Extract player name
        player_match = re.search(r"PLAYER:\s*(.+)", response, re.IGNORECASE)
        if not player_match:
            raise ValueError("Could not extract player name from response")

        player_name = player_match.group(1).strip()

        # Extract confidence
        confidence_match = re.search(r"CONFIDENCE:\s*([\d.]+)", response, re.IGNORECASE)
        confidence = float(confidence_match.group(1)) if confidence_match else 0.5

        # Extract reasoning
        reasoning_match = re.search(r"REASONING:\s*(.+)", response, re.IGNORECASE | re.DOTALL)
        reasoning = reasoning_match.group(1).strip() if reasoning_match else "No reasoning provided"

        # Validate player name
        valid_names = [p.name for p in possible_players]
        if player_name not in valid_names:
            # Try to find a close match
            player_name = self._find_closest_player(player_name, valid_names)

        return AgentDecision(
            player_name=player_name,
            confidence=confidence,
            reasoning=reasoning,
            strategy_used="Ollama-LLM",
            decision_time=0.0,  # Will be set by caller
            metadata={
                "model": self.model,
                "temperature": self.temperature,
                "raw_response": response
            }
        )

    def _find_closest_player(self, target_name: str, valid_names: List[str]) -> str:
        """Find the closest matching player name."""
        target_lower = target_name.lower()

        # Try exact match (case insensitive)
        for name in valid_names:
            if name.lower() == target_lower:
                return name

        # Try substring match
        for name in valid_names:
            if target_lower in name.lower() or name.lower() in target_lower:
                return name

        # Default to first available player
        return valid_names[0] if valid_names else "unknown"

    def _make_fallback_decision(self, possible_players: List[Player], error: str) -> AgentDecision:
        """Make a fallback decision when API call fails."""
        # Simple fallback: choose a player with high major appearances (likely well-known)
        if possible_players:
            chosen_player = max(possible_players, key=lambda p: p.major_appearances)
            return AgentDecision(
                player_name=chosen_player.name,
                confidence=0.3,
                reasoning=f"Fallback decision due to API error: {error}. Chose player with most major appearances.",
                strategy_used="Fallback-Heuristic",
                decision_time=0.0,
                metadata={"error": error, "fallback": True}
            )
        else:
            return AgentDecision(
                player_name="unknown",
                confidence=0.0,
                reasoning=f"No possible players available. Error: {error}",
                strategy_used="Error-Fallback",
                decision_time=0.0,
                metadata={"error": error, "fallback": True}
            )

    def explain_strategy(self) -> str:
        """Explain the Ollama agent's strategy."""
        return (
            f"{self.name} uses the {self.model} language model to analyze game state "
            f"and make strategic decisions. It considers previous feedback, applies "
            f"information theory principles, and reasons about CS player characteristics "
            f"to maximize information gain with each guess."
        )


class GroqAgent(OllamaAgent):
    """Agent that uses Groq API for fast inference."""

    def __init__(
        self,
        name: str = "Groq-Llama3",
        model: str = "llama3-8b-8192",
        api_key: Optional[str] = None,
        temperature: float = 0.1
    ):
        super().__init__(name)
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.base_url = "https://api.groq.com/openai/v1"

    def _call_ollama(self, prompt: str) -> str:
        """Call Groq API instead of Ollama."""
        if not self.api_key:
            raise RuntimeError("Groq API key not provided")

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            result = response.json()
            return result["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Groq API call failed: {e}")


class TogetherAgent(OllamaAgent):
    """Agent that uses Together AI API."""

    def __init__(
        self,
        name: str = "Together-Llama3",
        model: str = "meta-llama/Llama-3-8b-chat-hf",
        api_key: Optional[str] = None,
        temperature: float = 0.1
    ):
        super().__init__(name)
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.base_url = "https://api.together.xyz/v1"

    def _call_ollama(self, prompt: str) -> str:
        """Call Together AI API instead of Ollama."""
        if not self.api_key:
            raise RuntimeError("Together AI API key not provided")

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            result = response.json()
            return result["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Together AI API call failed: {e}")


def create_api_agent(provider: str = "ollama", **kwargs) -> BaseAgent:
    """
    Factory function to create API agents.

    Args:
        provider: API provider ("ollama", "groq", "together")
        **kwargs: Additional arguments for the specific agent

    Returns:
        Configured API agent
    """
    if provider.lower() == "ollama":
        return OllamaAgent(**kwargs)
    elif provider.lower() == "groq":
        return GroqAgent(**kwargs)
    elif provider.lower() == "together":
        return TogetherAgent(**kwargs)
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'ollama', 'groq', or 'together'.")