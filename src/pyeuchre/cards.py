"""Classes and functions pertaining to cards."""

import random
import typing

from pyeuchre.exceptions import DeckExhaustedError


class Rank:
    """Represents a card's rank."""

    def __init__(self, rank: tuple[int, bool, str, str]) -> None:
        """Initialize rank.

        Args:
            rank (tuple): Weight, trumper status (ie jack), short and long format for rank.
        """
        self.weight = rank[0]
        self.trumper = rank[1]
        self.short = rank[2]
        self.long = rank[3]

    def __eq__(self, other: object) -> bool:
        """Is this rank the same as another rank."""
        if not isinstance(other, Rank):
            raise NotImplementedError

        return self.long == other.long

    def __gt__(self, other: object) -> bool:
        """Is this rank greater than another rank."""
        if not isinstance(other, Rank):
            raise NotImplementedError

        return self.weight > other.weight

    def __lt__(self, other: object) -> bool:
        """Is this rank less than another rank."""
        if not isinstance(other, Rank):
            raise NotImplementedError

        return self.weight < other.weight

    def __str__(self) -> str:
        """Return rank as a string."""
        return self.short.title()

    def __repr__(self) -> str:
        """Return rank as a printable object string."""
        return f"{type(self).__name__}(short={self.short})"


class Suit:
    """Represents a suit."""

    def __init__(self, suit: tuple[int, str, str, str]) -> None:
        """Initialize suit.

        Args:
            suit (tuple): Color (as an int), short, "ascii", and long format of suit.
        """
        self.color = suit[0]
        self.short = suit[1]
        self.ascii = suit[2]
        self.long = suit[3]

    def __eq__(self, other: object) -> bool:
        """Is this suit the same as another suit."""
        if not isinstance(other, Suit):
            raise NotImplementedError

        return self.long == other.long

    def is_same_color(self, other: object) -> bool:
        """Is this suit the same color as another suit."""
        if not isinstance(other, Suit):
            raise NotImplementedError

        return self.color == other.color

    def __str__(self) -> str:
        """Return suit as a printable string."""
        return self.ascii

    def __repr__(self) -> str:
        """Return suit as a printable object string."""
        return f"{type(self).__name__}(short={self.short})"


SUITS = [
    Suit(suit)
    for suit in [
        (0, "h", "♥", "hearts"),
        (0, "d", "♦", "diamonds"),
        (1, "c", "♣", "clubs"),
        (1, "s", "♠", "spades"),
    ]
]

RANKS = [
    Rank(rank)
    for rank in [
        (0, False, "9", "nine"),
        (1, False, "10", "ten"),
        (2, True, "j", "jack"),
        (3, False, "q", "queen"),
        (4, False, "k", "king"),
        (5, False, "a", "ace"),
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


def is_trump(card: Card, trump: Suit) -> bool:
    """Given a trump suit, determines if a card is a trump or not."""
    if card.suit == trump:
        return True
    if card.rank.trumper and card.suit.is_same_color(trump):
        return True
    return False
