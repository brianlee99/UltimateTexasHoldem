class Card:
    # Aces are represented as the number 14, not as 1
    ranks = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
             11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
    suits = {'S': 'Spades', 'C': 'Clubs', 'H': 'Hearts', 'D': 'Diamonds'}

    def __init__(self, r: int, s: str):
        self.rank = r
        self.suit = s
        self.name = Card.ranks[r] + ' of ' + Card.suits[s]