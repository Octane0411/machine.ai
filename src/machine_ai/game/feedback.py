"""
Feedback generation system for the CS Player Guessing Game.

This module implements the core game mechanics for comparing guesses
against the target player and generating appropriate feedback across
all six dimensions.
"""

from typing import Dict
from .models import Player, DimensionFeedback, GuessFeedback, FeedbackType


class FeedbackGenerator:
    """Generates feedback by comparing guess and target players."""

    def __init__(self):
        """Initialize the feedback generator."""
        self.numeric_dimensions = {"age", "major_appearances"}
        self.categorical_dimensions = {"name", "team", "nationality", "role"}

    def generate_feedback(self, guess_player: Player, target_player: Player) -> GuessFeedback:
        """
        Generate complete feedback for a guess.

        Args:
            guess_player: The player that was guessed
            target_player: The target player to guess

        Returns:
            GuessFeedback containing dimension-wise comparison results
        """
        dimension_feedback = {}

        # Check all six dimensions
        for dimension in ["name", "team", "nationality", "age", "role", "major_appearances"]:
            feedback = self._compare_dimension(
                dimension,
                guess_player.get_dimension_value(dimension),
                target_player.get_dimension_value(dimension)
            )
            dimension_feedback[dimension] = feedback

        # Check if the guess is completely correct
        is_correct = all(
            feedback.feedback_type == FeedbackType.CORRECT
            for feedback in dimension_feedback.values()
        )

        return GuessFeedback(
            guess_player=guess_player,
            target_player=target_player,
            dimension_feedback=dimension_feedback,
            is_correct=is_correct
        )

    def _compare_dimension(self, dimension: str, guess_value, target_value) -> DimensionFeedback:
        """
        Compare a single dimension between guess and target.

        Args:
            dimension: Name of the dimension being compared
            guess_value: Value from the guessed player
            target_value: Value from the target player

        Returns:
            DimensionFeedback with appropriate feedback type
        """
        if guess_value == target_value:
            feedback_type = FeedbackType.CORRECT
        elif dimension in self.numeric_dimensions:
            # For numeric dimensions (age, major_appearances), provide directional feedback
            if guess_value < target_value:
                feedback_type = FeedbackType.HIGHER  # Target is higher
            else:
                feedback_type = FeedbackType.LOWER   # Target is lower
        else:
            # For categorical dimensions, just mark as wrong
            feedback_type = FeedbackType.WRONG

        return DimensionFeedback(
            dimension=dimension,
            guess_value=guess_value,
            target_value=target_value,
            feedback_type=feedback_type
        )

    def analyze_constraints(self, feedback_history: list[GuessFeedback]) -> Dict:
        """
        Analyze feedback history to determine constraints on the target player.

        Args:
            feedback_history: List of previous guess feedback

        Returns:
            Dictionary containing constraints for each dimension
        """
        constraints = {
            "name": {"excluded": set()},
            "team": {"excluded": set()},
            "nationality": {"excluded": set()},
            "age": {"min": 16, "max": 40, "excluded": set()},
            "role": {"excluded": set()},
            "major_appearances": {"min": 0, "max": 20, "excluded": set()}
        }

        for feedback in feedback_history:
            for dimension, dim_feedback in feedback.dimension_feedback.items():
                if dim_feedback.feedback_type == FeedbackType.CORRECT:
                    # If we have a correct match, this is the required value
                    constraints[dimension]["required"] = dim_feedback.target_value
                elif dim_feedback.feedback_type == FeedbackType.WRONG:
                    # Exclude this value
                    constraints[dimension]["excluded"].add(dim_feedback.guess_value)
                elif dim_feedback.feedback_type == FeedbackType.HIGHER:
                    # Target is higher than guess
                    if dimension == "age":
                        constraints["age"]["min"] = max(
                            constraints["age"]["min"],
                            dim_feedback.guess_value + 1
                        )
                    elif dimension == "major_appearances":
                        constraints["major_appearances"]["min"] = max(
                            constraints["major_appearances"]["min"],
                            dim_feedback.guess_value + 1
                        )
                elif dim_feedback.feedback_type == FeedbackType.LOWER:
                    # Target is lower than guess
                    if dimension == "age":
                        constraints["age"]["max"] = min(
                            constraints["age"]["max"],
                            dim_feedback.guess_value - 1
                        )
                    elif dimension == "major_appearances":
                        constraints["major_appearances"]["max"] = min(
                            constraints["major_appearances"]["max"],
                            dim_feedback.guess_value - 1
                        )

        return constraints

    def filter_candidates(self, players: list[Player], constraints: Dict) -> list[Player]:
        """
        Filter player list based on constraints from feedback history.

        Args:
            players: List of all possible players
            constraints: Constraints dictionary from analyze_constraints

        Returns:
            List of players that satisfy all constraints
        """
        valid_players = []

        for player in players:
            is_valid = True

            # Check each dimension constraint
            for dimension in ["name", "team", "nationality", "age", "role", "major_appearances"]:
                value = player.get_dimension_value(dimension)
                dim_constraints = constraints[dimension]

                # Check if required value is set
                if "required" in dim_constraints:
                    if value != dim_constraints["required"]:
                        is_valid = False
                        break

                # Check excluded values
                if value in dim_constraints["excluded"]:
                    is_valid = False
                    break

                # Check numeric ranges
                if dimension in ["age", "major_appearances"]:
                    if value < dim_constraints["min"] or value > dim_constraints["max"]:
                        is_valid = False
                        break

            if is_valid:
                valid_players.append(player)

        return valid_players