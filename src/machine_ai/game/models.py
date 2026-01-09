"""
Data models for the CS Player Guessing Game.

This module defines the core data structures used throughout the game,
including player information, game state, and feedback types.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple
import pandas as pd


class FeedbackType(Enum):
    """Types of feedback for each dimension."""
    CORRECT = "✅"      # Exact match
    WRONG = "❌"        # Different value
    HIGHER = "⬆️"       # Target value is higher
    LOWER = "⬇️"        # Target value is lower


@dataclass
class Player:
    """Represents a CS player with all required dimensions."""
    name: str
    team: str
    nationality: str
    age: int
    role: str
    major_appearances: int
    source_url: Optional[str] = None

    @classmethod
    def from_csv_row(cls, row: pd.Series) -> "Player":
        """Create a Player instance from a CSV row."""
        return cls(
            name=row["name"],
            team=row["team"],
            nationality=row["nationality"],
            age=int(row["age"]),
            role=row["role"],
            major_appearances=int(row["major_appearances"]),
            source_url=row.get("source_url")
        )

    def get_dimension_value(self, dimension: str):
        """Get the value for a specific dimension."""
        dimension_map = {
            "name": self.name,
            "team": self.team,
            "nationality": self.nationality,
            "age": self.age,
            "role": self.role,
            "major_appearances": self.major_appearances
        }
        return dimension_map.get(dimension)


@dataclass
class DimensionFeedback:
    """Feedback for a single dimension."""
    dimension: str
    guess_value: str | int
    target_value: str | int
    feedback_type: FeedbackType

    def __str__(self) -> str:
        return f"{self.dimension}: {self.guess_value} {self.feedback_type.value}"


@dataclass
class GuessFeedback:
    """Complete feedback for a guess across all dimensions."""
    guess_player: Player
    target_player: Player
    dimension_feedback: Dict[str, DimensionFeedback]
    is_correct: bool

    def __str__(self) -> str:
        feedback_lines = []
        for dim, feedback in self.dimension_feedback.items():
            feedback_lines.append(str(feedback))
        return f"Guess: {self.guess_player.name}\n" + "\n".join(feedback_lines)


@dataclass
class GameState:
    """Current state of the guessing game."""
    target_player: Player
    guesses: List[Player]
    feedback_history: List[GuessFeedback]
    max_guesses: int = 10
    is_won: bool = False
    is_over: bool = False

    @property
    def guess_count(self) -> int:
        """Number of guesses made so far."""
        return len(self.guesses)

    @property
    def remaining_guesses(self) -> int:
        """Number of guesses remaining."""
        return max(0, self.max_guesses - self.guess_count)

    def add_guess(self, player: Player, feedback: GuessFeedback) -> None:
        """Add a new guess and its feedback to the game state."""
        self.guesses.append(player)
        self.feedback_history.append(feedback)

        if feedback.is_correct:
            self.is_won = True
            self.is_over = True
        elif self.guess_count >= self.max_guesses:
            self.is_over = True


@dataclass
class GameResult:
    """Final result of a completed game."""
    target_player: Player
    guesses: List[Player]
    feedback_history: List[GuessFeedback]
    is_won: bool
    guess_count: int
    difficulty: str

    @property
    def success_rate(self) -> float:
        """Success rate (1.0 if won, 0.0 if lost)."""
        return 1.0 if self.is_won else 0.0

    @property
    def efficiency_score(self) -> float:
        """Efficiency score based on guess count (higher is better)."""
        if not self.is_won:
            return 0.0
        # Score from 0.1 to 1.0 based on guess count
        return max(0.1, 1.0 - (self.guess_count - 1) * 0.1)


class GameDifficulty(Enum):
    """Game difficulty levels based on player pool size."""
    EASY = "easy"      # Top 50 most famous players
    MEDIUM = "medium"  # Top 100 players
    HARD = "hard"      # Full dataset (200+ players)
    CUSTOM = "custom"  # Custom filtered player pool