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
    return s.lower() in ["y", "yes"]


def parse_card(s: str) -> Card:
    """Parses input for a card.

    Args:
        s (str): Input to parse.
    """
    r = re.search(r"([A-Za-z]+|[0-9]+)\s?o?f?\s?([A-Za-z]+)", s)
    if not r or not r[1] or not r[2]:
        raise InvalidInputError

    s_rank = r[1]
    s_suit = r[2]

    c_rank: Rank | None = None
    c_suit: Suit | None = None

    for rank in RANKS:
        if s_rank in [rank.short, rank.long]:
            c_rank = rank

    for suit in SUITS:
        if s_suit in [suit.short, suit.ascii, suit.long]:
            c_suit = suit

    if not c_rank or not c_suit:
        raise InvalidInputError

    return Card(c_suit, c_rank)
