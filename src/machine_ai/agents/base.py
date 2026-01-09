"""
Base agent interface for CS Player Guessing Game AI agents.

This module defines the abstract base class that all AI agents must implement,
along with common data structures for agent decisions and reasoning.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import time

from ..game import GameState, Player


@dataclass
class AgentDecision:
    """Represents a decision made by an AI agent."""
    player_name: str
    confidence: float  # 0.0 to 1.0
    reasoning: str
    strategy_used: str
    decision_time: float  # seconds
    metadata: Dict[str, Any]

    @property
    def is_confident(self) -> bool:
        """Check if the agent is confident about this decision."""
        return self.confidence >= 0.7


@dataclass
class AgentPerformance:
    """Tracks performance metrics for an agent."""
    games_played: int = 0
    games_won: int = 0
    total_guesses: int = 0
    total_decision_time: float = 0.0
    best_game_guesses: Optional[int] = None
    worst_game_guesses: Optional[int] = None

    @property
    def win_rate(self) -> float:
        """Calculate win rate."""
        if self.games_played == 0:
            return 0.0
        return self.games_won / self.games_played

    @property
    def average_guesses(self) -> float:
        """Calculate average guesses per game."""
        if self.games_played == 0:
            return 0.0
        return self.total_guesses / self.games_played

    @property
    def average_decision_time(self) -> float:
        """Calculate average decision time."""
        if self.total_guesses == 0:
            return 0.0
        return self.total_decision_time / self.total_guesses

    def update_game_result(self, guesses: int, won: bool, decision_times: List[float]):
        """Update performance metrics with a game result."""
        self.games_played += 1
        if won:
            self.games_won += 1

        self.total_guesses += guesses
        self.total_decision_time += sum(decision_times)

        if self.best_game_guesses is None or guesses < self.best_game_guesses:
            self.best_game_guesses = guesses

        if self.worst_game_guesses is None or guesses > self.worst_game_guesses:
            self.worst_game_guesses = guesses


class BaseAgent(ABC):
    """Abstract base class for all AI agents."""

    def __init__(self, name: str):
        """
        Initialize the agent.

        Args:
            name: Human-readable name for the agent
        """
        self.name = name
        self.performance = AgentPerformance()
        self._decision_history: List[AgentDecision] = []

    @abstractmethod
    def make_decision(self, game_state: GameState, possible_players: List[Player]) -> AgentDecision:
        """
        Make a decision about which player to guess next.

        Args:
            game_state: Current state of the game
            possible_players: List of players that could still be the target

        Returns:
            AgentDecision containing the chosen player and reasoning
        """
        pass

    def get_decision_history(self) -> List[AgentDecision]:
        """Get the history of decisions made by this agent."""
        return self._decision_history.copy()

    def reset_decision_history(self):
        """Clear the decision history."""
        self._decision_history.clear()

    def _record_decision(self, decision: AgentDecision):
        """Record a decision in the agent's history."""
        self._decision_history.append(decision)

    def _time_decision(self, func, *args, **kwargs) -> tuple[Any, float]:
        """Time how long a decision function takes."""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, end_time - start_time

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of the agent's performance."""
        return {
            "name": self.name,
            "games_played": self.performance.games_played,
            "win_rate": self.performance.win_rate,
            "average_guesses": self.performance.average_guesses,
            "best_game": self.performance.best_game_guesses,
            "worst_game": self.performance.worst_game_guesses,
            "average_decision_time": self.performance.average_decision_time
        }

    def explain_strategy(self) -> str:
        """
        Provide a human-readable explanation of the agent's strategy.

        Returns:
            String describing how this agent makes decisions
        """
        return f"{self.name}: Strategy explanation not implemented."

    def __str__(self) -> str:
        return f"{self.name} (Win Rate: {self.performance.win_rate:.1%}, Games: {self.performance.games_played})"


class MultiStrategyAgent(BaseAgent):
    """Base class for agents that use multiple strategies."""

    def __init__(self, name: str):
        super().__init__(name)
        self.strategies: List['BaseStrategy'] = []
        self.strategy_weights: Dict[str, float] = {}

    def add_strategy(self, strategy: 'BaseStrategy', weight: float = 1.0):
        """Add a strategy to this agent."""
        self.strategies.append(strategy)
        self.strategy_weights[strategy.name] = weight

    def get_weighted_decisions(self, game_state: GameState, possible_players: List[Player]) -> List[tuple[AgentDecision, float]]:
        """Get decisions from all strategies with their weights."""
        weighted_decisions = []

        for strategy in self.strategies:
            decision = strategy.make_decision(game_state, possible_players)
            weight = self.strategy_weights.get(strategy.name, 1.0)
            weighted_decisions.append((decision, weight))

        return weighted_decisions


class BaseStrategy(ABC):
    """Abstract base class for individual strategies."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def make_decision(self, game_state: GameState, possible_players: List[Player]) -> AgentDecision:
        """Make a decision using this strategy."""
        pass

    @abstractmethod
    def calculate_score(self, player: Player, game_state: GameState, possible_players: List[Player]) -> float:
        """Calculate a score for how good a player choice would be."""
        pass

    def explain_reasoning(self, player: Player, game_state: GameState) -> str:
        """Explain why this strategy chose a particular player."""
        return f"{self.name} strategy selected {player.name}"