"""
CS Player Guessing Game AI Agent.

A state-of-the-art AI agent for the CS player guessing game,
featuring strategic reasoning and self-improvement capabilities.
"""

__version__ = "0.1.0"

from .game import GameEngine, PlayerDatabase, GameDifficulty

__all__ = ["GameEngine", "PlayerDatabase", "GameDifficulty"]


def main():
    """Main entry point for the CLI application."""
    from .cli import main as cli_main
    cli_main()
