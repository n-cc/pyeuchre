"""Classes facilitating the flow of the game of Euchre."""

from __future__ import annotations

from pyeuchre.cards import Card
from pyeuchre.cards import Deck
from pyeuchre.cards import is_trump
from pyeuchre.exceptions import NotActiveError
from pyeuchre.people.groups import Players
from pyeuchre.people.groups import Team
from pyeuchre.people.players import Human
from pyeuchre.people.players import Player


class Game:
    """Represents a game of Euchre."""

    def __init__(
        self,
        players: Players | None = None,
        hand: Hand | None = None,
    ) -> None:
        """Initialize game.

        Args:
            players (Players): Players to start this game with.
            hand: (Hand): A custom hand to start the game on.
        """
        if players:
            self.players = players
        else:
            self.players = Players(
                (
                    Team(
                        (Human("North"), Human("South")),
                    ),
                    Team(
                        (Human("East"), Human("West")),
                    ),
                )
            )

        self.hand: Hand | None = hand if hand else None

    def __str__(self) -> str:
        """Return Game as a printable string.

        TODO get much better printing here.
        """
        return f"{self.players}"

    def __repr__(self) -> str:
        """Return Game as a printable object string."""
        return f"{type(self).__name__}(name={self.players})"

    @property
    def active(self) -> bool:
        """Is this game active."""
        return not any([team.score >= 10 for team in self.players.teams])

    def deal_hand(self) -> None:
        """Begin a hand."""
        if self.active:
            self.hand = Hand(self.players)
        else:
            raise NotActiveError


class Hand:
    """Represents a hand."""

    def __init__(
        self,
        players: Players,
        deck: Deck | None = None,
        shuffle_deck: bool = True,
    ) -> None:
        """Initialize hand.

        Args:
            players (Players): Players for this hand.
            deck (Deck): Custom deck to use.
            shuffle_deck (bool): Whether to auto-shuffle the deck.
        """
        self.players = players
        self.lead: Card | None = None
        self.kitty: list[Card] = []

        self.trick: Trick | None = None

        self.trump_team: Team | None = None
        self.trump_suit: Suit | None = None

        self.loner_player: Player | None = None

        if deck:
            self.deck = deck
        else:
            self.deck = Deck()

        if shuffle_deck:
            self.deck.shuffle()

        self.deal()

    def __str__(self) -> str:
        """Return Trick as a printable string.

        TODO get much better printing here.
        """
        return "Players: {players}\n\nLead: {lead}\n\nHands:\n{cards}\n".format(
            players=" vs ".join(
                [
                    f"{team} ({team.score} points, {team.tricks} tricks)"
                    for team in self.players.teams
                ]
            ),
            lead=self.lead,
            cards="\n".join(
                [
                    "{name}: {cards}".format(
                        name=player.name,
                        cards=", ".join([str(card) for card in player.cards]),
                    )
                    for player in self.players
                ]
            ),
        )

    def __repr__(self) -> str:
        """Return Hand as a printable string."""
        return f"{type(self).__name__}(lead={self.lead})"

    @property
    def active(self) -> bool:
        """Determine whether a hand is active."""
        for player in self.players:
            if len(player.cards) > 0:
                return True

        return False

    def deal(self) -> None:
        """Deals hand."""
        for player in self.players:
            player.cards = list(self.deck.deal(5))

        self.lead = next(self.deck.deal(1))
        self.kitty = list(self.deck.deal(3))

    def process_call_trump(self) -> None:
        """Processes calling trump."""
        # Let players pick the lead card up if desired
        for player in self.players.ordered(self.players.start_player):
            if player.request_trump_call(self):
                self.trump_suit = self.lead.suit
                player.request_replace_card(self, self.lead)
                self.trump_team = self.players.get_team(player)
                if player.request_loner(self):
                    self.loner_player = player
                    self.players.get_partner(player).skip = True
                return None

        # If the lead card is not picked up, let players choose trump
        for player in self.players.ordered(self.players.start_player):
            choice = player.request_trump_choose(self, self.players.dealer)
            if choice:
                self.suit = choice
                self.trump_team = self.players.get_team(player)
                if player.request_loner(self):
                    self.loner_player = player
                    self.players.get_partner(player).skip = True
                return None

        # TODO add third option based on whether we are playing with STD or not

    def start_trick(self) -> None:
        """Starts the next trick."""
        if self.active:
            self.trick = Trick(self, self.trump_suit)
        else:
            raise NotActiveError

    def record_trick(self) -> None:
        """Parses the current trick to determine a winner."""


class Trick:
    """Represents a Trick."""

    def __init__(self, hand: Hand, trump: Suit) -> None:
        """Init Trick."""
        self.hand: Hand = hand
        self.cards = []
        self.trump: Suit = trump
        self.suit: Suit | None = None

    def __str__(self) -> str:
        """Return Trick as a printable string.

        TODO get much better printing here.
        """
        return f"{self.cards}"

    def play(self) -> None:
        for player in self.hand.players.ordered(self.hand.players.start_player):
            if player.skip:
                continue

            card = player.request_play_card(self.hand)

            if not self.suit:
                self.suit = card.suit
            self.cards.append({"player": player, "card": card})

        wc = self.cards[0]["card"]
        wp = self.cards[0]["player"]

        for entry in self.cards[1:]:
            card = entry["card"]
            player = entry["player"]
            # if this card is trump, and...
            if is_trump(card, self.trump):
                # ... the current winner is not trump
                if not is_trump(wc, self.trump):
                    wp = player
                    wc = card
                else:
                    # ... this card is a "trumper (ie jack)", and...
                    if card.trumper:
                        # ... the current winner is not a trumper
                        if not wc.trumper:
                            wp = player
                            wc = card
                        # ... the current winner is a trumper, and...
                        else:
                            # ... this card has a higher rank than the current winner
                            if card.rank > wc.rank:
                                wp = player
                                wc = card
                            # ... this card is the exact same suit as the trump suit (left vs right bower)
                            if card.suit == self.trump:
                                wp = player
                                wc = card
                    # ... this card has a higher rank than the current winner
                    elif card.rank > wc.rank:
                        wp = player
                        wc = card
            # if this card is on suit and has a higher rank than the current winner
            elif card.suit == self.suit and card.rank > wc.rank:
                wp = player
                wc = card

        self.hand.players.get_team(wp).tricks += 1
