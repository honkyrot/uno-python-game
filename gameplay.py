import UNO_Deck_Module
import time


# the commit author is not always accurate due to a bug


def game_setup():
    # INSERT WELCOME SCREEN HERE
    plr_count = input("How many players would you like [2-4]? ")
    if plr_count == "2":
        print("You've chosen 2 players.")
        uno = Game(1)
        uno.setup_players()
        uno.create_hands()
        uno.gameplay()
    elif plr_count == "3":
        print("You've chosen 3 players.")
        uno = Game(2)
        uno.setup_players()
        uno.create_hands()
        uno.gameplay()
    elif plr_count == "4":
        print("You've chosen 4 players.")
        uno = Game(1)
        uno.setup_players()
        uno.create_hands()
        uno.gameplay()
    else:
        print("Can you read? Try again.")
        game_setup()


class Game:
    def __init__(self, player_count):
        self.player_count = player_count
        UNO_Deck_Module.create_deck()
        self.Player = deck.Player()
        self.CPU1 = UNO_Deck_Module.CPU1
        self.CPU2 = UNO_Deck_Module.CPU2
        self.CPU3 = UNO_Deck_Module.CPU3
        self.other_players = [self.CPU1, self.CPU2, self.CPU3]
        self.playing = [self.Player]  # append other players here
        self.table_color = ""
        self.table_value = ""
        self.current_player = self.Player
        self.table_clockwise = True

    def setup_players(self):
        for i in range(1, self.player_count):
            self.playing.append(self.other_players.pop())
            print(self.playing)

    def create_hands(self):
        for players in self.playing:
            players.create_hand()

    def next_plr_turn(self, plr, amt):
        print(f"{self.current_player} is now playing.")
        if amt < 2 and self.table_clockwise:
            if plr == self.Player:
                self.current_player = self.CPU1
            elif plr == self.CPU1:
                self.current_player = self.CPU2
            elif plr == self.CPU2:
                self.current_player = self.CPU3
            elif plr == self.CPU3:
                self.current_player = self.CPU1
        if amt < 2 and not self.table_clockwise:
            if plr == self.Player:
                self.current_player = self.CPU3
            elif plr == self.CPU3:
                self.current_player = self.CPU2
            elif plr == self.CPU2:
                self.current_player = self.CPU1
            elif plr == self.CPU1:
                self.current_player = self.Player

        if amt == 2 and self.table_clockwise:
            if plr == self.Player:
                self.current_player = self.CPU2
            elif plr == self.CPU1:
                self.current_player = self.CPU3
            elif plr == self.CPU2:
                self.current_player = self.CPU1
            elif plr == self.CPU3:
                self.current_player = self.CPU2
        if amt == 2 and not self.table_clockwise:
            if plr == self.Player:
                self.current_player = self.CPU3
            elif plr == self.CPU3:
                self.current_player = self.CPU2
            elif plr == self.CPU2:
                self.current_player = self.CPU1
            elif plr == self.CPU1:
                self.current_player = self.Player

    def skip(self, plr):
        self.next_plr_turn(plr, 2)

    def reverse(self, plr):
        if self.table_clockwise:
            self.table_clockwise = False
        else:
            self.table_clockwise = True
        self.next_plr_turn(plr, 1)

    def wild(self, plr, color):
        self.table_color = color
        self.next_plr_turn(plr, 1)

    def draw_two(self, plr):
        if self.table_clockwise:
            if plr == self.Player:
                UNO_Deck_Module.draw_cards(self.CPU1, 2)
            elif plr == self.CPU1:
                UNO_Deck_Module.draw_cards(self.CPU2, 2)
            elif plr == self.CPU2:
                UNO_Deck_Module.draw_cards(self.CPU3, 2)
            elif plr == self.CPU3:
                UNO_Deck_Module.draw_cards(self.Player, 2)
        if not self.table_clockwise:
            if plr == self.Player:
                UNO_Deck_Module.draw_cards(self.CPU3, 2)
            elif plr == self.CPU3:
                UNO_Deck_Module.draw_cards(self.CPU2, 2)
            elif plr == self.CPU2:
                deck.draw_cards(self.CPU1, 2)
            elif plr == self.CPU1:
                UNO_Deck_Module.draw_cards(self.Player, 2)

    def draw_four(self, plr, color):
        for i, player in enumerate(self.playing):
            if plr == player:
                if self.table_clockwise:
                    if i == 3:
                        victim = player[0]
                    else:
                        victim = player[i + 1]
                    UNO_Deck_Module.draw_cards(victim, 4)
                    self.skip(victim)
                else:
                    if i == 0:
                        victim == player[3]
                    else:
                        victim = player[i - 1]
                    UNO_Deck_Module.draw_cards(victim, 4)
                    self.skip(victim)

    def gameplay(self):
        # round cycle
        if self.current_player == self.Player:
            print("Here is your hand.")
            self.current_player.print_hand()
            choice = input("Play a card. [Press 1] \nDraw a card [Press 2] \n")
            if choice == "1":
                card = input("What card would you like to play?")
                for i in range(0, len(self.current_player.hand)):
                    color = self.current_player.hand[i].color.title()
                    value = self.current_player.hand[i].value
                    if card == f"{color} {value}":
                        print(f"Player has chosen to play {card}.")
                        self.table_color = self.current_player.hand[i].color
                        played_card = self.current_player.hand.pop(i)
                        UNO_Deck_Module.discard_pile.append(played_card)

                        if self.current_player.hand[i].value == "reverse":
                            print("Player played a Reverse Card.")
                            self.reverse(self.current_player)
                            self.next_plr_turn(self.current_player, 1)
                            self.gameplay()

                        if self.current_player.hand[i].value == "skip":
                            print("Player played a skip card.")
                            self.skip(self.current_player)
                            self.gameplay()

                        if self.current_player.hand[i].value == "+2":
                            print("Player played a plus two card.")
                            self.draw_two(self.current_player)
                            self.gameplay()

                    else:
                        self.next_plr_turn(self.current_player, 1)
                        self.gameplay()

            elif choice == "2":
                print(f"{self.current_player} has chosen to draw a card.")
                UNO_Deck_Module.draw_cards(self.current_player, 1)
                self.current_player.print_hand()
                self.next_plr_turn(self.current_player, 1)
                self.gameplay()

        if self.current_player != self.Player:
            print(f"It's {self.current_player}'s turn.")
            time.sleep(3)
            for i in range(0, len(self.current_player.hand)):
                color = self.current_player.hand[i].color
                value = self.current_player.hand[i].value
                print(self.table_color)

                if color == self.table_color or value == self.table_value:
                    card = self.current_player.hand[i].pop()
                    UNO_Deck_Module.discard_pile.append(card)
                    print(f"{self.current_player} has chosen to play {card}")
                    self.next_plr_turn(self.current_player, 1)
                    self.gameplay()

                elif self.current_player.hand[i].value == "reverse":
                    print(f"{self.current_player} played {color.title} {value}")
                    self.reverse(self.current_player)
                    self.gameplay()
                elif self.current_player.hand[i].value == "skip":
                    print(f"{self.current_player} played {color.title} {value}")
                    self.skip(self.current_player)
                    self.gameplay()

                elif self.current_player.hand[i].value == "reverse":
                    print("Player played a plus two card.")
                    print(f"{self.current_player} played {color.title} {value}")
                    self.draw_two(self.current_player)
                    self.next_plr_turn(self.current_player, 1)
                    self.gameplay()
            else:
                print(f"{self.current_player} has chosen to draw a card.")
                UNO_Deck_Module.draw_cards(self.current_player, 1)
                self.next_plr_turn(self.current_player, 1)
                self.gameplay()


game_setup()
