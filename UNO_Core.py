"""This UNO_Core script will handle all gameplay activities.
This will be the main script that will be used to run the game.
sorry Uno_Rules_Actions.py, code didn't fit for me to use."""

import random
import time
import UNO_Deck_Module as UNO_Deck


class UNO_Game:
    """YOU HAVE UNO!!!!!"""

    def __init__(self) -> None:
        self.new_deck()
        self.discard_pile = []
        self.deck = UNO_Deck.deck

        self.player0 = UNO_Deck.Player()  # The actual player
        self.player1 = UNO_Deck.CPU1()  # ALL AI
        self.player2 = UNO_Deck.CPU2()
        self.player3 = UNO_Deck.CPU3()
        self.player0.create_hand()  # mildly dirty but ok.
        self.player1.create_hand()
        self.player2.create_hand()
        self.player3.create_hand()

        self.players = [self.player0, self.player1, self.player2, self.player3]

        self.overall_turn = 0
        self.current_turn = 0
        self.current_game = 0
        self.actions_played = 0
        self.game_ended = False
        self.winner = None

        self.playing_player = self.player0  # starts from player 1
        self.playing_player_number = 0
        self.clockwise = True
        self.current_color = None
        self.current_card = None
        self.round_skipped = False

    def print_cards_in_deck(self) -> None:
        print(f"Cards left in deck: {len(self.deck)}")

    def four_loopback(self, number: int, increment: int) -> int:
        """Returns the player_id number from 0 trough 3. If the increment is 1 and the number is 3, it will return 0.
        If the increment is -1 and the number is 0, it will return 3. If the game is reversed, it will do the opposite."""
        # print(f"received: {number} incrementing {increment}. "
        #      f"the game is {'clockwise' if self.clockwise else 'counter-clockwise'}")
        if self.clockwise:
            if number + increment > 3:
                new_number = 0
            elif number + increment < 0:
                new_number = 3
            else:
                new_number = number + increment
        else:
            if number - increment > 3:
                new_number = 0
            elif number - increment < 0:
                new_number = 3
            else:
                new_number = number - increment
        # print(f"returning: {new_number}\n")
        return new_number

    def return_assignment(self, number: int) -> UNO_Deck.Player:
        """Returns CPU or Player object on current number; a dirty way to do it."""
        # print(f"\n returning player assignment: {number}\n")
        if number == 0:
            return self.player0
        elif number == 1:
            return self.player1
        elif number == 2:
            return self.player2
        elif number == 3:
            return self.player3

    def print_showing_card(self) -> None:
        """Just prints the last played card"""
        print(f"Last card showing up: {self.current_card.color} {self.current_card.value}")

    def display_status(self) -> None:
        """Displays the current player status such as cards in hand and current card."""
        print(f"It is now {self.playing_player.user_name}'s turn.")
        print(f"{self.playing_player.user_name} has {len(self.playing_player.hand)} cards.")

    def display_game_status(self) -> None:
        """Displays the current game status such as cards in deck remaining."""
        print(f"Cards left in deck: {len(self.deck)}")
        print(f"Cards in discard pile: {len(self.discard_pile)}")

    def display_last_card_up(self) -> None:
        """Displays the last card up."""
        print(f"Last card showing up: {self.current_card.color.title()} {self.current_card.value}")

    def display_your_player_hand(self, override: bool = False) -> None:
        """Displays the player's (mainly you, or anyone else) hand to select and play."""
        if not override:
            for i in range(len(self.playing_player.hand)):
                _temp_value = self.playing_player.hand[i].value
                if self.playing_player.hand[i].value == "wild":
                    _temp_value = "card"
                if self.check_if_card_can_be_played(self.playing_player.hand[i]):
                    print(f"◆ [{i + 1}] {self.playing_player.hand[i].color.title()} {_temp_value}")
                else:
                    print(f"◇ [{i + 1}] {self.playing_player.hand[i].color.title()} {_temp_value}")
                time.sleep(0.2)
        else:
            print(f"{override.user_name}'s hand:")
            for i in range(len(override.hand)):
                _temp_value = override.hand[i].value
                if override.hand[i].value == "wild":
                    _temp_value = "card"
                print(f"◈ {override.hand[i].color.title()} {_temp_value}")
                time.sleep(0.2)

    def check_if_card_can_be_played(self, card: UNO_Deck.Card) -> bool:
        """Checks if the card can be played for the user to know. (UI)"""
        if card.color == "wild":  # Wild Checks
            return True
        elif card.color == self.current_card.color:
            return True
        elif card.value == self.current_card.value:
            return True
        return False

    def check_for_action(self, player: UNO_Deck.Player, card: UNO_Deck.Card) -> None:
        """Check if the card is an action card, if it is play the function
        If not play the card regularly."""
        if card.value == "skip":
            self.action_skip(player, card)
        elif card.value == "reverse":
            self.action_reverse(player, card)
        elif card.value == "+2":
            self.action_draw_two(player, card)
        elif card.value == "+4":
            self.action_draw_four_wild(player, card)
        elif card.value == "wild":
            self.action_wild(player, card)
        else:
            self.play_regular_card(player, card)

    def discard_played_card(self, player: UNO_Deck.Player, card: UNO_Deck.Card, discard: bool = True) -> None:
        """Discards a card from the player's hand."""
        self.current_card = card
        self.current_color = card.color
        if discard:
            self.discard_pile.append(card)
        # print("DISCARDED CARD: ", card.color, card.value)
        if player:
            try:
                player.hand.remove(card)
            except ValueError:
                for i, c in enumerate(player.hand):
                    if c.color == card.color and c.value == card.value:
                        player.hand.pop(i)
                        break

    def new_deck(self) -> None:
        """Creates a new deck and shuffles it."""
        UNO_Deck.create_deck()
        self.deck = UNO_Deck.deck
        random.shuffle(self.deck)

    def refill_deck(self, player: UNO_Deck.Player, remaining_amount: int) -> None:
        """Refills deck from discard pile.
        If somehow all the cards are in play and no more cards can be shuffled in,
        add a new deck of cards to be played."""
        while remaining_amount > 0 and len(self.discard_pile) > 0:
            self.deck.append(self.discard_pile.pop())
            remaining_amount -= 1
        if remaining_amount > 0 and len(self.discard_pile) == 0:
            print("\nNo cards in discard pile to refill deck."
                  "\nSurprised that you dragged the game this far."
                  "\nRefilling deck with a new set of cards."
                  "\nWill continue to keep giving you cards."
                  f"\n{player.user_name}'s remaining cards left to draw: {remaining_amount}")
            self.new_deck()
            self.draw_card(player, remaining_amount)

    def draw_card(self, player: UNO_Deck.Player, amount: int = 1) -> None:
        """Draws a card from the deck and adds it to the player's hand."""
        if amount < 1:
            raise ValueError("Amount cannot be less than 1.")
        if player:
            remaining_amount = amount
            for i in range(amount):
                if len(self.deck) == 0:
                    self.refill_deck(player, remaining_amount)
                    break
                remaining_amount -= 1
                card = self.deck.pop()
                player.hand.append(card)

    def next_turn(self) -> None:
        """Goes to the next player."""
        if not self.round_skipped:
            new_id = self.four_loopback(self.playing_player_number, 1)
            self.playing_player_number = new_id
            self.playing_player = self.return_assignment(new_id)
        for i in range(4):  # Checks if any player's hand are empty. Wins the game if it is.
            if len(self.players[i].hand) == 0:
                self.game_ended = True
                self.winner = self.players[i]
                break
        self.round_skipped = False

    def play_card(self, player: UNO_Deck.Player, selection: UNO_Deck.Card) -> None:
        """Plays a card from a player's hand in selection."""
        if selection:
            self.check_for_action(player, selection)

    def action_reverse(self, player: UNO_Deck.Player, card: UNO_Deck.Card) -> None:
        """Plays a reverse action and broadcasts the turn rotation."""
        self.discard_played_card(player, card)
        print(f"{player.user_name} played a reverse card.")
        self.round_skipped = True
        if self.clockwise:
            print("The game is now going counterclockwise.")
        else:
            print("The game is now going clockwise.")
        self.clockwise = not self.clockwise
        new_number_id = self.four_loopback(self.playing_player_number, 1)
        self.playing_player_number = new_number_id

    def action_skip(self, player: UNO_Deck.Player, card: UNO_Deck.Card) -> None:
        """Skips a players turn"""
        self.discard_played_card(player, card)
        new_number_id = self.four_loopback(self.playing_player_number, 1)
        target_player = self.return_assignment(new_number_id)
        if target_player.user_name == player.user_name:  # Reattempt to skip if the player is the same.
            new_number_id = self.four_loopback(new_number_id, 1)
            target_player = self.return_assignment(new_number_id)
        print(f"{player.user_name} used a skip card!.",
              f"Skipped {target_player.user_name}'s turn.")
        new_number_id = self.four_loopback(new_number_id, 1)
        self.playing_player_number = new_number_id
        self.round_skipped = True
        if self.clockwise:
            self.current_turn += 1
        else:
            self.current_turn -= 1

    def general_action_skip(self) -> None:
        """Skips next player without using a card, used for +2 and +4"""
        new_number_id = self.four_loopback(self.playing_player_number, 1)
        target_player = self.return_assignment(new_number_id)
        if target_player.user_name == self.return_assignment(
                self.playing_player_number):  # Reattempt to skip if the player is the same.
            new_number_id = self.four_loopback(new_number_id, 1)
            target_player = self.return_assignment(new_number_id)
        print(f"Skipped {target_player.user_name}'s turn.")
        new_number_id = self.four_loopback(new_number_id, 1)
        self.playing_player_number = new_number_id
        self.round_skipped = True
        if self.clockwise:
            self.current_turn += 1
        else:
            self.current_turn -= 1

    def action_draw_two(self, player: UNO_Deck.Player, card: UNO_Deck.Card) -> None:
        """Plays a plus two on the next player"""
        self.discard_played_card(player, card)
        new_number_id = self.four_loopback(self.playing_player_number, 1)
        target_player = self.return_assignment(new_number_id)
        print(f"{player.user_name} played a +2 card."
              f" {target_player.user_name} draws 2 cards.")
        self.draw_card(target_player, 2)
        self.general_action_skip()

    def action_draw_four_wild(self, player: UNO_Deck.Player, card: UNO_Deck.Card) -> None:
        """Plays a plus four on the next player, also skipping them"""
        new_number_id = self.four_loopback(self.playing_player_number, 1)
        target_player = self.return_assignment(new_number_id)
        print(f" {target_player.user_name} draws 4 cards.")
        self.discard_played_card(player, card)
        self.draw_card(target_player, 4)
        current_turn = abs((self.current_turn - 1) % 4)
        if current_turn == 0:  # The player picks the color
            print("Please pick a color.",
                  "\n[1] Red",
                  "\n[2] Blue",
                  "\n[3] Green",
                  "\n[4] Yellow")
            while True:
                try:
                    color = int(input("Color choice \n> "))
                    if color in range(1, 5):
                        break
                except ValueError:
                    pass
            color = ["red", "blue", "green", "yellow"][color - 1]
            card.color = color
            card.value = "+4"
            self.current_card = card
            self.current_color = color
            print(f"The color is now {color}.")
        else:  # AI picks random color.
            print(f"{player.user_name} picked a color.")
            color = random.choice(["red", "blue", "green", "yellow"])
            card.color = color
            card.value = "+4"
            self.current_card = card
            self.current_color = color
            print(f"{player.user_name} picked {color}.")
        self.general_action_skip()

    def action_wild(self, player: UNO_Deck.Player, card: UNO_Deck.Card) -> None:
        """Plays a wild card for the player."""
        self.discard_played_card(player, card)
        current_turn = abs((self.current_turn - 1) % 4)
        if current_turn == 0:  # The player picks the color
            print("Please pick a color.",
                  "\n[1] Red",
                  "\n[2] Blue",
                  "\n[3] Green",
                  "\n[4] Yellow")
            while True:
                try:
                    color = int(input("Color choice \n> "))
                    if color in range(1, 5):
                        break
                except ValueError:
                    pass
            color = ["red", "blue", "green", "yellow"][color - 1]
            card.color = color
            card.value = "wild"
            self.current_card = card
            self.current_color = color
            print(f"The color is now {color}.")
        else:  # AI picks random color.
            print(f"{player.user_name} picked a color.")
            color = random.choice(["red", "blue", "green", "yellow"])
            card.color = color
            card.value = "wild"
            self.current_card = card
            self.current_color = color
            print(f"{player.user_name} picked {color}.")

    def play_regular_card(self, player: UNO_Deck.Player, card: UNO_Deck.Card) -> None:
        """Plays a regular card for the player."""
        self.discard_played_card(player, card)

    def draw_first_card(self) -> None:
        """Dealer draws first card to show"""  # Ignore that it is dirty.
        card = self.deck.pop()
        self.discard_played_card(None, card)
        
        match card.value:
            case "wild":
                print_str = "wild"
                card.value = "wild"
            case "+4":
                print_str = "wild +4"
                card.value = "+4"
            case "reverse":
                print_str = card.color.title() + " reverse"
                self.clockwise = not self.clockwise
            case "skip":
                print_str = card.color.title() + " skip"
            case "+2":
                print_str = card.color.title() + " +2"
            case _:
                print_str = card.color.title() + " " + str(card.value)
            
        print(f"Dealer drew a {print_str} card!")
        
        if card.value in ("wild", "+4"):
            color = random.choice(["red", "blue", "green", "yellow"])
            card.color = color
            self.current_card = card
            self.current_color = color
            
            print(f"Dealer changed the color to {color.title()}!")
        
        if card.value in ("+4", "+2"):
            target_player = self.return_assignment(0)
            print(f" {target_player.user_name} draws {card.value[1]} cards.")
            self.draw_card(target_player, int(card.value[1]))
        
        if card.value != "wild": #something legacy, i guess because it was not in the original if elif chain
            self.current_turn += 1

