"""Classes pertaining to players."""

import typing

from pyeuchre.cards import Card
from pyeuchre.utility.input import parse_bool


# only import Hand for typing purposes within the Player class - avoid circular imports
if typing.TYPE_CHECKING:
    from pyeuchre.game import Hand


class Player:
    """Represents a player."""

    def __init__(self, name: str) -> None:
        """Initialize player.

        Args:
            name (str): Player's display name.
        """
        self.name = name
        self.cards: list[Card] = []
        self.skip = False

    def __str__(self) -> str:
        """Return Player as a printable string."""
        return self.name

    def __repr__(self) -> str:
        """Return Player as a printable string."""
        return f"{type(self).__name__}(name={self.name})"

    def request_loner(self, hand: "Hand") -> bool:  # noqa: N803
        """Request a player to decide if they want go alone."""
        raise NotImplementedError

    def request_trump_call(self, hand: "Hand") -> bool:  # noqa: N803
        """Request a player to decide if they want to call a face up trump value."""
        raise NotImplementedError

    def request_trump_choose(self, hand: "Hand") -> bool:  # noqa: N803
        """Request a player to decide if they want to choose a trump."""
        raise NotImplementedError

    def request_card(self, hand: "Hand") -> Card:
        """Request a player to play a card.

        Args:
            hand (Hand): Hand object that the player can use for context when making a decision.
        """
        raise NotImplementedError


class Human(Player):
    """Represents a human player."""

    def request_card(self, hand: "Hand") -> Card:
        """Request a human player to play a card.

        Args:
            hand (Hand): Hand object that the player can use for context when making a decision.
        """
        # TODO flesh this out more - add a new utility/input function to parse input into a card
        card = input("Card number?")
        return self.cards[card]  # type: ignore [no-any-return,call-overload]

    def request_loner(self, hand: "Hand") -> bool:  # noqa: N803
        """Request a player to decide if they want go alone."""
        return parse_bool(input(f"{self.name}: go alone (y/n)? "))

    def request_trump_call(self, hand: "Hand") -> bool:  # noqa: N803
        """Request a human player to call a trump suit.

        Args:
            hand (Hand): Hand object that the player can use for context when making a decision.
        """
        return parse_bool(input(f"{self.name}: call trump (y/n)? "))

    def request_trump_choose(self, hand: "Hand") -> bool:  # noqa: N803
        """Request a human player to choose a trump suit.

        Args:
            hand (Hand): Hand object that the player can use for context when making a decision.
        """
        raise NotImplementedError


class Bot(Player):
    """Represents a bot player."""

    def request_card(self, hand: "Hand") -> Card:
        """Request a bot player to play a card.

        Args:
            hand (Hand): Hand object that the player can use for context when making a decision.
        """
        # TODO write code here - subclass again for varying bot strengths?
        return self.cards[0]
