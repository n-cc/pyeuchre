"""Classes pertaining to players."""


from typing import TYPE_CHECKING

from pyeuchre.cards import Card


# only import Game for typing purposes within the Player class
if TYPE_CHECKING:
    from pyeuchre.game import Game


class Player:
    """Represents a player."""

    def __init__(self, name: str) -> None:
        """Initialize player.

        Args:
            name (str): Player's display name.
        """
        self.name = name
        self.hand: list[Card] = []

    def __str__(self) -> str:
        """Return Player as a printable string."""
        return self.name

    def __repr__(self) -> str:
        """Return Player as a printable string."""
        return f"{type(self).__name__}(name={self.name})"

    def request_trump_call(self, Game: "Game") -> bool:  # noqa: N803
        """Request a player to decide if they want to call a face up trump value."""
        raise NotImplementedError

    def request_trump_choose(self, Game: "Game") -> bool:  # noqa: N803
        """Request a player to decide if they want to choose a trump."""
        raise NotImplementedError

    def request_card(self, game: "Game") -> Card:
        """Request a player to play a card.

        Args:
            game (Game): Game object that the player can use for context when making a decision.
        """
        raise NotImplementedError


class Human(Player):
    """Represents a human player."""

    def request_card(self, game: "Game") -> Card:
        """Request a human player to play a card.

        Args:
            game (Game): Game object that the player can use for context when making a decision.
        """
        # TODO flesh this out more
        card = input("Card number?")
        return self.hand[card]  # type: ignore [no-any-return,call-overload]


class Bot(Player):
    """Represents a bot player."""

    def request_card(self, game: "Game") -> Card:
        """Request a bot player to play a card.

        Args:
            game (Game): Game object that the player can use for context when making a decision.
        """
        # TODO write code here - subclass again for varying bot strengths?
        return self.hand[0]


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


class Players:
    """Represents a group of players."""

    def __init__(self, teams: tuple[Team, Team]) -> None:
        """Initialize players.

        TODO __iter__ method to loop over players

        Args:
            teams (tuple): Tuple of teams.
        """
        self.teams = teams
        self.players = [player for team in self.teams for player in team.players]

        self._dealer_index = 0

    @property
    def start_player(self) -> Player:
        """Returns the start player for a hand (left of the dealer)."""
        return self.players[(self._dealer_index + 1) % len(self.players)]

    @property
    def dealer(self) -> Player:
        """Returns the dealer for a hand."""
        return self.players[self._dealer_index % len(self.players)]

    def rotate_dealer(self) -> None:
        """Rotates the dealer."""
        self._dealer_index += 1
