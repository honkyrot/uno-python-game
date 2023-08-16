import random

colors = ["red", "blue", "yellow", "green"]
# below, first list is values, second list is how many of the card to have
values = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
          [1, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
action_values = ["reverse", "skip", "+2"]
wild_values = ["wild", "+4"]

deck = []
discard_pile = []


class Player:
    score = 0
    user_name = "player"

    def __init__(self):
        self.hand = []

    def create_hand(self):
        draw_cards(self, 7)

    def print_hand(self):
        print("Your Hand:")
        for card in range(len(self.hand)):
            print(f"{self.hand[card].color.title()} {self.hand[card].value}")
        print("\t")


class CPU1:
    score = 0
    user_name = "CPU_1"

    def __init__(self):
        self.hand = []

    def create_hand(self):
        draw_cards(self, 7)

    def print_hand(self):
        print("CPU1's Hand:")
        for card in range(len(self.hand)):
            print(f"{self.hand[card].color.title()} {self.hand[card].value}")
        print("\t")


class CPU2:
    score = 0
    user_name = "CPU_2"

    def __init__(self):
        self.hand = []

    def create_hand(self):
        draw_cards(self, 7)

    def print_hand(self):
        print("CPU2's Hand:")
        for card in range(len(self.hand)):
            print(f"{self.hand[card].color.title()} {self.hand[card].value}")
        print("\t")


class CPU3:
    score = 0
    user_name = "CPU_3"

    def __init__(self):
        self.hand = []

    def create_hand(self):
        draw_cards(self, 7)

    def print_hand(self):
        print("CPU3's Hand:")
        for card in range(len(self.hand)):
            print(f"{self.hand[card].color.title()} {self.hand[card].value}")
        print("\t")


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value


def create_deck():
    # color num cards
    for color in colors:
        for x in range(len(values[0])):
            for y in range(values[1][x]):
                value = values[0][x]
                deck.append(Card(color, value))
        # color action cards
        for x in range(len(action_values)):
            value = action_values[x]
            for y in range(2):
                deck.append(Card(color, value))
    # wild cards
    color = "wild"
    for x in range(len(wild_values)):
        value = wild_values[x]
        for y in range(4):
            deck.append(Card(color, value))


player = Player()
cpu1 = CPU1()
cpu2 = CPU2()
cpu3 = CPU3()


def setup():
    """creates deck and player hands"""
    create_deck()
    player.create_hand()
    cpu1.create_hand()
    cpu2.create_hand()
    cpu3.create_hand()


def draw_cards(user, amount=1):
    """given specified player and number, will give number of random cards to
    player and remove the cards from the main deck"""
    for i in range(amount):
        drawn_card = deck.pop(random.randrange(0, len(deck)))
        user.hand.append(drawn_card)

# setup()

# for testing purposes, uncomment below
# player.print_hand()
# CPU1.print_hand()
# CPU2.print_hand()
# CPU3.print_hand()
# for card in deck:
#     print(f"{card.color.title()} {card.value}")

# main game functions
