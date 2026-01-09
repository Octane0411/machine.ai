"""
Command Line Interface for the CS Player Guessing Game.

Provides interactive gameplay and testing functionality.
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

from .game import GameEngine, PlayerDatabase, GameDifficulty


console = Console()


@click.group()
def cli():
    """CS Player Guessing Game AI Agent."""
    pass


@cli.command()
@click.option(
    "--players-csv",
    default="players.csv",
    help="Path to the players CSV file",
    type=click.Path(exists=True)
)
@click.option(
    "--difficulty",
    default="medium",
    type=click.Choice(["easy", "medium", "hard"]),
    help="Game difficulty level"
)
@click.option(
    "--max-guesses",
    default=10,
    help="Maximum number of guesses allowed"
)
def play(players_csv: str, difficulty: str, max_guesses: int):
    """Play the CS player guessing game interactively."""
    console.print("[bold blue]🎮 CS Player Guessing Game[/bold blue]")
    console.print()

    # Initialize game components
    try:
        db = PlayerDatabase(players_csv)
        engine = GameEngine(db)
    except Exception as e:
        console.print(f"[red]Error initializing game: {e}[/red]")
        return

    # Convert difficulty string to enum
    difficulty_map = {
        "easy": GameDifficulty.EASY,
        "medium": GameDifficulty.MEDIUM,
        "hard": GameDifficulty.HARD
    }
    game_difficulty = difficulty_map[difficulty]

    # Create new game
    game_state = engine.create_new_game(
        difficulty=game_difficulty,
        max_guesses=max_guesses
    )

    console.print(f"[green]Game started![/green] Difficulty: {difficulty.title()}")
    console.print(f"[yellow]Target: Unknown Player[/yellow]")
    console.print(f"[cyan]Max guesses: {max_guesses}[/cyan]")
    console.print()

    # Game loop
    while not game_state.is_over:
        # Show current stats
        stats = engine.get_game_stats(game_state)
        console.print(f"[dim]Guesses: {stats['guesses_made']}/{max_guesses} | "
                     f"Possible players: {stats['possible_players_count']}[/dim]")

        # Get player guess
        guess = Prompt.ask("[bold]Enter player name")

        if guess.lower() in ['quit', 'exit', 'q']:
            console.print("[yellow]Game quit![/yellow]")
            break

        # Process guess
        success, message = engine.make_guess(game_state, guess)

        if not success:
            console.print(f"[red]{message}[/red]")
            continue

        # Show feedback
        latest_feedback = game_state.feedback_history[-1]
        display_feedback(latest_feedback)

        console.print(f"[dim]{message}[/dim]")
        console.print()

    # Game over
    if game_state.is_won:
        console.print("[bold green]🎉 Congratulations! You won![/bold green]")
    elif game_state.is_over:
        console.print(f"[bold red]💀 Game Over! The answer was: {game_state.target_player.name}[/bold red]")

    # Show final stats
    result = engine.get_game_result(game_state, difficulty)
    show_game_result(result)


@cli.command()
@click.option(
    "--players-csv",
    default="players.csv",
    help="Path to the players CSV file",
    type=click.Path(exists=True)
)
@click.option("--player-name", help="Specific player name to search for")
def info(players_csv: str, player_name: str):
    """Show information about players in the database."""
    try:
        db = PlayerDatabase(players_csv)
    except Exception as e:
        console.print(f"[red]Error loading database: {e}[/red]")
        return

    if player_name:
        # Show specific player info
        player = db.get_player_by_name(player_name)
        if player:
            show_player_info(player)
        else:
            console.print(f"[red]Player '{player_name}' not found.[/red]")
            # Show similar players
            similar = db.search_players(player_name, limit=5)
            if similar:
                console.print("[yellow]Similar players:[/yellow]")
                for p in similar:
                    console.print(f"  - {p.name}")
    else:
        # Show database stats
        console.print(f"[bold blue]Player Database Statistics[/bold blue]")
        console.print(f"Total players: {len(db.players)}")

        # Show difficulty breakdowns
        for diff in [GameDifficulty.EASY, GameDifficulty.MEDIUM, GameDifficulty.HARD]:
            players = db.get_players_by_difficulty(diff)
            console.print(f"{diff.value.title()}: {len(players)} players")


def display_feedback(feedback):
    """Display guess feedback in a formatted table."""
    table = Table(title=f"Feedback for: {feedback.guess_player.name}")

    table.add_column("Dimension", style="cyan")
    table.add_column("Your Guess", style="yellow")
    table.add_column("Feedback", style="green")

    for dimension, dim_feedback in feedback.dimension_feedback.items():
        table.add_row(
            dimension.replace("_", " ").title(),
            str(dim_feedback.guess_value),
            dim_feedback.feedback_type.value
        )

    console.print(table)


def show_player_info(player):
    """Display detailed information about a player."""
    info_panel = Panel.fit(
        f"[bold]{player.name}[/bold]\n"
        f"Team: {player.team}\n"
        f"Nationality: {player.nationality}\n"
        f"Age: {player.age}\n"
        f"Role: {player.role}\n"
        f"Major Appearances: {player.major_appearances}",
        title="Player Information",
        border_style="blue"
    )
    console.print(info_panel)


def show_game_result(result):
    """Display final game result statistics."""
    console.print()
    console.print("[bold blue]📊 Game Statistics[/bold blue]")
    console.print(f"Target Player: {result.target_player.name}")
    console.print(f"Guesses Made: {result.guess_count}")
    console.print(f"Result: {'Won' if result.is_won else 'Lost'}")
    console.print(f"Efficiency Score: {result.efficiency_score:.2f}")


def main():
    """Main CLI entry point."""
    cli()