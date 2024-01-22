"""pyeuchre command-line utility."""

from pyeuchre.game import Game


def main() -> None:
    """Main CLI entrypoint.

    Major revamp needed with click; cli is only used for testing classes currently.
    """
    game = Game()
    game.deal_hand()

    if game.hand:  # TODO fix mypy here
        while game.hand.active:
            print(game.hand)
            if game.hand.process_call_trump():
                print(f"{game.hand.trump_team} call trump!")
