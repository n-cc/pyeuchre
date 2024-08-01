"""Classes pertaining groups of players."""

import typing

from pyeuchre.people.players import Player


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

    def __getitem__(self, i: int) -> Player:
        """Return self.players if self is treated as a list."""
        return self.players[i]

    def __iter__(self) -> typing.Generator[Player, None, None]:
        """Iterate over self.players."""
        yield from self.players

    def get_partner(self, player: Player) -> Player:
        """Given a player, get their partner."""
        for p in self.players:
            if player is not p:
                return p

        # TODO raise custom exception or return None?
        raise IndexError


class Players:
    """Represents a group of players within teams."""

    def __init__(self, teams: tuple[Team, Team]) -> None:
        """Initialize players.

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

    def __getitem__(self, i: int) -> Player:
        """Return self.players if self is treated as a list."""
        return self.players[i]

    def __iter__(self) -> typing.Generator[Player, None, None]:
        """Iterate over self.players."""
        yield from self.players

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

    def get_partner(self, player: Player) -> Player:
        for team in self.teams:
            if player in team.players:
                return team.get_partner(player)

        raise IndexError

    def ordered(self, first: Player) -> typing.Generator[Player, None, None]:
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
