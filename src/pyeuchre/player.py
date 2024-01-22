"""Classes pertaining to players."""


import typing

from pyeuchre.cards import Card


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

    def __str__(self) -> str:
        """Return Player as a printable string."""
        return self.name

    def __repr__(self) -> str:
        """Return Player as a printable string."""
        return f"{type(self).__name__}(name={self.name})"

    def request_trump_call(self, hand: "Hand") -> bool:  # noqa: N803
        """Request a player to decide if they want to call a face up trump value."""
        raise NotImplementedError

    def request_trump_choose(self, hand: "Hand") -> bool:  # noqa: N803
        """Request a player to decide if they want to choose a trump."""
        raise NotImplementedError

    def request_card(self, hand: "Hand") -> Card:
        """Request a player to play a card.

        Args:
            hand (Hand): Game object that the player can use for context when making a decision.
        """
        raise NotImplementedError


class Human(Player):
    """Represents a human player."""

    def request_card(self, hand: "Hand") -> Card:
        """Request a human player to play a card.

        Args:
            hand (Hand): Hand object that the player can use for context when making a decision.
        """
        # TODO flesh this out more
        card = input("Card number?")
        return self.cards[card]  # type: ignore [no-any-return,call-overload]

    def request_trump_call(self, hand: "Hand") -> bool:  # noqa: N803
        """Request a human player to call a trump suit.

        Args:
            hand (Hand): Hand object that the player can use for context when making a decision.
        """
        r = input(f"{self.name}: call trump (y/n)? ")

        if r in ["Y", "y"]:
            return True
        return False

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
            hand (Hand): Game object that the player can use for context when making a decision.
        """
        # TODO write code here - subclass again for varying bot strengths?
        return self.cards[0]


class Team:
    """Represents a team."""

    def __init__(
        self, players: tuple[Player, Player], score: int = 0, tricks: int = 0
    ) -> None:
        """Initialize team.

        Args:
            players (tuple): Tuple of players for the team.
            score (int): Score for the team.
            tricks (int): Number of tricks the team currently holds.
        """
        self.players = players
        self.score = score
        self.tricks = tricks

    def __str__(self) -> str:
        """Return Team as a printable string."""
        return f"{self.players[0]} and {self.players[1]}"

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
        self.players: list[Player] = []

        # TODO sanity check that teams have same length
        for i in range(len(self.teams[0].players)):
            self.players.append(self.teams[0].players[i])
            self.players.append(self.teams[1].players[i])

        self._dealer_index = 0

    @property
    def start_player(self) -> Player:
        """Returns the start player for a hand (left of the dealer)."""
        return self.players[(self._dealer_index + 1) % len(self.players)]

    @property
    def dealer(self) -> Player:
        """Returns the dealer for a hand."""
        return self.players[self._dealer_index % len(self.players)]

    def get_team(self, player: Player) -> Team:
        """Get the team for a player.

        Args:
            player (Player): Player to get the team for.
        """
        for team in self.teams:
            if player in team.players:
                return team

        # TODO custom exception or return None?
        raise IndexError

    def players_ordered(self, first: Player) -> typing.Generator[Player, None, None]:
        """Yields players to play after (and including) first.

        Args:
            first (Player): First player.
        """
        i = 0
        for player in self.players:
            if player is first:
                break
            i += 1

        for j in range(len(self.players)):
            yield self.players[(j + i) % len(self.players)]

    def rotate_dealer(self) -> None:
        """Rotates the dealer."""
        self._dealer_index += 1
