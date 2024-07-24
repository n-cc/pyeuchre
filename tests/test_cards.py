"""Tests for card functions and classes."""

import pytest
from pyeuchre.cards import Rank, RANKS, Suit, SUITS, Card, Deck, is_trump

# TODO add test for gt, lt, color comparisons for ranks and suits

def test_rank_eq():
    for i in range(0, len(RANKS)):
        assert RANKS[i] == RANKS[i] and RANKS[i] != RANKS[(i + 1) % len(RANKS)]

def test_rank_short():
    assert isinstance(RANKS[0].short, str)

def test_rank_long():
    assert isinstance(RANKS[0].long, str)

def test_rank_str():
    assert isinstance(str(RANKS[0]), str)

def test_suit_eq():
    for i in range(0, len(SUITS)):
        assert SUITS[i] == SUITS[i] and SUITS[i] != SUITS[(i + 1) % len(SUITS)]

def test_suit_short():
    assert isinstance(SUITS[0].short, str)

def test_suit_long():
    assert isinstance(SUITS[0].long, str)

def test_suit_str():
    assert isinstance(str(SUITS[0]), str)

def test_card_eq():
    a = Card(SUITS[0], RANKS[0])
    b = Card(SUITS[0], RANKS[1])
    c = Card(SUITS[1], RANKS[0])
    d = Card(SUITS[1], RANKS[1])
    e = Card(SUITS[0], RANKS[0])
    assert a == e and a != b and a != c and a != d

def test_card_suit():
    assert isinstance(Card(SUITS[0], RANKS[0]).suit, Suit)

def test_card_rank():
    assert isinstance(Card(SUITS[0], RANKS[0]).rank, Rank)

def test_card_str():
    assert isinstance(str(Card(SUITS[0], RANKS[0])), str)

def test_deck_cards():
    deck = Deck()
    for card in deck.cards:
        assert isinstance(card, Card)

def test_deck_shuffle():
    unshuffled = Deck()
    shuffled = Deck()

    shuffled.shuffle()

    for i in range(0, len(shuffled.cards)):
        if unshuffled.cards[0] != shuffled.cards[0]:
            assert True
            break
    else:
        assert False

def test_deck_deal():
    deck = Deck()
    prev = len(deck.cards)

    assert isinstance(list(deck.deal())[0], Card)
    assert len(deck.cards) == prev - 1

def test_trump():
    assert is_trump(Card(Suit((1, "s", "♠", "spades")), Rank((2, True, "j", "jack"))), Suit((1, "s", "♠", "spades")))
    assert is_trump(Card(Suit((1, "s", "♠", "spades")), Rank((1, False, "10", "ten"))), Suit((1, "s", "♠", "spades")))
    assert not is_trump(Card(Suit((0, "d", "♦", "diamonds")), Rank((2, True, "j", "jack"))), Suit((1, "s", "♠", "spades")))
    assert not is_trump(Card(Suit((1, "c", "♣", "clubs")), Rank((1, False, "10", "ten"))), Suit((1, "s", "♠", "spades")))
