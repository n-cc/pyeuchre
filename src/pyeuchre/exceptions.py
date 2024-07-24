"""Exceptions."""


class InvalidInputError(Exception):
    """Indicates that the user provided invalid input."""

    pass


class DeckExhaustedError(Exception):
    """Indicates the deck would have been exhausted with the requested number of cards to deal."""

    pass


class NotActiveError(Exception):
    """Indicates that a hand or a trick cannot be played as the game or hand is no longer active."""

    pass

class RenegeError(Exception):
    """Indicates that a player has attempted to renege."""

    pass