"""Classes pertaining to cards."""

import random
import typing

from pyeuchre.exceptions import DeckExhaustedError


class Rank:
    """Represents a card's rank."""

    def __init__(self, rank: tuple[str, str]) -> None:
        """Initialize rank.

        Args:
            rank (tuple): Short and long format of rank.
        """
        self.short = rank[0]
        self.long = rank[1]

    def __str__(self) -> str:
        """Return rank as a string."""
        return self.long.title()

    def __repr__(self) -> str:
        """Return rank as a printable object string."""
        return f"{type(self).__name__}(short={self.short})"


class Suit:
    """Represents a suit."""

    def __init__(self, suit: str) -> None:
        """Initialize suit.

        Args:
            suit (tuple): Short and long format of suit.
        """
        self.short = suit[0]
        self.long = suit[1]

    def __str__(self) -> str:
        """Return suit as a printable string."""
        return self.long.title()

    def __repr__(self) -> str:
        """Return suit as a printable object string."""
        return f"{type(self).__name__}(short={self.short})"


class Card:
    """Represents a card."""

    def __init__(self, suit: Suit, rank: Rank) -> None:
        """Initialize card.

        Args:
            suit (Suit): Suit of the card.
            rank (Rank): Rank of the card.
        """
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        """Return card as a printable string."""
        return f"{self.rank} of {self.suit}"

    def __repr__(self) -> str:
        """Return card as a printable object string."""
        return f"{type(self).__name__}(suit={self.suit}, rank={self.rank})"


class Deck:
    """Represents a deck of cards."""

    def __init__(self) -> None:
        """Initialize (build) a deck."""
        self._ranks = [
            Rank(rank)
            for rank in [
                ("8", "eight"),
                ("9", "nine"),
                ("10", "ten"),
                ("j", "jack"),
                ("q", "queen"),
                ("k", "king"),
                ("a", "ace"),
            ]
        ]

        self._suits = [
            Suit(suit)
            for suit in [
                ("h", "hearts"),
                ("d", "diamonds"),
                ("c", "clubs"),
                ("s", "spades"),
            ]
        ]

        self.cards = [Card(suit, rank) for suit in self._suits for rank in self._ranks]

    def shuffle(self) -> None:
        """Shuffle the deck.

        TODO: Implement deck cutting.
        """
        random.shuffle(self.cards)

    def deal(self, n: int = 1) -> typing.Generator[Card, None, None]:
        """Deal X number of cards, removing them from the deck.

        Args:
            n (int): Number of cards to deal from the deck.

        Returns:
            Generator of Cards.
        """
        if len(self.cards) < n:
            raise DeckExhaustedError

        for _i in range(n):
            yield self.cards.pop()

    def __str__(self) -> str:
        """Return deck as a printable string."""
        return f"{self.cards}"

    def __repr__(self) -> str:
        """Return card as a printable object string."""
        return f"{type(self).__name__}(cards={self.cards}"
