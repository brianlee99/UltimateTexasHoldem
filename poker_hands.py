import itertools
import random

###############################################
#           FUNCTION DECLARATIONS             #
###############################################
def draw_card(deck):
    card = deck.pop()  # Remove from the tail
    return card


def convert_val_to_num(val):
    conversions = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                   '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13}
    return conversions[val]


def sort_by_val(hand):
    vals = []
    for card in hand:
        vals.append(convert_val_to_num(card[0]))
    vals.sort()
    return vals


def identify_hand(hand):
    if is_royal(hand):
        return 'Royal Flush'
    elif is_straight_flush(hand):
        return 'Straight Flush'
    elif is_quads(hand):
        return 'Four of a Kind'
    elif is_full_house(hand):
        return 'Full House'
    elif is_flush(hand):
        return 'Flush'
    elif is_straight(hand):
        return 'Straight'
    elif is_trips(hand):
        return 'Three of a Kind'
    elif is_two_pairs(hand):
        return 'Two Pairs'
    elif is_pair(hand):
        return 'Pair'
    else:
        return 'High card'


def is_royal(hand):
    suit = hand[0][1]  # Every card in the hand must be this suit
    if hand[0][0] not in 'TJQKA':
        return False  # Must be one of 10, J, Q, K, or A
    for i in range(1, 5):
        if hand[i][1] != suit:
            return False
        if hand[i][0] not in 'TJQKA':
            return False
    return True  # Is a royal flush


def is_straight_flush(hand):
    return is_straight(hand) and is_flush(hand)


def is_quads(hand):
    sorted_vals = sort_by_val(hand)
    first_val = sorted_vals[0]
    second_val = sorted_vals[1]
    if second_val == first_val:  # First two cards are the same
        for i in range(2, 4):  # Check the third and fourth card
            if sorted_vals[i] != first_val:
                return False
        return True
    elif second_val != first_val:  # First two cards are different
        for i in range(2, 5): # Check the last 3 cards
            if sorted_vals[i] != second_val:
                return False
        return True


def is_full_house(hand):
    sorted_vals = sort_by_val(hand)
    first_val = sorted_vals[0]
    second_val = sorted_vals[3]

    if sorted_vals[1] != first_val:
        return False
    if sorted_vals[4] != second_val:
        return False
    middle_val = sorted_vals[2]  # must either belongs to first_val or second_val
    if middle_val != first_val and middle_val != second_val:
        return False

    return True


def is_flush(hand):
    suit = hand[0][1]
    for i in range(1, 5):
        if hand[i][1] != suit:
            return False
    return True


def is_straight(hand):
    sorted_vals = sort_by_val(hand)
    starting_val = sorted_vals[0]  # A number between 1 and 13
    if starting_val == 1:  # Check for ace-high straight
        curr = 9
        for i in range(1, 5):
            if sorted_vals[i] - curr != 1:
                break
            if i == 4:
                return True
            curr += 1
    for i in range(1, 5):  # Also accounts for ace-low straight
        if sorted_vals[i] - starting_val != 1:  # Must be a difference of 1:
            return False
        starting_val += 1
    return True


def is_trips(hand):
    sorted_vals = sort_by_val(hand)
    first_val = sorted_vals[0]
    last_val = sorted_vals[4]
    middle_val = sorted_vals[2]  # middle_val must either be the same as the first or the last card

    if middle_val == first_val:
        if sorted_vals[1] == first_val:
            return True
    elif middle_val == last_val:
        if sorted_vals[3] == last_val:
            return True
    else:
        return False


def is_two_pairs(hand):
    sorted_vals = sort_by_val(hand)
    first = sorted_vals[0]
    second = sorted_vals[1]
    if second == first:
        third = sorted_vals[2]
        if sorted_vals[3] == third:
            return True
        else:
            if sorted_vals[3] == sorted_vals[4]:
                return True
            else:
                return False
    else:
        if sorted_vals[1] == sorted_vals[2] and sorted_vals[3] == sorted_vals[4]:
            return True
        else:
            return False


def is_pair(hand):
    sorted_vals = sort_by_val(hand)
    for i in range(1, 5):
        if sorted_vals[i] == sorted_vals[i-1]:
            return True
    return False


# Creates a deck
values = "A23456789TJQK"
suits = "CDHS"
cards = itertools.product(values, suits)
deck = []

for card in cards:
    deck.append(''.join(card))

for card in deck:
    print(card)

# Shuffles the deck
random.seed()
random.shuffle(deck)

# Now the deck is shuffled.
hand = []
for i in range(5):
    card = draw_card(deck)
    hand.append(card)

# Print the hand
print(hand)


# Print the type of hand
print(identify_hand(hand))