# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CS (Counter-Strike) player guessing game AI agent project. The goal is to build a state-of-the-art AI that can efficiently guess professional CS players based on multi-dimensional feedback, similar to the game at https://blast.tv/counter-strikle/multiplayer.

## Game Domain Knowledge

### Game Mechanics
- **Input**: Player name guess
- **Feedback Dimensions**: Name, Team, Nationality, Age, Role, Major Appearances
- **Feedback Types**: Correct (✅), Wrong (❌), Higher (⬆️), Lower (⬇️)
- **Objective**: Guess the target player in minimum attempts

### CS Player Attributes
- **Roles**: IGL (In-Game Leader), AWPer (Sniper), Entry Fragger, Support, Lurker
- **Teams**: Professional CS teams (e.g., Astralis, NAVI, FaZe, etc.)
- **Major Tournaments**: Premier CS competitions (frequency varies by player career)
- **Age Range**: Typically 16-35 years for active professional players

## Project Architecture

### Planned Directory Structure
```
machine.ai/
├── data/                    # Player datasets and game data
│   ├── players/            # CS player database
│   ├── teams/              # Team information
│   └── tournaments/        # Tournament and major data
├── src/                     # Source code
│   ├── agents/             # AI agent implementations
│   ├── game/               # Game simulation engine
│   ├── models/             # ML model definitions
│   ├── data/               # Data processing utilities
│   └── utils/              # General utility functions
├── tests/                  # Test suites
├── docs/                   # Documentation
├── experiments/            # Training and evaluation scripts
└── configs/                # Configuration files
```

## Development Commands

### Environment Setup
```bash
# Install Python dependencies (when requirements.txt exists)
pip install -r requirements.txt

# Install development dependencies (when available)
pip install -r requirements-dev.txt
```

### Data Management
```bash
# Update player database (when implemented)
python src/data/update_players.py

# Validate data integrity (when implemented)
python src/data/validate.py
```

### Game Simulation
```bash
# Run game simulation (when implemented)
python src/game/simulator.py

# Test game mechanics (when implemented)
python -m pytest tests/test_game.py
```

### AI Agent Development
```bash
# Train AI agent (when implemented)
python experiments/train_agent.py

# Evaluate agent performance (when implemented)
python experiments/evaluate.py

# Run specific agent tests (when implemented)
python -m pytest tests/test_agents.py -v
```

### Testing
```bash
# Run all tests (when test suite exists)
python -m pytest

# Run tests with coverage (when configured)
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/test_specific.py -v
```

## Key Development Considerations

### Data Quality
- Ensure CS player data is current and accurate
- Handle edge cases (retired players, team transfers, name changes)
- Maintain consistency across different data sources

### Game Simulation Accuracy
- Replicate exact feedback logic from the original game
- Handle ambiguous cases (multiple players with same attributes)
- Ensure deterministic behavior for testing

### AI Agent Design
- Focus on optimal guessing strategies
- Consider both exploitation (use known information) and exploration (gather new information)
- Implement different difficulty levels and player pools

### Performance Optimization
- Efficient player database queries
- Fast game state evaluation
- Scalable training pipeline

## Testing Strategy

### Unit Tests
- Individual component functionality
- Data validation and processing
- Game rule implementation

### Integration Tests
- End-to-end game simulation
- AI agent interaction with game environment
- Data pipeline integrity

### Performance Tests
- Agent decision speed
- Database query performance
- Training efficiency

## Model Development

### Training Data
- Simulated game scenarios
- Human expert gameplay patterns
- Optimal solution paths

### Evaluation Metrics
- Average guesses to solution
- Success rate within N guesses
- Performance across player difficulty tiers

### Model Types to Consider
- Rule-based heuristics (baseline)
- Reinforcement learning agents
- Fine-tuned language models
- Ensemble approaches

## Domain-Specific Notes

### CS Esports Context
- Player careers are dynamic (transfers, retirements, comebacks)
- Major tournaments happen 2-4 times per year
- Team compositions change frequently
- Regional differences in player naming conventions

### Data Sources
- HLTV.org for comprehensive player statistics
- Liquipedia for tournament and team information
- Official tournament databases for major appearances
- Team websites for current rosters

### Common Pitfalls
- Outdated player information
- Ambiguous player names (handle duplicates)
- Regional vs international team names
- Inactive vs retired player status

## Project Management and Progress Tracking

### ROADMAP.md - Development Progress Tracking
**CRITICAL**: This project uses `ROADMAP.md` for comprehensive progress tracking and planning.

#### Usage Rules:
1. **Always check ROADMAP.md first** before starting any development work
2. **Update progress regularly** by checking off completed tasks ([ ] → [x])
3. **Update status indicators** for each phase:
   - ⏳ 待开始 (Not Started)
   - 🔄 进行中 (In Progress)
   - ✅ 已完成 (Completed)
4. **Add new tasks** if you discover additional work during implementation
5. **Update milestone table** when phases are completed
6. **Record significant decisions** in the update log section

#### Current Development Status:
- **Active Phase**: Phase 1 - Project Infrastructure (⏳ 待开始)
- **Next Milestone**: Runnable game engine + Ollama environment
- **Overall Progress**: 0/5 phases completed

#### Key Performance Targets:
- Phase 2: <6 average guesses (API baseline)
- Phase 3: <5 average guesses (optimized)
- Phase 4: 10%+ improvement (fine-tuned)
- Phase 5: <4 average guesses (SOTA target)

### Development Workflow:
1. Check current phase in ROADMAP.md
2. Review specific tasks and requirements
3. Implement according to technical specifications in claude_plan.md
4. Update progress in ROADMAP.md
5. Move to next task/phase when completed

## Current Status

**Project Stage**: Foundation Complete, Ready for Phase 1 Implementation
**Key Assets**:
- ✅ Player dataset (202+ players with 6 dimensions)
- ✅ Technical architecture planned (claude_plan.md)
- ✅ Development roadmap defined (ROADMAP.md)
- ✅ Documentation complete (README.md, CLAUDE.md)

**Next Action**: Begin Phase 1 - Project Infrastructure Setup