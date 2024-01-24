"""Exceptions."""


class InvalidInputError(Exception):
    """Indicates that the user provided invalid input."""

    pass


class DeckExhaustedError(Exception):
    """Indicates the deck would have been exhausted with the requested number of cards to deal."""

    pass
