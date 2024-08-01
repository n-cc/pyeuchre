"""pyeuchre command-line utility."""

from pyeuchre.game import Game
from pyeuchre.utility.display import Display


def main() -> None:
    """Main CLI entrypoint.

    Major revamp needed with click; cli is only used for testing classes currently.
    """
    game = Game()

    display = Display(game)

    while game.active:
        game.deal_hand()

        if game.hand:  # TODO fix mypy here
            display.print(score=True, tricks=False, lead=True, hands=True, dealer=True)
            game.hand.process_call_trump()

            while game.hand.active:
                game.hand.start_trick()
                display.print(tricks=True, hands=True, trump=True)
                game.hand.trick.play()
