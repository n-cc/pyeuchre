"""Classes facilitating the flow of the game of Euchre."""

from __future__ import annotations

from pyeuchre.cards import Card
from pyeuchre.cards import Deck
from pyeuchre.player import Human
from pyeuchre.player import Players
from pyeuchre.player import Team


class Game:
    """Represents a game of Euchre."""

    def __init__(
        self,
        players: Players | None = None,
        hand: Hand | None = None,
    ) -> None:
        """Initialize game.

        Args:
            players (Players): Players to start this game with.
            hand: (Hand): A custom hand to start the game on.
        """
        if players:
            self.players = players
        else:
            self.players = Players(
                (
                    Team(
                        (Human("North"), Human("South")),
                    ),
                    Team(
                        (Human("East"), Human("West")),
                    ),
                )
            )

        self.hand: Hand | None = hand if hand else None

    def __str__(self) -> str:
        """Return Game as a printable string.

        TODO get much better printing here.
        """
        return f"{self.players}"

    def __repr__(self) -> str:
        """Return Game as a printable object string."""
        return f"{type(self).__name__}(name={self.players})"

    def deal_hand(self) -> None:
        """Begin a hand."""
        self.hand = Hand(self.players)

    def shift_dealer(self) -> None:
        """Rotates dealers through the player list."""
        raise NotImplementedError


class Hand:
    """Represents a hand."""

    def __init__(
        self,
        players: Players,
        tricks: tuple[int, int] | None = None,
        deck: Deck | None = None,
        shuffle_deck: bool = True,
    ) -> None:
        """Initialize hand.

        Args:
            players (Players): Players for this hand.
            tricks (tuple): Number of taken tricks for each team for this hand.
            deck (Deck): Custom deck to use.
            shuffle_deck (bool): Whether to auto-shuffle the deck.
        """
        self.players = players
        self.lead: Card | None = None
        self.kitty: list[Card] = []

        if tricks:
            self.tricks = tricks
        else:
            self.tricks = (0, 0)

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
        return "Players: {players}\n\nTricks: {tricks}\n\nLead: {lead}\n\nCards: {cards}".format(
            players=self.players.teams,
            tricks=self.tricks,
            lead=self.lead,
            cards=[
                f"{player.name}: {[card for card in player.hand]}"
                for player in self.players.players
            ],
        )

    def __repr__(self) -> str:
        """Return Hand as a printable string."""
        return f"{type(self).__name__}(lead={self.lead})"

    def deal_trick(self) -> None:
        """Deals a trick."""
        for player in self.players.players:
            player.hand = list(self.deck.deal(5))

        self.lead = next(self.deck.deal(1))
        self.kitty = list(self.deck.deal(3))

    def decide_trump(self) -> None:
        """Initiates the trump deciding procedure."""
        raise NotImplementedError
