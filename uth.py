import sys, itertools, random

# For testing purpose, --table_min = 5, --balance = 1000
def main(args):
    for i in range(len(args)):
        if args[i] == "--balance":
            balance =  args[i+1]
        if args[i] == "--table_min":
            table_min = args[i+1]
    # Start the game once initialized
    UTH(balance, table_min)


class Card:
    # In this program, Aces are represented as 14 internally (but can also be part of
    # an ace-low straight or straight flush).
    ranks = {2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten',
             11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
    suits = {'S': 'Spades', 'C': 'Clubs', 'H': 'Hearts', 'D': 'Diamonds'}

    def __init__(self, r: int, s: str):
        self.rank = r
        self.suit = s
        self.name = Card.ranks[r] + ' of ' + s


class Deck:
    def __init__(self):
        self.cards = [card for card in itertools.product((range(2,15)), ['C', 'D', 'H', 'S'])]
        random.shuffle(self.cards)

    # Pops the leftmost element in the deck (being the top of the deck) and returns it
    def draw(self):
        card = self.cards.pop(0)
        return card


class UTH:
    bet_ante = 0
    bet_blind = 0
    bet_trips = 0

    def __init__(self, balance, table_min):
        self.balance = int(balance)
        self.table_min = int(table_min)
        print("Welcome to Ultimate Texas Hold'em!")
        self.play()

    def set_ante_bets(self):
        bet_input = int(input())
        # If bet_input * 2 < balance, then ask again how much to bet.
        while bet_input < self.table_min or self.balance < 2*bet_input:
            if bet_input < self.table_min:
                print("Your bet is under the table minimum.")
                print("Please place another bet: ", end="")
                bet_input = int(input())
            elif self.balance < 2*bet_input:
                print("You do not have enough to cover the requested bet")
                print("Please place another bet: ", end="")
                bet_input = int(input())
        self.bet_ante = bet_input
        self.bet_blind = bet_input
        self.balance -= 2*bet_input

    def set_trips_bet(self):
        bet_input = int(input())
        while bet_input < self.table_min or self.balance < bet_input:
            if bet_input < self.table_min:
                print("Your bet is under the table minimum.")
                print("Please place another bet: ", end="")
                bet_input = int(input())
            elif self.balance < 2*bet_input:
                print("You do not have enough to cover the requested bet")
                print("Please place another bet: ", end="")
                bet_input = int(input())
        self.bet_trips = bet_input
        self.balance -= bet_input

    def print_ante_bets(self):
        print("You have placed", self.bet_ante, "and", self.bet_blind, "on ante/blind.")
        print("New balance:", self.balance)

    def print_trips_bet(self):
        print("You have placed", self.bet_trips, "on trips.")
        print("New balance:", self.balance)

    def refund_bets(self):
        self.balance += (self.bet_ante + self.bet_blind + self.bet_trips)
        self.bet_ante = 0
        self.bet_blind = 0
        self.bet_trips = 0

    def play(self):
        # First, place bets on ante/blind
        print("Please place a bet on the ante/blind: ", end="")
        self.set_ante_bets()
        self.print_ante_bets()

        # Ask user if she/he wants to bet on trips
        print("Would you like to bet on trips?")
        print("1. Yes")
        print("2. No")
        answer = int(input())
        if answer == 1:
            print("Please place a bet on trips: ", end="")
            self.set_trips_bet()
        # Print out Trips bet, if placed
        self.print_trips_bet()

        # Ask user if they are ready
        print("Would you like to start the hand?")
        print("1. Yes")
        print("2. No")
        answer = int(input())
        if answer == 1:
            self.hand()
        else:
            # Refund bets
            self.refund_bets()
            print("Your bets have been refunded.")
            print("New balance:", self.balance)

    def game_bet(self):
        # pass

    def fold(self):


    def hand(self):
        print("Good luck!")
        # Creates a Deck object for the game
        deck = Deck()
        player_hand = []
        dealer_hand = []
        community_cards = []
        # Distribute 5, 2, and 2 cards to board, player, dealer respectively.
        for i in range(5):
            card = deck.draw()
            community_cards.append(card)
        for i in range(2):
            card = deck.draw()
            player_hand.append(card)
        for i in range(2):
            card = deck.draw()
            dealer_hand.append(card)

        # TODO: Course of action begins. The player has the opportunity to look at his/her cards, and
        print("Your cards are:", player_hand)
        print("Your options:")
        print("1) Bet 4x")
        print("2) Bet 3x")
        print("3) Check")
        choice = int(input())
        if choice == 1:
            self.game_bet(4)
        elif choice == 2:
            self.game_bet(3)
        elif choice != 3:
            print("Please input a valid answer")
        print("Checking.")
        # Open the first 3 community cards
        print("The flop is:", community_cards[0:3])
        print("Your cards are:", player_hand)
        print("Your options:")
        print("1) Bet 2x")
        print("2) Check")
        choice = int(input())
        if choice == 1:
            self.game_bet(2)
        elif choice != 3:
            print("Please input a valid answer")
        print("Checking.")
        # Open the last 2 community cards
        print("The river is:", community_cards)
        print("Your cards are:", player_hand)
        print("Your options:")
        print("1) Bet 1x")
        print("2) Fold")
        if choice == 1:
            self.game_bet(1)
        elif choice == 2:
            self.fold()




if __name__ == '__main__':
    main(sys.argv)

# Project outline:
# example run: py uth.py --balance 1000 --table_min 5
# This will run UTH with a starting balance of $1000 and table_minimum of $5.

# You are allowed to bet in dollar increments
# Every round, the user will input an amount to bet on the ante. (The corresponding amount will go on the blind.)
# The balance goes down IN THE BEGINNING. If they win they will get about double back, if they lose they don't get anything
# If they "push" they will get most of their bets back
# An optional 'trips' bet is permissible.
# Once the user says 'go', 5 community cards come face down, then 2 cards to player, then to the dealer.
# Player can inspect their cards.

# ... play out the game, and at the end bets are settled.