"""pyeuchre command-line utility."""

from pyeuchre.game import Game


def main() -> None:
    """Main CLI entrypoint.

    Major revamp needed with click; cli is only used for testing classes currently.
    """
    game = Game()

    while game.active:
        game.deal_hand()

        if game.hand:  # TODO fix mypy here
            print(game.hand)
            game.hand.process_call_trump()

            if game.hand.trump_team:
                print(f"{game.hand.trump_team} call trump!")
                if game.hand.loner_player:
                    print(f"{game.hand.loner_player} goes alone!")
            
            game.hand.start_trick()
