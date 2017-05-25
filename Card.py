import operator

class Card:
    # Aces are represented as the number 14, not as 1
    ranks_full = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
                  11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
    suits = {'S': 'Spades', 'C': 'Clubs', 'H': 'Hearts', 'D': 'Diamonds'}
    ranks_short = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
                   11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

    def __init__(self, r: int, s: str):
        self.rank = r
        self.suit = s
        self.name = Card.ranks_full[r] + ' of ' + Card.suits[s]

    def __getitem__(self, i):
        if i == 0:
            return self.rank
        elif i == 1:
            return self.suit
        else:
            raise ValueError('The index must be either 0 (rank) or 1 (suit)')

    def __repr__(self):
        return "({}, {})".format(Card.ranks_short[self.rank], self.suit)

    # TODO: a way to go card_obj[0] to get the value, and card_obj[1] to get the suit
