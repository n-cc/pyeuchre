"""Classes pertaining to cards."""

import random

from exceptions import InvalidCardError


RANKS = {
    "8": "eight",
    "9": "nine",
    "10": "ten",
    "j": "jack",
    "q": "queen",
    "k": "king",
    "a": "ace",
}

SUITS = {"h": "hearts", "d": "diamonds", "c": "clubs", "s": "spades"}


class Rank:
    """Represents a card's rank."""

    def __init__(self, rank: str) -> None:
        """Initialize rank.

        Args:
            rank (str): Rank of the rank.
        """
        if rank not in RANKS.keys():
            raise InvalidCardError(f"invalid rank: {rank}")

        self.short = rank
        self.long = RANKS[rank]

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
            suit (str): Suit of the suit.
        """
        if suit not in SUITS.keys():
            raise InvalidCardError(f"invalid suit: {suit}")

        self.short = suit
        self.long = SUITS[suit]

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
        self.cards = [
            Card(Suit(suit), Rank(rank))
            for suit in SUITS.keys()
            for rank in RANKS.keys()
        ]

    def shuffle(self) -> None:
        """Shuffle the deck.

        TODO: Implement deck cutting.
        """
        random.shuffle(self.cards)

    def __str__(self) -> str:
        """Return deck as a printable string."""
        return f"{self.cards}"

    def __repr__(self) -> str:
        """Return card as a printable object string."""
        return f"{type(self).__name__}(cards={self.cards}"
