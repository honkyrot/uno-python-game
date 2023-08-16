import random

colors = ["red", "blue", "yellow", "green"]
# below, first list is values, second list is how many of the card to have
values = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
          [1, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
action_values = ["reverse", "skip", "+2"]
wild_values = ["wild", "+4"]

deck = []
discard_pile = []

class BasePlayer:
    score = 0
    user_name = "BasePlayer"
    print_string = "BasePlayer's Hand:"
    hand = []
    
    
    def __str__(self) -> str:
        return self.user_name
    
    def create_hand(self) -> None:
        draw_cards(self, 7)
    
    def print_hand(self) -> None:
        print(self.print_string)
        for card in self.hand:
            print(f"{card.color.title()} {card.value}")
        print("\t")

#individual subclasses that inherit from the base class and only have to change user_name    

class Player(BasePlayer):
    user_name = "Player"
    print_string = "Your Hand:"


class CPU1(BasePlayer):
    user_name = "CPU1"
    print_string = "CPU1's Hand:"
    
    def __str__(self) -> str:
        return super().__str__()

class CPU2(BasePlayer):
    user_name = "CPU2"
    print_string = "CPU2's Hand:"

class CPU3(BasePlayer):
    user_name = "CPU3"
    print_string = "CPU3's Hand:"





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
