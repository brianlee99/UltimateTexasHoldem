from Card import Card
from enum import Enum
import operator

class HandType(Enum):
    ROYAL_FLUSH = 10
    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIRS = 3
    ONE_PAIR = 2
    HIGH_CARD = 1
###############################################
#           FUNCTION DECLARATIONS             #
###############################################
CARDS_TEST = [Card(11, 'S'),
              Card(2, 'S'),
              Card(6, 'S'),
              Card(8, 'S'),
              Card(4, 'S'),
              Card(6, 'H'),
              Card(9, 'D')]
CARDS_TEST2 = [Card(5, 'H'),
              Card(6, 'S'),
              Card(7, 'C'),
              Card(8, 'C'),
              Card(9, 'S'),
              Card(6, 'H'),
              Card(9, 'D')]

# Attempts to find a straight from a list of 7 cards.
# Returns a list of cards in increasing, consecutive order if there are at least
# 5 cards in a row. Otherwise, returns an empty list.
def find_straights(cards):
    str_exists = False
    # the last card is an ace
    if cards[-1][0] == 14:
        # the first card is a 2
        # in this case, start with [Ace, 2]
        if cards[0][0] == 2:
            str_cards = [cards[-1], cards[0]]
        # otherwise, start with the lowest card (that is not a 2)
        else:
            str_cards = [cards[0]]
    # the last card is not an ace; start with the lowest card
    else:
        str_cards = [cards[0]]

    for i in range(1, len(cards)):
        curr = cards[i]
        prev = cards[i - 1]
        if curr[0] == prev[0]:  # same value
            continue
        elif curr[0] - prev[0] == 1:  # differ by exactly 1
            str_cards.append(curr)
            if len(str_cards) == 5:
                str_exists = True
        else:  # differ by 2 or more
            if str_exists:
                break  # no more cards can be added to the straight
            else:
                str_cards = [curr]

    # fewer than 5 cards in the straight
    if len(str_cards) < 5:
        return []

    return str_cards

# Using the list of flush cards, this function attempts to find straight flushes.
# If a continuous sequence of 5 or more cards of the same suit exists,
# returns that entire sequence. Otherwise, returns None.
def find_straight_flush(cards):
    sf_exists = False
    if cards[-1][0] == 14:
        # the first card is a 2
        # in this case, start with [Ace, 2]
        if cards[0][0] == 2:
            sf_cards = [cards[-1], cards[0]]
        # otherwise, start with the lowest card (that is not a 2)
        else:
            sf_cards = [cards[0]]
    # the last card is not an ace; start with the lowest card
    else:
        sf_cards = [cards[0]]
    for i in range(1, len(cards)):
        curr = cards[i]
        prev = cards[i-1]
        if curr[0] - prev[0] == 1:  # differ by exactly 1
            sf_cards.append(curr)
            if len(sf_cards) == 5:
                sf_exists = True
        else:  # differ by 2 or more
            if sf_exists:
                break  # no more cards can be added to the straight
            else:
                sf_cards = [curr]

    # fewer than 5 cards in the straight
    if len(sf_cards) < 5:
        return []

    return sf_cards

def identify_hand(cards):
    cards = sorted(cards, key=operator.attrgetter('rank'))  # sort cards for simplicity
    quads = []
    trips = []
    pairs = []
    flush = []
    straight_flush = []
    suits = {'H': [], 'C': [], 'D': [], 'S': []}
    ranks = {2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [],
             11: [], 12: [], 13: [], 14: []}

    # count how many cards of each suit, and of each rank, there are
    for card in cards:
        suits[card[1]].append(card)
        ranks[card[0]].append(card)

    # finding all cards that can make a flush
    for suit, count in suits.items():
        if len(count) >= 5:
            flush.extend(count)
            straight_flush = find_straight_flush(flush)  # only look for a sf if there is a flush
            break  #  no more than one suit to consider

    # consider quads (all 4 suits of a value), trips (3 out of 4), and pairs (2 out of 4)
    for rank, count in ranks.items():
        if len(count) == 4:
            quads.extend(count)  # only one quad may exist
        elif len(count) == 3:
            trips.append(count)
        elif len(count) == 2:
            pairs.append(count)

    # find all cards that go up consecutively
    straight = find_straights(cards)

    # starting with royal flush, look for the best hand that the player/dealer possesses
    if straight_flush:
        # possibly has a royal flush
        if straight_flush[-1][0] == 14:  # ace high straight flush = royal flush
            return straight_flush[-5:], HandType.ROYAL_FLUSH  # return the best five cards
        else:
            return straight_flush[-5:], HandType.STRAIGHT_FLUSH
    elif quads:
        quad_value = quads[0][0]
        # find all cards that do not have the same value as the 'quad'
        rest = [card for card in cards if card[0] != quad_value]
        # pick the best kicker by sorting
        rest.sort(key=operator.attrgetter('rank'))
        kicker = rest[-1]
        # append the kicker to the list of cards that contains the quad
        quads.append(kicker)
        return quads, HandType.FOUR_OF_A_KIND
    elif trips and pairs:  # full house
        # only one trip to chose from
        fh_trips = trips[0]
        # select the highest-ranked pair
        fh_pair = pairs[-1]
        # concatenate
        fh_hand = fh_trips + fh_pair
        return fh_hand, HandType.FULL_HOUSE
    elif len(trips) == 2: # also full house
        # select the highest-ranked trips
        fh_trips = trips[-1]
        # select two cards from the lowest-ranked trips
        fh_pair = trips[0][0:2]
        fh_hand = fh_trips + fh_pair
        return fh_hand, HandType.FULL_HOUSE
    elif flush:
        # simply pick the best 5 cards of the flush suit
        return flush[-5:], HandType.FLUSH
    elif straight:
        # within the straight array, each element is a list of all cards that have the same value
        # need to unpack this, and so will choose any card within each list to be part of the straight
        straight = straight[-5:]
        return straight, HandType.STRAIGHT
    elif trips:
        # there is only one trip, otherwise the player would have a full house
        trip_value = trips[0][0][0]
        rest = [card for card in cards if card[0] != trip_value]
        # pick the best two
        rest.sort(key=operator.attrgetter('rank'))
        kickers = rest[-2:]
        trips_hand = trips[0] + kickers
        return trips_hand, HandType.THREE_OF_A_KIND
    elif len(pairs) >= 2:
        first = pairs[-1][0][0]  # the largest pair value
        second = pairs[-2][0][0]  # the second largest pair value
        rest = [card for card in cards if card[0] != first and card[0] != second]
        # pick the best card
        rest.sort(key=operator.attrgetter('rank'))
        kicker = rest[-1]
        two_pairs_hand = pairs[-1] + pairs[-2] + [kicker]
        return two_pairs_hand, HandType.TWO_PAIRS
    elif len(pairs) == 1:
        # only one pair to pick from
        pair_value = pairs[0][0][0]
        rest = [card for card in cards if card[0] != pair_value]
        rest.sort(key=operator.attrgetter('rank'))
        # pick the best 3 cards
        kickers = rest[-3:]
        pair_hand = pairs[0] + kickers
        return pair_hand, HandType.ONE_PAIR
    else:
        return cards[-5:], HandType.HIGH_CARD

# A class that represents the five cards that make up a poker hand.
# These are computed using the identify_hand() function on an array of seven cards (for both the player
# and the dealer). A PokerHand object includes information on not only the cards themselves that make up
# the hand, but also the type of hand (e.g. full house, three-of-a-kind), represented as Enums, as well as
# properties unique to the hand (e.g. for a three-of-a-kind, what is the value of the 'trips', and what
# are the values of the two kickers?)222244
class PokerHand:
    def __init__(self, cards):
        self.cards, self.type = identify_hand(cards)
        self.set_props()
        # print("Cards:", self.cards)
        # print("Type of hand:", self.type)
        # print("Properties:", self.props)
    def set_props(self):
        if self.type == HandType.ROYAL_FLUSH:
            self.props = {'value1': 14}
        elif self.type == HandType.STRAIGHT_FLUSH:
            # value1 represents 'high', that's all we care about when comparing straight flushes
            self.props = {'value1': self.cards[-1][0]}
        elif self.type == HandType.FOUR_OF_A_KIND:
            self.props = {'value1': self.cards[0][0],
                          'value2': self.cards[-1][0]}
        elif self.type == HandType.FULL_HOUSE:
            self.props = {'value1': self.cards[0][0],
                          'value2': self.cards[-1][0]}
        elif self.type == HandType.FLUSH:
            self.props = {'value'+str(i): self.cards[-i][0] for i in range(1,6)}
        elif self.type == HandType.STRAIGHT:
            # same goes for regular straights as straight flushes
            self.props = {'value1': self.cards[-1][0]}
        elif self.type == HandType.THREE_OF_A_KIND:
            self.props = {'value1': self.cards[0][0],
                          'value2': self.cards[-1][0],  # where value2 is the best kicker
                          'value3': self.cards[-2][0]}  # value3 is the second best kicker
        elif self.type == HandType.TWO_PAIRS:
            self.props = {'value1': self.cards[0][0],  # value1 is the better pair
                          'value2': self.cards[2][0],  # value2 is the worse pair
                          'value3': self.cards[4][0]}  # value3 is the kicker
        elif self.type == HandType.ONE_PAIR:
            self.props = {'value1': self.cards[0][0],
                          'value2': self.cards[-1][0],
                          'value3': self.cards[-2][0],
                          'value4': self.cards[-3][0]}
        elif self.type == HandType.HIGH_CARD:
            self.props = {'value'+str(i): self.cards[-i][0] for i in range(1,6)}

    def __repr__(self):
        return "{}\n{}\n".format(self.type, self.cards)