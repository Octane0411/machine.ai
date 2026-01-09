"""
Strategy implementations for CS Player Guessing Game agents.

This module contains various strategies that agents can use to make decisions,
including information theory approaches, heuristic methods, and constraint-based strategies.
"""

import math
import random
from typing import List, Dict, Any, Set
from collections import Counter

from .base import BaseStrategy, AgentDecision
from ..game import GameState, Player


class InformationTheoryStrategy(BaseStrategy):
    """Strategy based on information theory and entropy maximization."""

    def __init__(self, name: str = "Information-Theory"):
        super().__init__(name)

    def make_decision(self, game_state: GameState, possible_players: List[Player]) -> AgentDecision:
        """Choose the player that maximizes expected information gain."""
        if not possible_players:
            return self._make_fallback_decision()

        # Calculate information gain for each possible guess
        best_player = None
        best_score = -1

        for candidate in possible_players:
            score = self.calculate_score(candidate, game_state, possible_players)
            if score > best_score:
                best_score = score
                best_player = candidate

        confidence = min(0.9, 0.3 + best_score * 0.6)  # Scale score to confidence
        reasoning = self._explain_information_gain(best_player, best_score, possible_players)

        return AgentDecision(
            player_name=best_player.name,
            confidence=confidence,
            reasoning=reasoning,
            strategy_used=self.name,
            decision_time=0.0,
            metadata={
                "information_gain": best_score,
                "possible_players_count": len(possible_players)
            }
        )

    def calculate_score(self, player: Player, game_state: GameState, possible_players: List[Player]) -> float:
        """Calculate expected information gain for guessing this player."""
        total_entropy = 0.0
        dimensions = ["team", "nationality", "age", "role", "major_appearances"]

        for dimension in dimensions:
            entropy = self._calculate_dimension_entropy(player, possible_players, dimension)
            total_entropy += entropy

        # Normalize by number of dimensions
        return total_entropy / len(dimensions)

    def _calculate_dimension_entropy(self, candidate: Player, possible_players: List[Player], dimension: str) -> float:
        """Calculate entropy for a specific dimension."""
        candidate_value = candidate.get_dimension_value(dimension)

        if dimension in ["age", "major_appearances"]:
            return self._calculate_numeric_entropy(candidate_value, possible_players, dimension)
        else:
            return self._calculate_categorical_entropy(candidate_value, possible_players, dimension)

    def _calculate_categorical_entropy(self, candidate_value: Any, possible_players: List[Player], dimension: str) -> float:
        """Calculate entropy for categorical dimensions."""
        # Count how many players would be eliminated vs kept
        matches = sum(1 for p in possible_players if p.get_dimension_value(dimension) == candidate_value)
        non_matches = len(possible_players) - matches

        if matches == 0 or non_matches == 0:
            return 0.0  # No information gain

        # Calculate entropy: -p*log2(p) - (1-p)*log2(1-p)
        total = len(possible_players)
        p_match = matches / total
        p_non_match = non_matches / total

        entropy = 0.0
        if p_match > 0:
            entropy -= p_match * math.log2(p_match)
        if p_non_match > 0:
            entropy -= p_non_match * math.log2(p_non_match)

        return entropy

    def _calculate_numeric_entropy(self, candidate_value: int, possible_players: List[Player], dimension: str) -> float:
        """Calculate entropy for numeric dimensions (age, major_appearances)."""
        values = [p.get_dimension_value(dimension) for p in possible_players]

        # Count players in different ranges relative to candidate
        lower_count = sum(1 for v in values if v < candidate_value)
        equal_count = sum(1 for v in values if v == candidate_value)
        higher_count = sum(1 for v in values if v > candidate_value)

        total = len(values)
        if total == 0:
            return 0.0

        # Calculate entropy for three possible outcomes: lower, equal, higher
        entropy = 0.0
        for count in [lower_count, equal_count, higher_count]:
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)

        return entropy

    def _explain_information_gain(self, player: Player, score: float, possible_players: List[Player]) -> str:
        """Explain why this player was chosen based on information gain."""
        return (
            f"Selected {player.name} for maximum information gain (score: {score:.3f}). "
            f"This guess should efficiently narrow down from {len(possible_players)} possible players "
            f"by providing optimal feedback across multiple dimensions."
        )

    def _make_fallback_decision(self) -> AgentDecision:
        """Fallback when no possible players available."""
        return AgentDecision(
            player_name="unknown",
            confidence=0.0,
            reasoning="No possible players available for information gain calculation",
            strategy_used=self.name,
            decision_time=0.0,
            metadata={"fallback": True}
        )


class PopularPlayerStrategy(BaseStrategy):
    """Strategy that prioritizes well-known players with high major appearances."""

    def __init__(self, name: str = "Popular-Player"):
        super().__init__(name)

    def make_decision(self, game_state: GameState, possible_players: List[Player]) -> AgentDecision:
        """Choose the most popular/well-known player."""
        if not possible_players:
            return self._make_fallback_decision()

        # Sort by major appearances (descending) and age (for tie-breaking)
        best_player = max(possible_players,
                         key=lambda p: (p.major_appearances, -p.age))

        # Higher confidence for players with more major appearances
        confidence = min(0.9, 0.3 + (best_player.major_appearances / 20) * 0.6)

        reasoning = (
            f"Selected {best_player.name} as a well-known player with "
            f"{best_player.major_appearances} major appearances. "
            f"Popular players are statistically more likely to be chosen as targets."
        )

        return AgentDecision(
            player_name=best_player.name,
            confidence=confidence,
            reasoning=reasoning,
            strategy_used=self.name,
            decision_time=0.0,
            metadata={
                "major_appearances": best_player.major_appearances,
                "age": best_player.age
            }
        )

    def calculate_score(self, player: Player, game_state: GameState, possible_players: List[Player]) -> float:
        """Score based on major appearances and recognition."""
        # Base score from major appearances (0-1 range)
        major_score = min(1.0, player.major_appearances / 15)

        # Bonus for being in prime age range (22-28)
        age_bonus = 0.1 if 22 <= player.age <= 28 else 0.0

        return major_score + age_bonus

    def _make_fallback_decision(self) -> AgentDecision:
        """Fallback decision."""
        return AgentDecision(
            player_name="s1mple",  # Default to a well-known player
            confidence=0.3,
            reasoning="Fallback to well-known player s1mple",
            strategy_used=self.name,
            decision_time=0.0,
            metadata={"fallback": True}
        )


class ConstraintStrategy(BaseStrategy):
    """Strategy that focuses on satisfying constraints from previous feedback."""

    def __init__(self, name: str = "Constraint-Based"):
        super().__init__(name)

    def make_decision(self, game_state: GameState, possible_players: List[Player]) -> AgentDecision:
        """Choose a player that satisfies all constraints and has good characteristics."""
        if not possible_players:
            return self._make_fallback_decision()

        # If this is the first guess, use a different strategy
        if not game_state.feedback_history:
            # Start with a diverse player to maximize information
            best_player = self._choose_diverse_starter(possible_players)
            confidence = 0.6
            reasoning = f"Selected {best_player.name} as a diverse starting guess to gather maximum information."
        else:
            # Choose based on constraint satisfaction and likelihood
            best_player = max(possible_players,
                             key=lambda p: self.calculate_score(p, game_state, possible_players))

            confidence = min(0.9, 0.4 + (1.0 / len(possible_players)) * 0.5)
            reasoning = self._explain_constraint_reasoning(best_player, game_state, possible_players)

        return AgentDecision(
            player_name=best_player.name,
            confidence=confidence,
            reasoning=reasoning,
            strategy_used=self.name,
            decision_time=0.0,
            metadata={
                "constraints_applied": len(game_state.feedback_history),
                "remaining_candidates": len(possible_players)
            }
        )

    def calculate_score(self, player: Player, game_state: GameState, possible_players: List[Player]) -> float:
        """Score based on constraint satisfaction and player characteristics."""
        score = 0.5  # Base score

        # Bonus for major appearances (well-known players more likely)
        score += min(0.3, player.major_appearances / 15)

        # Bonus for being in common age range
        if 20 <= player.age <= 30:
            score += 0.1

        # Bonus for being from common regions
        common_nationalities = {"Denmark", "Sweden", "Ukraine", "Russia", "France", "Brazil"}
        if player.nationality in common_nationalities:
            score += 0.1

        return score

    def _choose_diverse_starter(self, possible_players: List[Player]) -> Player:
        """Choose a diverse starting player to maximize information gain."""
        # Prefer players with moderate characteristics that can provide good feedback
        candidates = []

        for player in possible_players:
            # Score based on diversity potential
            score = 0.0

            # Moderate major appearances (not too high or low)
            if 3 <= player.major_appearances <= 10:
                score += 0.3

            # Moderate age (not too young or old)
            if 23 <= player.age <= 27:
                score += 0.2

            # Common but not overwhelming nationality
            common_nations = {"Denmark", "Sweden", "France", "Ukraine"}
            if player.nationality in common_nations:
                score += 0.2

            # AWPer or Rifler (common roles)
            if player.role in ["AWPer", "Rifler"]:
                score += 0.1

            candidates.append((player, score))

        # Return the player with highest diversity score
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0] if candidates else possible_players[0]

    def _explain_constraint_reasoning(self, player: Player, game_state: GameState, possible_players: List[Player]) -> str:
        """Explain the constraint-based reasoning."""
        constraints_count = len(game_state.feedback_history)
        return (
            f"Selected {player.name} based on {constraints_count} constraint(s) from previous feedback. "
            f"This player satisfies all known requirements and has favorable characteristics "
            f"(age: {player.age}, majors: {player.major_appearances}) among {len(possible_players)} remaining candidates."
        )

    def _make_fallback_decision(self) -> AgentDecision:
        """Fallback decision."""
        return AgentDecision(
            player_name="unknown",
            confidence=0.0,
            reasoning="No players satisfy the current constraints",
            strategy_used=self.name,
            decision_time=0.0,
            metadata={"fallback": True}
        )


class RandomStrategy(BaseStrategy):
    """Random strategy for baseline comparison."""

    def __init__(self, name: str = "Random"):
        super().__init__(name)

    def make_decision(self, game_state: GameState, possible_players: List[Player]) -> AgentDecision:
        """Choose a random player from possible options."""
        if not possible_players:
            return self._make_fallback_decision()

        chosen_player = random.choice(possible_players)
        confidence = 1.0 / len(possible_players)  # Uniform probability

        return AgentDecision(
            player_name=chosen_player.name,
            confidence=confidence,
            reasoning=f"Randomly selected {chosen_player.name} from {len(possible_players)} possible players",
            strategy_used=self.name,
            decision_time=0.0,
            metadata={"possible_count": len(possible_players)}
        )

    def calculate_score(self, player: Player, game_state: GameState, possible_players: List[Player]) -> float:
        """All players have equal score in random strategy."""
        return 1.0

    def _make_fallback_decision(self) -> AgentDecision:
        """Fallback decision."""
        return AgentDecision(
            player_name="s1mple",
            confidence=0.1,
            reasoning="Random fallback to s1mple",
            strategy_used=self.name,
            decision_time=0.0,
            metadata={"fallback": True}
        )


def create_strategy(strategy_type: str, **kwargs) -> BaseStrategy:
    """
    Factory function to create strategy instances.

    Args:
        strategy_type: Type of strategy ("information", "popular", "constraint", "random")
        **kwargs: Additional arguments for the strategy

    Returns:
        Configured strategy instance
    """
    strategy_map = {
        "information": InformationTheoryStrategy,
        "popular": PopularPlayerStrategy,
        "constraint": ConstraintStrategy,
        "random": RandomStrategy
    }

    strategy_class = strategy_map.get(strategy_type.lower())
    if not strategy_class:
        raise ValueError(f"Unknown strategy type: {strategy_type}. Available: {list(strategy_map.keys())}")

    return strategy_class(**kwargs)