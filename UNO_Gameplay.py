"""Created by HonkyRot
This is the UNO_Gameplay script for the gameplay.
This will run all player inputs and actions.
v1.0
"""
import random
import time
import UNO_Core
import UNO_Intro
from Call_Uno_TImer import call_uno_timer
from UNO_AI_Module import AI_Module

time_delay = 1


class Card:
    """Creates a dummy card to convert dictionary to object."""

    def __init__(self, color, value):
        self.color = color
        self.value = value


def clamp(num, min_value, max_value):
    """Clamps a number between a minimum and maximum value."""
    return max(min(num, max_value), min_value)


def y_n_response(input_message):
    """Returns True or False for y and n. This forces the user to only respond with y or n."""
    while True:
        user_input = input(input_message)
        if user_input.lower() == "y" or user_input.lower() == "yes":
            return True
        elif user_input.lower() == "n" or user_input.lower() == "no":
            return False
        else:
            print("Please enter either y or n!")


def forced_number_response_custom(input_message, max_number):
    """Returns a number from the user. This forces the user to only respond with a number.
    With the maximum number being the amount of cards in hand.
    Exceptions are made for the user to type in 's' to sort, etc."""
    while True:
        try:
            user_input = input(input_message)
            # custom input here
            user_input = abs(int(user_input))
            if user_input <= max_number:
                return user_input
            else:
                print("Please enter a number that is less than or equal to the amount of cards in your hand!\n")
        except ValueError:
            print("Please enter a number!")


play_uno_start = y_n_response("Do you want to play UNO?\n>")
if play_uno_start:  # Start game here, if user wants to play.
    UNO_Intro.start()
    game_active = True
    game_count = 0
    player_name = input("What would your username be?\n>")
    while True:
        try:
            game_speed = int(input("How fast do you want the game to be? (1 slow-5 fast)\n>"))
            game_speed = clamp(game_speed, 1, 5)
            print(f"\nGame speed set to {game_speed}!")
            time_delay = 5 / game_speed
            break
        except ValueError:
            print("Please enter a number!")
    while game_active:
        uno_game = UNO_Core.UNO_Game()
        uno_game.player0.user_name = player_name
        uno_game.draw_first_card()
        time.sleep(time_delay)
        while not uno_game.game_ended:
            uno_game.overall_turn += 1
            if uno_game.clockwise:
                uno_game.current_turn += 1  # Increment turn counter
            else:
                uno_game.current_turn -= 1  # Decrement turn counter
            print(f"Turn {uno_game.overall_turn}")
            time.sleep(time_delay/3)
            uno_game.display_last_card_up()
            time.sleep(time_delay/3)
            current_turn = abs((uno_game.current_turn - 1) % 4)  # Get current turn assigned to player
            if current_turn == 0:  # If its player's turn.
                print(f"It is your turn!")
                print("Please select a card to play.")
                has_selected_card = False
                while not has_selected_card:
                    uno_game.playing_player = uno_game.player0
                    uno_game.display_game_status()
                    time.sleep(time_delay/3)
                    print(f"Your current hand: ")
                    uno_game.display_your_player_hand()
                    player_response = forced_number_response_custom("Please enter the number of the card you want to play.\n"
                                                                    "Type [0] to draw a card!\n>",
                                                                    len(uno_game.player0.hand))
                    if player_response == 0:  # If player wants to draw a card.
                        uno_game.draw_card(uno_game.player0, 1)
                        if uno_game.player0.hand[-1].value == "wild":
                            print(f"You drew a {uno_game.player0.hand[-1].color.title()} card!")
                        else:
                            print(
                                f"You drew a {uno_game.player0.hand[-1].color.title()} {uno_game.player0.hand[-1].value}!")
                        has_selected_card = True
                    else:  # If any other card is selected.
                        card_play_check = uno_game.check_if_card_can_be_played(
                            uno_game.player0.hand[player_response - 1])
                        if card_play_check:
                            print("Playing card...",
                                  f"{uno_game.player0.hand[player_response - 1].color.title()} "
                                  f"{uno_game.player0.hand[player_response - 1].value if uno_game.player0.hand[player_response - 1].value != 'wild' else 'card'}")
                            uno_game.play_card(uno_game.player0, uno_game.player0.hand[player_response - 1])
                            has_selected_card = True
                            if len(uno_game.player0.hand) == 1:
                                call = call_uno_timer()
                                if call:
                                    pass
                                else:
                                    uno_game.draw_card(uno_game.player0, 2)
                        else:
                            print("You can't play that card!")
                            uno_game.display_last_card_up()
                            continue
                    time.sleep(time_delay/2)
            elif current_turn != 0:  # CPUs turn
                uno_game.playing_player = None
                if current_turn == 1:
                    uno_game.playing_player = uno_game.player1
                elif current_turn == 2:
                    uno_game.playing_player = uno_game.player2
                elif current_turn == 3:
                    uno_game.playing_player = uno_game.player3
                print(f"It is {uno_game.playing_player.user_name}'s turn!\n"
                      f"They have about {len(uno_game.playing_player.hand)} cards left in their hand.\n",
                      f"{uno_game.playing_player.user_name} is thinking...")
                time.sleep(time_delay)
                ai_module = AI_Module(uno_game.playing_player)
                ai_module.game_set_color(uno_game.current_color, uno_game.current_card.value)
                ai_card = ai_module.make_choice()
                # print(uno_game.display_your_player_hand())
                if ai_card is None:
                    print(f"ERROR: AI card from {uno_game.playing_player.user_name} is None!")
                if ai_card and ai_card != "Draw card":
                    _temp_value = ai_card["value"]
                    if ai_card["value"] == "wild":
                        _temp_value = "card"
                    print(f"{uno_game.playing_player.user_name} Played a card!", ai_card["color"].title(), _temp_value)
                    converted_card = Card(ai_card["color"].lower(), ai_card["value"])
                    card_check = uno_game.check_if_card_can_be_played(converted_card)
                    if card_check:
                        uno_game.play_card(uno_game.playing_player, converted_card)
                        if len(uno_game.playing_player.hand) == 1:
                            time.sleep(time_delay/2)
                            rng_chance = random.randint(1, 100)
                            if rng_chance > 90:  # If above 90, fail to call uno.
                                uno_game.draw_card(uno_game.playing_player, 2)
                                print(f"{uno_game.playing_player.user_name} forgot to call UNO!")
                            else:
                                print(f"{uno_game.playing_player.user_name} called UNO!")
                            time.sleep(time_delay/2)
                    else:
                        print("ERROR: AI card can't be played! Possible bug in AI_Module!",
                              "Drawing card to prevent game from crashing...")
                        uno_game.draw_card(uno_game.playing_player)
                        confirm_user_continue = input("\nPress enter to continue...\n")
                else:
                    print(f"{uno_game.playing_player.user_name} has decided to draw a card!")
                    uno_game.draw_card(uno_game.playing_player)
            print("\nNext turn!\n")
            wait = input("Press enter to continue...")
            time.sleep(time_delay/2)  # Wait x seconds before next turn.
            uno_game.next_turn()
            game_active = not uno_game.game_ended
        print("Game ended.")
        print(f"Game lasted {uno_game.overall_turn} turns.")
        print(f"Player {uno_game.winner.user_name} won!")
        time.sleep(time_delay)
        print(f"Everyone's final hands: ")
        for player in uno_game.players:
            if player.user_name != uno_game.winner.user_name:
                uno_game.display_your_player_hand(player)
            else:
                print(f"{player.user_name} hand: [empty]")
        time.sleep(time_delay)
print("Goodbye!")
