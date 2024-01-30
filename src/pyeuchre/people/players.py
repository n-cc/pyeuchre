"""Classes pertaining to players."""

import typing

from pyeuchre.cards import Card
from pyeuchre.cards import Suit
from pyeuchre.exceptions import InvalidInputError
from pyeuchre.utility.input import parse_bool
from pyeuchre.utility.input import parse_card
from pyeuchre.utility.input import parse_suit


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

    def request_trump_choose(self, hand: "Hand") -> Suit | None:  # noqa: N803
        """Request a player to decide if they want to choose a trump."""
        raise NotImplementedError

    def request_replace_card(self, hand: "Hand") -> None:  # noqa: N803
        """Request a player replace a card in their hand with a new card."""
        raise NotImplementedError

    def request_play_card(self, hand: "Hand") -> Card:
        """Request a player to play a card.

        Args:
            hand (Hand): Hand object that the player can use for context when making a decision.
        """
        raise NotImplementedError


class Human(Player):
    """Represents a human player."""

    def request_play_card(self, hand: "Hand") -> Card:
        """Request a human player to play a card.

        Args:
            hand (Hand): Hand object that the player can use for context when making a decision.
        """
        raise NotImplementedError

    def request_replace_card(self, hand: "Hand", card: Card) -> None:  # noqa: N803
        """Request a player replace a card in their hand with a new card."""
        while True:
            try:
                replace_card = parse_card(
                    input(f"{self.name}: which card to replace? ")
                )
            except InvalidInputError:
                print("Invalid choice.")
                continue

            for i, held_card in enumerate(self.cards):
                if held_card == replace_card:
                    self.cards[i] = card  # type: ignore[assignment]
                    return None
            else:
                print(f"Card not in hand: {replace_card}")

    def request_loner(self, hand: "Hand") -> bool:  # noqa: N803
        """Request a player to decide if they want go alone."""
        while True:
            try:
                return parse_bool(input(f"{self.name}: go alone (y/n)? "))
            except InvalidInputError:
                print("Invalid choice.")

    def request_trump_call(self, hand: "Hand") -> bool:  # noqa: N803
        """Request a human player to call a trump suit.

        Args:
            hand (Hand): Hand object that the player can use for context when making a decision.
        """
        while True:
            try:
                return parse_bool(input(f"{self.name}: call trump (y/n)? "))
            except InvalidInputError:
                print("Invalid choice.")

    def request_trump_choose(self, hand: "Hand", dealer: Player) -> Suit | None:  # noqa: N803
        """Request a human player to choose a trump suit.

        Args:
            hand (Hand): Hand object that the player can use for context when making a decision.
        """
        while True:
            try:
                choice = input(f"{self.name}: call a suit (suit/n)? ")
                try:
                    if not parse_bool(choice):
                        if dealer is not self:
                            return None
                        else:
                            print("You must choose a suit!")
                            continue
                except InvalidInputError:
                    return parse_suit(choice)
            except InvalidInputError:
                print("Invalid choice.")


class Bot(Player):
    """Represents a bot player."""

    # TODO write code here - subclass again for varying bot strengths?
    pass
