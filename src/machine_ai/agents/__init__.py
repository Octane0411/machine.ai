"""
AI Agents for the CS Player Guessing Game.

This package contains various AI agents that can play the CS player guessing game,
including API-based agents, heuristic agents, and machine learning agents.
"""

from .base import BaseAgent, AgentDecision
from .api_agent import OllamaAgent
from .heuristic_agent import HeuristicAgent
from .strategy import (
    InformationTheoryStrategy,
    PopularPlayerStrategy,
    ConstraintStrategy
)

__all__ = [
    "BaseAgent",
    "AgentDecision",
    "OllamaAgent",
    "HeuristicAgent",
    "InformationTheoryStrategy",
    "PopularPlayerStrategy",
    "ConstraintStrategy"
]