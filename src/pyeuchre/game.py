"""Classes facilitating the flow of the game of Euchre."""

from __future__ import annotations

from cards import Deck


class Game:
    """Represents a game of Euchre."""

    def __init__(
        self,
        teams: tuple[Team, Team] | None = None,
        trick: Trick | None = None,
    ) -> None:
        """Initialize game.

        Args:
            teams (tuple): A tuple of two teams.
            trick: (Trick): A custom trick to start the game on.
        """
        if teams:
            self.teams = teams
        else:
            self.teams = (
                Team(Player("North"), Player("South")),
                Team(Player("East"), Player("West")),
            )

    def __str__(self) -> str:
        """Return Game as a printable string."""
        return self.teams

    def __repr__(self) -> str:
        """Return Game as a printable object string."""
        return f"{type(self).__name__}(name={self.teams})"


class Trick:
    """Represents a trick."""

    def __init__(
        self, plays: tuple[int, int] | None = None, deck: Deck | None = None
    ) -> None:
        """Initialize trick.

        Args:
            plays (tuple): Number of taken tricks for each team for this trick.
            deck (Deck): Custom deck to use.
        """
        if plays:
            self.plays = plays
        else:
            self.plays = [0, 0]

        if deck:
            self.deck = deck
        else:
            self.deck = Deck(deck)

    def __str__(self) -> str:
        """Return Trick as a printable string."""
        pass

    def __repr__(self) -> str:
        """Return Trick as a printable string."""
        pass


class Player:
    """Represents a player."""

    def __init__(self, name: str) -> None:
        """Initialize player.

        Args:
            name (str): Player's display name.
        """
        self.name = name

    def __str__(self) -> str:
        """Return Player as a printable string."""
        return self.name

    def __repr__(self) -> str:
        """Return Player as a printable string."""
        return f"{type(self).__name__}(name={self.name})"


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
