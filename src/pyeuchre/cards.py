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

    def __eq__(self, other: object) -> bool:
        """Is this rank the same as another rank."""
        if not isinstance(other, Rank):
            raise NotImplementedError

        return self.long == other.long

    def __str__(self) -> str:
        """Return rank as a string."""
        return self.short.title()

    def __repr__(self) -> str:
        """Return rank as a printable object string."""
        return f"{type(self).__name__}(short={self.short})"


class Suit:
    """Represents a suit."""

    def __init__(self, suit: tuple[str, str, str]) -> None:
        """Initialize suit.

        Args:
            suit (tuple): Short, "ascii", and long format of suit.
        """
        self.short = suit[0]
        self.ascii = suit[1]
        self.long = suit[2]

    def __eq__(self, other: object) -> bool:
        """Is this suit the same as another suit."""
        if not isinstance(other, Suit):
            raise NotImplementedError

        return self.long == other.long

    def __str__(self) -> str:
        """Return suit as a printable string."""
        return self.ascii

    def __repr__(self) -> str:
        """Return suit as a printable object string."""
        return f"{type(self).__name__}(short={self.short})"


SUITS = [
    Suit(suit)
    for suit in [
        ("h", "♥", "hearts"),
        ("d", "♦", "diamonds"),
        ("c", "♣", "clubs"),
        ("s", "♠", "spades"),
    ]
]

RANKS = [
    Rank(rank)
    for rank in [
        ("9", "nine"),
        ("10", "ten"),
        ("j", "jack"),
        ("q", "queen"),
        ("k", "king"),
        ("a", "ace"),
    ]
]


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

    def __eq__(self, other: object) -> bool:
        """Is this card the same as another card."""
        if not isinstance(other, Card):
            raise NotImplementedError

        return self.suit == other.suit and self.rank == other.rank

    def __str__(self) -> str:
        """Return card as a printable string."""
        return f"{self.rank}{self.suit}"

    def __repr__(self) -> str:
        """Return card as a printable object string."""
        return f"{type(self).__name__}(suit={self.suit}, rank={self.rank})"


class Deck:
    """Represents a deck of cards."""

    def __init__(self) -> None:
        """Initialize (build) a deck."""
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]

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
