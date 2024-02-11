import random

class Card:
    def __init__(self, value) -> None:
        self, value = value


class Deck:
    def __init__(self) -> None:
        self.cards = []
        for value in ["Duke", "Assassin", "Ambassador", "Captain", "Contessa"]:
            for _ in range(3):
                self.cards.append(value)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def __repr__(self) -> str:
        return ' '.join([self.card for self.card in self.cards])


def main():
    deck = Deck()
    deck.shuffle()
    print(deck.draw())
    print(deck)

if __name__=='__main__':
    main()