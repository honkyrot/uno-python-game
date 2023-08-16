"""AI Core module backend.
Import this as ai_module_core
by Honkyrot
v1.3

Module will select a card and return it to the calling function.

Player decisions. Not controlled by this module.

AI decisions
If AI does not have card compatible in hand, draw ONCE and move to next player.
If AI does have a compatible card. Play the card.
    Action Card Order >
        first in list goes first!
    Highest Priority Cards >
        If they don't have the color while having an +4, play +4.
        Action cards first if color match or action match.
    High Priority Cards >
        If +2 card in hand matches color or played +2 card, play it.
    Medium Priority Cards >
        If any card in hand does not match, play wild card.
    Low Priority Cards >
        Any number face card.
        Any color matching card.
    Lowest Priority >
        Draw card

Win condition.
You have no cards.
This module does not check for a win condition.

HOW TO USE:
Import this module and have the class AI_Module ready.
Once called, call the AI_Module with the CPU class from the 'UNO_Deck_Module.py' module.
Call this with

UNO_AI_Module(UNO_Deck_Module.CPU1)

This module will select the best card and return the card as this format
{"color": "green", "value": 6} or
{"color": "wild", "value": "wild"} or
{"color": "wild", "value": "+4"} or
{"color": "red", "value": 9} or
{"color": "yellow", "value": 2} or
{"color": "blue", "value": "skip"}

Use these formats to change the game and so on. PLEASE REMEMBER that this module only
selects the card to return and does not do any game mechanics what-so-ever.
"""

import UNO_Deck_Module as deck


class AI_Module:
    def __init__(self, ai_id: deck.Player):
        self.ai = ai_id
        self.ai_hand = ai_id.hand
        self.current_hand = []
        self.wild_check = False
        self.action_check = False
        self.action_type = {"skip": False, "reverse": False, "+2": False}
        self.color_check = {"red": False, "green": False, "blue": False, "yellow": False}
        self.current_color = None
        self.showing_number = None

        self.drew_card = False

    def game_set_color(self, color: str, card_number: int) -> None:
        """Set current game color, dependent on other scripts."""
        self.current_color = color.lower()
        self.showing_number = card_number

    def _card_actions(self) -> None:
        """Picks the card to play"""
        for grabbed_cards in self.ai_hand:
            self.current_hand.append({"color": grabbed_cards.color, "value": grabbed_cards.value})
        for index1, cards in enumerate(self.current_hand):  # Check if color is in hand
            if cards["color"] in list(self.color_check.keys()):
                self.color_check.update({cards["color"]: True})
            if cards["color"] == "wild":
                self.wild_check = True
        person_no_color = self._check_all_did_not_match()
        self._check_action_cards()
        #        print("Current Hand: ", self.current_hand)
        # print(f"Color Check: {self.color_check}"  # debug line
        #       f"\nAction Types: {self.action_type}"  # debug line
        #       f"\nAction Check: {self.action_check}"  # debug line
        #       f"\nWild Check: {self.wild_check}"  # debug line
        #       f"\nCurrent Game Color: {self.current_color}"  # debug line
        #       f"\nCurrent Showing Number: {self.showing_number}")  # debug line
        if person_no_color:  # Check if AI does not have any color.
            if self.wild_check:  # Play only remaining wild card if you have no color.
                selected_card = self._play_wild_plus_four() or self._play_wild()
                # print("RETURN -1- DEBUG")
                return selected_card
            else:
                raise f"{self.ai} does not have any compatible cards!"
        else:
            current_color = self.current_color
            has_color = self._check_if_AI_has_color(current_color)
            if has_color != self.current_color and self.wild_check:  # If card selected does not match current color.
                if self.wild_check:  # Play any other wild card as high priority.
                    selected_card = self._play_wild_plus_four() or self._play_wild()
                    # print("RETURN -2- DEBUG")
                    return selected_card
            if has_color:  # Get wild card if color matches as high priority
                selected_card = self._pick_action_card(current_color)
                if selected_card:  # Finds an action card.
                    # print("RETURN -3- DEBUG")
                    return selected_card
                else:  # If it cant find an action card.
                    # print("RETURN -4- DEBUG")
                    return self._get_random_card(current_color)
            if self.wild_check:  # Play any other wild card as high priority.
                selected_card = self._play_wild() or self._play_wild_plus_four()
                # print("RETURN -5- DEBUG")
                return selected_card
            # print("RETURN -6- DEBUG")
            return self._get_same_number_card() or self.draw_card()

    def _check_all_did_not_match(self) -> bool:
        """Returns True if player does not have any color."""
        any_fail = True
        for key, data in self.color_check.items():
            if data:
                any_fail = False
        return any_fail

    def _get_same_number_card(self) -> dict or str:
        """Get a card that nots the same color but has the same number.
        NOTE: This must change the game color to the new card color."""
        for i, data in enumerate(self.current_hand):
            if data["value"] == self.showing_number and data["color"] != self.current_color:
                # print("RETURN _get_same_number_card -1- DEBUG")
                return data
        self.drew_card = True
        # print("RETURN _get_same_number_card -2- DEBUG")
        return "Draw card"

    def draw_card(self) -> str:
        """Draw a card from the deck."""
        self.drew_card = True
        return "Draw card"

    def _get_random_card(self, color: str) -> dict or str:
        """Get a random card, general gameplay"""
        for i, data in enumerate(self.current_hand):
            try:
                int_value = int(data["value"])
            except ValueError:
                int_value = False
            if data["color"] == color and int_value:
                data["value"] = int_value
                # print("RETURN _get_random_card -1- DEBUG")
                return data
        # print("RETURN _get_random_card -2- DEBUG")
        return self._get_same_number_card()

    def _pick_action_card(self, color: str) -> dict or bool:
        """Select an action card"""
        for i, data in enumerate(self.current_hand):
            if data["value"] == "+2" and data["color"] == color:
                return data
            elif data["value"] == "reverse" and data["color"] == color:
                return data
            elif data["value"] == "skip" and data["color"] == color:
                return data
        return False

    def _check_if_AI_has_color(self, color: str) -> bool:
        """Check if AI has matching color to the games color"""
        for key, data in self.color_check.items():
            if color == key and data:
                return key
        return False

    def _check_action_cards(self) -> None:
        """Check if AI has any action card in its hand"""
        for i, data in enumerate(self.current_hand):
            if data["value"] == "reverse":
                self.action_type.update({"reverse": True})
            elif data["value"] == "skip":
                self.action_type.update({"skip": True})
            elif data["value"] == "+2":
                self.action_type.update({"+2": True})

    def _play_wild_plus_four(self) -> dict:
        """Select a +4"""
        for i, data in enumerate(self.current_hand):
            if data["color"] == "wild" and data["value"] == "+4":
                return data

    def _play_wild(self) -> dict:
        """Select a  Wild Card"""
        for i, data in enumerate(self.current_hand):
            if data["color"] == "wild" and data["value"] == "wild":
                return data

    def make_choice(self) -> dict or str:
        """ONLY Call this along with game_set_color to make the AI play a card"""
        card = self._card_actions()
        if card is None:
            print(f"ERROR: AI card from {self.ai.user_name} is None!")
        return card


'''
tst = AI_Module(deck.CPU2)
tst.game_set_color("yellow")
print(tst.card_actions())
'''
