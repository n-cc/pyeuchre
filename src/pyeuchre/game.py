"""Classes facilitating the flow of the game of Euchre."""

from __future__ import annotations

from pyeuchre.cards import Card
from pyeuchre.cards import Deck


class Game:
    """Represents a game of Euchre."""

    def __init__(
        self,
        teams: tuple[Team, Team] | None = None,
        hand: Hand | None = None,
    ) -> None:
        """Initialize game.

        Args:
            teams (tuple): A tuple of two teams.
            hand: (Hand): A custom hand to start the game on.
        """
        if teams:
            self.teams = teams
        else:
            self.teams = (
                Team((Player("North"), Player("South"))),
                Team((Player("East"), Player("West"))),
            )

        self.hand = self.start_hand()

    def __str__(self) -> str:
        """Return Game as a printable string.

        TODO get much better printing here.
        """
        return self.teams

    def __repr__(self) -> str:
        """Return Game as a printable object string."""
        return f"{type(self).__name__}(name={self.teams})"

    def start_hand(self) -> Hand:
        """Begin a hand."""
        return Hand(self.teams)


class Hand:
    """Represents a hand."""

    def __init__(
        self,
        teams: tuple[Team, Team],
        tricks: tuple[int, int] | None = None,
        deck: Deck | None = None,
        shuffle_deck: bool = True,
    ) -> None:
        """Initialize hand.

        Args:
            teams (tuple): Tuple of two Teams participating in this hand.
            tricks (tuple): Number of taken tricks for each team for this hand.
            deck (Deck): Custom deck to use.
            shuffle_deck (bool): Whether to auto-shuffle the deck.
        """
        self.teams = teams
        self.lead: Card = None
        self.kitty = []

        if tricks:
            self.tricks = tricks
        else:
            self.tricks = [0, 0]

        if deck:
            self.deck = deck
        else:
            self.deck = Deck()

        if shuffle_deck:
            self.deck.shuffle()

        self.deal_trick()

    def __str__(self) -> str:
        """Return Trick as a printable string.

        TODO get much better printing here.
        """
        print([team.players for team in self.teams])
        return "Teams:{teams}\nTricks:{tricks}Lead:{lead}\nCards:{cards}".format(
            teams=self.teams,
            tricks=self.tricks,
            lead=self.lead,
            cards=[
                f"{player.name}: {[card for card in player.hand]}"
                for team in self.teams
                for player in team.players
            ],
        )

    def __repr__(self) -> str:
        """Return Hand as a printable string."""
        return f"{type(self).__name__}(lead={self.lead})"

    def deal_trick(self) -> None:
        """Deals a trick."""
        for team in self.teams:
            for player in team.players:
                player.hand = list(self.deck.deal(5))

        self.lead = list(self.deck.deal(1))
        self.kitty = list(self.deck.deal(3))


class Player:
    """Represents a player."""

    def __init__(self, name: str) -> None:
        """Initialize player.

        Args:
            name (str): Player's display name.
        """
        self.name = name
        self.hand = []

    def __str__(self) -> str:
        """Return Player as a printable string."""
        return self.name

    def __repr__(self) -> str:
        """Return Player as a printable string."""
        return f"{type(self).__name__}(name={self.name})"


class Team:
    """Represents a team."""

    def __init__(self, players: tuple[Player, Player], score: int = 0) -> None:
        """Initialize team.

        Args:
            players (tuple): Tuple of players for the team.
            score (int): Score for the team.
        """
        self.players = players
        self.score = score

    def __str__(self) -> str:
        """Return Team as a printable string."""
        return f"{self.players[0]} and {self.players[1]}: {self.score}"

    def __repr__(self) -> str:
        """Return Team as a printable object string."""
        return f"{type(self).__name__}(players={self.players})"
