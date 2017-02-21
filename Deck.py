import Card
import itertools

class Deck:
    def __init__(self):
        self.cards = []

        # Generates all possible cartesian products between A-K and CDHS
        prod = [card for card in itertools.product((range(2, 15)), ['C', 'D', 'H', 'S'])]

        for card in prod:
            c = Card(card[0], card[1])
            self.cards.append(Card(card[0], card[1]))

        random.shuffle(self.cards)

    # Pops a card from the top of the deck and returns it
    def draw(self):
        card = self.cards.pop(0)
        return card
