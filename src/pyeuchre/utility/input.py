"""Classes and functions pertaining to parsing input."""

import re

from pyeuchre.cards import RANKS
from pyeuchre.cards import SUITS
from pyeuchre.cards import Card
from pyeuchre.cards import Rank
from pyeuchre.cards import Suit
from pyeuchre.exceptions import InvalidInputError


def parse_bool(s: str) -> bool:
    """Parses input for a yes or no question.

    Args:
        s (str): Input to parse.
    """
    if s.lower() in ["n", "no"]:
        return False
    if s.lower() in ["y", "yes"]:
        return True

    raise InvalidInputError


def parse_suit(s: str) -> Suit:
    """Parses input for a suit.

    Args:
        s (str): Input to parse.
    """
    r = re.search(r"([A-Za-z]+)", s)
    if not r or not r[1]:
        raise InvalidInputError

    for suit in SUITS:
        if r[1] in [suit.short, suit.ascii, suit.long]:
            return suit

    raise InvalidInputError


def parse_rank(s: str) -> Rank:
    """Parses input for a rank.

    Args:
        s (str): Input to parse.
    """
    r = re.search(r"([A-Za-z]+|[0-9]+)", s)
    if not r or not r[1]:
        raise InvalidInputError

    for rank in RANKS:
        if r[1] in [rank.short, rank.long]:
            return rank

    raise InvalidInputError


def parse_card(s: str) -> Card:
    """Parses input for a card.

    Args:
        s (str): Input to parse.
    """
    r = re.search(r"([A-Za-z]+|[0-9]+)\s*o?f?\s*([A-Za-z]+)", s)
    if not r or not r[1] or not r[2]:
        raise InvalidInputError

    return Card(parse_suit(r[2]), parse_rank(r[1]))
