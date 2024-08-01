"""Classes and utilities pertaining to displaying information."""

from pyeuchre.cards import Card
from pyeuchre.game import Game


class Display:
    def __init__(self, game: Game, width: int = 80) -> None:
        self.width = width
        self.game = game

    def _print_center(self, s):
        for line in s.split("\n"):
            print(line.center(self.width))
        print()

    def print(
        self, score=False, dealer=False, lead=False, trump=False, cards=False, hands=False, tricks=False,
    ) -> None:
        print()

        if score:
            self._print_center(
                "\n".join(
                    [
                        f"{team}: {team.score}"
                        for team in self.game.players.teams
                    ]
                )
            )

        if dealer:
            print(f"Dealer: {self.game.players.dealer}")

        if lead:
            print(f"Lead: {self.game.hand.lead}\n")

        if tricks:
             print(
                "\n".join(
                    [
                        f"{team}: {team.tricks} tricks"
                        for team in self.game.players.teams
                    ]
                )
                + "\n"
            )

        if trump:
            print(f"Trump: {self.game.hand.trump_suit}\n")

        if hands:
            print(
                "\n".join(
                    [
                        "{name}: {cards}".format(
                            name=player.name,
                            cards=", ".join([str(card) for card in player.cards]),
                        )
                        for player in self.game.players
                    ]
                )
                + "\n"
            )

        if cards:
            print(" ".join(card) for card in self.game.hand.trick.cards)
