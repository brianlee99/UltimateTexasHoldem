import sys
import Deck


# For testing purpose, --table_min = 5, --balance = 1000
def main(args):
    for i in range(len(args)):
        if args[i] == "--balance":
            balance = args[i+1]
        if args[i] == "--table_min":
            table_min = args[i+1]
    # Start the game once initialized
    UTH(balance, table_min)


class UTH:

    def __init__(self, balance, table_min):

        # Passed in from main()
        self.balance = int(balance)
        self.table_min = int(table_min)

        # Other initialized variables
        self.bet_ante = 0
        self.bet_blind = 0
        self.bet_trips = 0
        self.bet_play = 0
        self.folded = False
        self.made_bet = False

        print("Welcome to Ultimate Texas Hold'em!")
        # Start the game, i.e. prompt user for bets
        self.play()

    # Checks if bet is enough to cover ante, blind and 1x play
    def check_ante_is_enough(self, bet):
        if 3 * bet <= self.balance:
            return True
        else:
            return False

    # Checks if the bet is a multiple of 5
    def check_mult_of_5(self, bet):
        if bet % 5 != 0:
            return False
        else:
            return True

    # Checks if table is at least the table min
    def check_above_min(self, bet):
        if bet < self.table_min:
            return False
        else:
            return True

    # Checks if trips does not prevent player from betting on play
    def check_trips_is_enough(self, bet):
        remainder = self.balance - bet
        if remainder < self.bet_ante:
            return False
        else:
            return True

    """Sets a bet on ante and blind in equal amounts. Note that the bet amount has to be a multiple of 5, greater than
    or equal to the table minimum (specified in self.table_min), and the player has to have *at least* 3x
    what he/she decides to bet on ante."""
    def set_ante_bets(self):
        # TODO: What if the user has less than 3*table_minimum? Check for this
        # Prompt user for a bet
        bet_input = int(input())

        is_enough = self.check_ante_is_enough(bet_input)
        mult_of_5 = self.check_mult_of_5(bet_input)
        above_min = self.check_above_min(bet_input)

        # If any of these are false, then prompt user again
        while not (is_enough and mult_of_5 and above_min):
            if not is_enough:
                print("You do not have enough to cover ante, blind, and 1x play")
                print("Please input a smaller amount: ", end="")
                bet_input = int(input())
                is_enough = self.check_ante_is_enough(bet_input)
                mult_of_5 = self.check_mult_of_5(bet_input)
                above_min = self.check_above_min(bet_input)

            elif not above_min:
                print("Your bet is below the table minimum")
                print("Please input a greater amount: ", end="")
                bet_input = int(input())
                is_enough = self.check_ante_is_enough(bet_input)
                mult_of_5 = self.check_mult_of_5(bet_input)
                above_min = self.check_above_min(bet_input)

            elif not mult_of_5:
                print("Your bet is not a multiple of 5")
                print("Please input another amount: ", end="")
                bet_input = int(input())
                is_enough = self.check_ante_is_enough(bet_input)
                mult_of_5 = self.check_mult_of_5(bet_input)
                above_min = self.check_above_min(bet_input)

        # Bet equal amounts on ante and blind
        self.bet_ante = bet_input
        self.bet_blind = bet_input
        self.balance -= 2*bet_input

    """Places a bet on trips. Note that tbe bet amount can be 0 (or greater), with $1 increments, as long as
    the player has enough to cover at least 1x ante after betting on trips. """
    def set_trips_bet(self):
        # Prompt user for a bet
        bet_input = int(input())
        # Checks if there is enough after betting on trips
        is_enough = self.check_trips_is_enough(bet_input)

        while not is_enough:
            print("You do not have enough to cover at least 1x play bet.")
            print("Please input a smaller amount: ", end="")
            bet_input = int(input())
            is_enough = self.check_ante_is_enough(bet_input)

        # Place bet on trips
        self.bet_trips = bet_input
        self.balance -= bet_input

    # Print the amount bet on ante and blind
    def print_ante_bets(self):
        print("You have placed", self.bet_ante, "and", self.bet_blind, "on ante/blind.")
        self.print_balance()

    # Print the amount bet on trips
    def print_trips_bet(self):
        print("You have placed", self.bet_trips, "on trips.")
        self.print_balance()

    def print_play_bet(self):
        print("You have placed", self.bet_play, "on play.")
        self.print_balance()

    # Print remaining balance
    def print_balance(self):
        print("Your balance is:", self.balance)

    # Refund all bets, including trips, ante, and blind. Resets all bets, and allows
    # user to place new values
    def refund_bets(self):
        self.balance += (self.bet_ante + self.bet_blind + self.bet_trips)
        self.bet_ante = 0
        self.bet_blind = 0
        self.bet_trips = 0

    def query_trips(self):
        print("Would you like to bet on trips?")
        print("1. Yes")
        print("2. No")
        answer = int(input())
        return answer

    # Multiplier is either 1, 2, 3, or 4
    def set_play_bet(self, mult):
        bet = mult*self.bet_ante
        if bet <= self.balance:
            self.bet_play = bet
            self.balance -= bet
            self.print_play_bet()
            return 0  # Everything okay
        else:  # Not enough to cover play bet
            print("You do not have enough to cover %sx ante.", mult)
            return -1  # Error

    def play(self):
        # First, place bets on ante/blind. Due to the way set_ante_bets() works,
        # the play function will not continue until the user has specified a valid bet amount.
        print("Please place a bet on the ante/blind: ", end="")
        self.set_ante_bets()
        self.print_ante_bets()

        # Query the user until they provide either 1 or 2 as an answer
        answer = self.query_trips()
        while answer != 1 and answer != 2:
            print("Please input a valid answer")
            answer = self.query_trips()
        # If the answer is 1, call set_trips_bet().
        if answer == 1:
            print("Please place a bet on trips: ", end="")
            self.set_trips_bet()
            self.print_trips_bet()
        # If the answer is 2, do nothing
        elif answer == 2:
            pass

        # Ask user if they are ready
        print("Would you like to start the hand?")
        print("1. Yes")
        print("2. No")
        answer = int(input())
        while answer != 1 and answer != 2:
            print("Please input a valid answer")
            print("Would you like to start the hand?")
            print("1. Yes")
            print("2. No")
            answer = int(input())
        if answer == 1:
            # Start the hand
            self.hand()
        elif answer == 2:
            # Refund bets
            self.refund_bets()
            print("Your bets have been refunded.")
            self.print_balance()

    def fold(self):
        print("You have folded")
        # Lose your ante and your blind
        self.bet_ante = 0
        self.bet_blind = 0
        # If you have a trips or better, get paid on your trips
        self.folded = True

    player_hand = []
    dealer_hand = []
    community_cards = []

    def print_cards(self, cards):
        for card in cards:
            print(card.name)
        print()

    def hand(self):
        print("Good luck!")
        # Creates a Deck object for the game
        deck = Deck.Deck()

        # Distribute 5, 2, and 2 cards to board, player, dealer respectively.
        for i in range(5):
            card = deck.draw()
            self.community_cards.append(card)
        for i in range(2):
            card = deck.draw()
            self.player_hand.append(card)
        for i in range(2):
            card = deck.draw()
            self.dealer_hand.append(card)

        # TODO: Course of action begins. The player has the opportunity to look at his/her cards, and
        print("Your cards are:")
        self.print_cards(self.player_hand)
        print("Your options:")
        print("1) Bet 4x")
        print("2) Bet 3x")
        print("3) Check")
        answer = int(input())
        while answer != 1 and answer != 2 and answer != 3:
            print("Please input a valid answer")
            print("Your options:")
            print("1) Bet 4x")
            print("2) Bet 3x")
            print("3) Check")
            answer = int(input())
        if answer == 1:
            self.set_play_bet(4)
            self.made_bet = True
            print("You have made a 4x bet on play.")
        elif answer == 2:
            self.set_play_bet(3)
            self.made_bet = True
            print("You have made a 3x bet on play.")
        elif answer == 3:
            print("Checking.")
        # elif answer == 3:
        #     pass

        # Open the first 3 community cards
        print("The flop is:")
        self.print_cards(self.community_cards[0:3])
        print("Your cards are:")
        self.print_cards(self.player_hand)
        if not self.made_bet:
            print("Your options:")
            print("1) Bet 2x")
            print("2) Check")
            answer = int(input())
            while answer != 1 and answer != 2:
                print("Please input a valid answer")
                print("Your options:")
                print("1) Bet 2x")
                print("2) Check")
                answer = int(input())
            if answer == 1:
                self.set_play_bet(2)
                self.made_bet = True
                print("You have made a 2x bet on play.")
            elif answer == 2:
                print("Checking.")

        print("The river is:")
        self.print_cards(self.community_cards)
        print("Your cards are:")
        self.print_cards(self.player_hand)
        if not self.made_bet:
            print("Your options:")
            print("1) Bet 1x")
            print("2) Fold")
            answer = int(input())
            while answer != 1 and answer != 2:
                print("Please input a valid answer")
                print("Your options:")
                print("1) Bet 1x")
                print("2) Fold")
                answer = int(input())
            if answer == 1:
                self.set_play_bet(1)
                self.made_bet = True
                print("You have made a 1x bet on play.")
            elif answer == 2:
                print("Folding")
                self.fold()

        if not self.folded:
            self.showdown()

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