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


def prompt(f):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return f(*args, **kwargs)
            except InvalidInputError as e:
                print(str(e) if str(e) else "Invalid choice.")

    return wrapper


def prompt_card(f):
    @prompt
    def wrapper(*args, **kwargs):
        card = parse_card(f(*args, **kwargs))
        if card not in args[0].cards:
            raise InvalidInputError(f"Card not in hand: {card}")
        return card

    return wrapper


def prompt_bool(f):
    @prompt
    def wrapper(*args, **kwargs):
        return parse_bool(f(*args, **kwargs))

    return wrapper


def prompt_suit(f):
    @prompt
    def wrapper(*args, **kwargs):
        return parse_suit(f(*args, **kwargs))

    return wrapper


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
        self.team: Team | None = None

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

    @prompt_card
    def request_replace_card(self, hand: "Hand", card: Card) -> Card:  # noqa: N803
        """Request a human player replace a card in their hand with a new card."""
        return input(f"{self.name}: which card to replace? ")

    @prompt_bool
    def request_loner(self, hand: "Hand") -> bool:  # noqa: N803
        """Request a human player to decide if they want go alone."""
        return input(f"{self.name}: go alone (y/n)? ")

    @prompt_bool
    def request_trump_call(self, hand: "Hand") -> bool:  # noqa: N803
        """Request a human player to call a trump suit.

        Args:
            hand (Hand): Hand object that the player can use for context when making a decision.
        """
        return input(f"{self.name}: call trump (y/n)? ")

    # TODO get this decorator working
    # @prompt_suit
    def request_trump_choose(self, hand: "Hand") -> Suit | None:  # noqa: N803
        """Request a human player to choose a trump suit.

        TODO: Move some of this logic elsewhere so that game logic is not contained in the Human class.

        Args:
            hand (Hand): Hand object that the player can use for context when making a decision.
        """
        while True:
            try:
                choice = input(f"{self.name}: call a suit (suit/n)? ")
                input(f"{self.name}: call a suit (suit/n)? ")
                try:
                    if not parse_bool(choice):
                        if hand.players.dealer is not self:
                            return None
                        else:
                            print("You must choose a suit!")
                            continue
                except InvalidInputError:
                    suit = parse_suit(choice)
                    if suit == hand.lead.suit:
                        print("You cannot choose the suit of the lead card.")
                    else:
                        return suit
            except InvalidInputError:
                print("Invalid choice.")

    @prompt_card
    def request_play_card(self, hand: "Hand") -> Card:
        """Request a human player to play a card.

        args:
            hand (Hand): Hand object that the player can use for context when making a decision.
        """
        return input(f"{self.name}: Card to play? ")

    def swap_card(self, before: Card, after: Card) -> None:
        for i, card in enumerate(self.cards):
            if card == before:
                self.cards[i] = after


class Bot(Player):
    """Represents a bot player."""

    # TODO write code here - subclass again for varying bot strengths?
    pass
