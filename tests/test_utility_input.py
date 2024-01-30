"""Tests for the input utility functions."""

from pyeuchre.utility.input import parse_bool, parse_suit, parse_rank, parse_card
from pyeuchre.exceptions import InvalidInputError

def test_parse_bool_true():
    """Test parse_bool true inputs."""
    for s in ["y", "yes"]:
        assert parse_bool(s) == True
        assert parse_bool(s.upper()) == True
        assert parse_bool(f" {s} ") == True

def test_parse_bool_false():
    """Test parse_bool false inputs."""
    for s in ["n", "no"]:
        assert parse_bool(s) == False
        assert parse_bool(s.upper()) == False
        assert parse_bool(f" {s} ") == False

def test_parse_bool_invalid():
    """Test parse_bool false inputs."""
    for invalid in ["asdf", "" " "]:
        try:
            parse_bool(invalid)
            assert False
        except InvalidInputError:
            assert True

def test_parse_suit():
    """Test suit parsing."""
    for s in ["s", "spades"]:
        assert parse_suit(s).short == "s"
        assert parse_suit(s.upper()).short == "s"

    for s in ["c", "clubs"]:
        assert parse_suit(s).short == "c"
        assert parse_suit(s.upper()).short == "c"

    for s in ["h", "hearts"]:
        assert parse_suit(s).short == "h"
        assert parse_suit(s.upper()).short == "h"

    for s in ["d", "diamonds"]:
        assert parse_suit(s).short == "d"
        assert parse_suit(s.upper()).short == "d"

def test_parse_rank():
    """Test rank parsing."""
    for s in ["9", "nine"]:
        assert parse_rank(s).short == "9"
        assert parse_rank(s.upper()).short == "9"

    for s in ["10", "ten"]:
        assert parse_rank(s).short == "10"
        assert parse_rank(s.upper()).short == "10"

    for s in ["j", "jack"]:
        assert parse_rank(s).short == "j"
        assert parse_rank(s.upper()).short == "j"

    for s in ["q", "queen"]:
        assert parse_rank(s).short == "q"
        assert parse_rank(s.upper()).short == "q"

    for s in ["k", "king"]:
        assert parse_rank(s).short == "k"
        assert parse_rank(s.upper()).short == "k"

    for s in ["a", "a"]:
        assert parse_rank(s).short == "a"
        assert parse_rank(s.upper()).short == "a"
