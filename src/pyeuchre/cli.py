"""pyeuchre command-line utility."""

from pyeuchre.game import Game


def main() -> None:
    """Main CLI entrypoint."""
    game = Game()
    print(game.hand)
