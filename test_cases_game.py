"""Test cases for all modules stored
Mainly created by honkyrot
Make sure to install the package 'pytest' first!
Does not use the 'unittest' module.
Python Version 3.11
test_cases_game.py version v1.2
"""

import pytest  # Import pytest, the test framework
from UNO_AI_Module import AI_Module
from UNO_Core import UNO_Game
import UNO_Deck_Module as udm

"""UNO_AI_Module.py Tests, for AI functions"""


@pytest.fixture()
def ai_module():
    """Fixture"""
    return AI_Module(udm.cpu1)


def test_AI_always_select_plus_four_wild(ai_module):
    """Always picks the +4 card with set hand."""
    ai_module.current_color = "blue"  # Overwrite color
    ai_module.showing_number = 0
    local_deck = [udm.Card("green", 2),
                  udm.Card("green", 2),
                  udm.Card("green", 2),
                  udm.Card("green", 2),
                  udm.Card("green", 2),
                  udm.Card("green", 2),
                  udm.Card("wild", "+4")]
    ai_module.ai_hand = local_deck
    selected_card = ai_module.make_choice()
    assert selected_card["color"] == "wild"
    assert selected_card["value"] == "+4"


def test_AI_always_select_plus_4_wild_with_wild(ai_module):
    """Always picks the +4 card over the wild."""
    ai_module.current_color = "blue"  # Overwrite color
    ai_module.showing_number = 0
    local_deck = [udm.Card("green", 2),
                  udm.Card("green", 2),
                  udm.Card("green", 2),
                  udm.Card("green", 2),
                  udm.Card("green", 2),
                  udm.Card("wild", "wild"),
                  udm.Card("wild", "+4")]
    ai_module.ai_hand = local_deck
    selected_card = ai_module.make_choice()
    assert selected_card["color"] == "wild"
    assert selected_card["value"] == "+4"


def test_AI_always_select_wild(ai_module):
    """Always picks the wild."""
    ai_module.current_color = "blue"  # Overwrite color
    ai_module.showing_number = 0
    local_deck = [udm.Card("green", 2),
                  udm.Card("green", 2),
                  udm.Card("yellow", 4),
                  udm.Card("green", 2),
                  udm.Card("green", 2),
                  udm.Card("wild", "wild"),
                  udm.Card("red", 3)]
    ai_module.ai_hand = local_deck
    selected_card = ai_module.make_choice()
    assert selected_card["color"] == "wild"
    assert selected_card["value"] == "wild"


def test_AI_select_blue_over_wild(ai_module):
    """Always picks the blue card over the wild."""
    ai_module.current_color = "blue"  # Overwrite color
    ai_module.showing_number = 0
    local_deck = [udm.Card("green", 2),
                  udm.Card("green", 2),
                  udm.Card("blue", 4),
                  udm.Card("green", 2),
                  udm.Card("green", 2),
                  udm.Card("wild", "wild"),
                  udm.Card("red", 3)]
    ai_module.ai_hand = local_deck
    selected_card = ai_module.make_choice()
    assert selected_card["color"] == "blue"
    assert selected_card["value"] == 4


def test_AI_select_blue_plus_two(ai_module):
    """Always picks the blue +2."""
    ai_module.current_color = "blue"  # Overwrite color
    ai_module.showing_number = 0
    local_deck = [udm.Card("blue", "+2"),
                  udm.Card("green", 2),
                  udm.Card("blue", 4),
                  udm.Card("green", 2),
                  udm.Card("green", 2),
                  udm.Card("wild", "wild"),
                  udm.Card("red", 3)]
    ai_module.ai_hand = local_deck
    selected_card = ai_module.make_choice()
    assert selected_card["color"] == "blue"
    assert selected_card["value"] == "+2"


def test_AI_select_number_yellow_only(ai_module):
    """Always picks the yellow 7 card."""
    ai_module.current_color = "yellow"  # Overwrite color
    ai_module.showing_number = 0
    local_deck = [udm.Card("blue", "+2"),
                  udm.Card("green", 2),
                  udm.Card("blue", 4),
                  udm.Card("green", 2),
                  udm.Card("yellow", 7),
                  udm.Card("wild", "wild"),
                  udm.Card("red", 3)]
    ai_module.ai_hand = local_deck
    selected_card = ai_module.make_choice()
    assert selected_card["color"] == "yellow"
    assert selected_card["value"] == 7


def test_AI_select_skip_yellow_only(ai_module):
    """Always picks the yellow skip card."""
    ai_module.current_color = "yellow"  # Overwrite color
    ai_module.showing_number = 0
    local_deck = [udm.Card("blue", "+2"),
                  udm.Card("green", 2),
                  udm.Card("yellow", "skip"),
                  udm.Card("yellow", "reverse"),
                  udm.Card("yellow", 7),
                  udm.Card("wild", "wild"),
                  udm.Card("red", 3)]
    ai_module.ai_hand = local_deck
    selected_card = ai_module.make_choice()
    assert selected_card["color"] == "yellow"
    assert selected_card["value"] == "skip"


def test_AI_select_wild_plus_4_card_only(ai_module):
    """Always picks the wild +4 card even with wilds and actions."""
    ai_module.current_color = "red"  # Overwrite color
    ai_module.showing_number = 0
    local_deck = [udm.Card("blue", "+2"),
                  udm.Card("green", 2),
                  udm.Card("yellow", "skip"),
                  udm.Card("wild", "wild"),
                  udm.Card("yellow", 7),
                  udm.Card("wild", "+4"),
                  udm.Card("blue", 3)]
    ai_module.ai_hand = local_deck
    selected_card = ai_module.make_choice()
    assert selected_card["color"] == "wild"
    assert selected_card["value"] == "+4"


def test_AI_draw_card(ai_module):
    """Draws a card. 3 Cards"""
    ai_module.current_color = "red"  # Overwrite color
    ai_module.showing_number = 0
    local_deck = [udm.Card("blue", "+2"),
                  udm.Card("green", 2),
                  udm.Card("yellow", "skip")]
    ai_module.ai_hand = local_deck
    selected_card = ai_module.make_choice()
    assert selected_card == "Draw card"


def test_AI_pick_same_number_different_color_card(ai_module):
    """Draws a card that's not the same color, BUT has the same number."""
    ai_module.current_color = "yellow"  # Overwrite color
    ai_module.showing_number = 4
    local_deck = [udm.Card("blue", "+2"),
                  udm.Card("green", 2),
                  udm.Card("red", 4)]
    ai_module.ai_hand = local_deck
    selected_card = ai_module.make_choice()
    assert selected_card["color"] == "red"
    assert selected_card["value"] == 4


def test_AI_pick_plus_four_over_wild(ai_module):
    """Picks a +4 over 1 wild with a deck of all wilds."""
    ai_module.current_color = "yellow"  # Overwrite color
    ai_module.showing_number = 4
    local_deck = [udm.Card("wild", "+4"),
                  udm.Card("wild", "+4"),
                  udm.Card("wild", "+4"),
                  udm.Card("wild", "wild"),
                  udm.Card("wild", "+4")]
    ai_module.ai_hand = local_deck
    selected_card = ai_module.make_choice()
    assert selected_card["color"] == "wild"
    assert selected_card["value"] == "+4"


def test_AI_pick_plus_four_over_wild_with_action(ai_module):
    """Picks a wild same color over a +4 with a deck of all wilds."""
    ai_module.current_color = "yellow"  # Overwrite color
    ai_module.showing_number = 4
    local_deck = [udm.Card("wild", "+4"),
                  udm.Card("wild", "+4"),
                  udm.Card("wild", "+4"),
                  udm.Card("yellow", "skip"),
                  udm.Card("wild", "wild"),
                  udm.Card("wild", "wild"),
                  udm.Card("green", "reverse"),
                  udm.Card("wild", "+4")]
    ai_module.ai_hand = local_deck
    selected_card = ai_module.make_choice()
    assert selected_card["color"] == "yellow"
    assert selected_card["value"] == "skip"


def test_AI_picks_plus_four_on_action_discard(ai_module):
    """Picks a +4 when there is an action card on the discard pile."""
    ai_module.current_color = "green"  # Overwrite color
    ai_module.showing_number = "skip"  # action card
    local_deck = [udm.Card("wild", "+4"),
                  udm.Card("wild", "wild")]
    ai_module.ai_hand = local_deck
    selected_card = ai_module.make_choice()
    assert selected_card["color"] == "wild"
    assert selected_card["value"] == "+4"


def test_AI_picks_color_card_on_action_discard(ai_module):
    """Picks a +2 same-color action when there is an action card on the discard pile."""
    ai_module.current_color = "green"  # Overwrite color
    ai_module.showing_number = "skip"  # action card
    local_deck = [udm.Card("green", "+2"),
                  udm.Card("green", 6)]
    ai_module.ai_hand = local_deck
    selected_card = ai_module.make_choice()
    assert selected_card["color"] == "green"
    assert selected_card["value"] == "+2"


def test_AI_picks_wild_over_same_number_card(ai_module):
    """Picks a wild over same numbered card"""
    ai_module.current_color = "green"  # Overwrite color
    ai_module.showing_number = 5  # action card
    local_deck = [udm.Card("wild", "wild"),
                  udm.Card("blue", 5)]
    ai_module.ai_hand = local_deck
    selected_card = ai_module.make_choice()
    assert selected_card["color"] == "wild"
    assert selected_card["value"] == "wild"


"""UNO_Deck_Module.py tests"""


@pytest.fixture
def deck_module():
    """Fixture for the deck module."""
    udm.deck.clear()
    return udm


def test_deck_should_have_108_cards(deck_module):
    """The deck should have 108 cards."""
    deck_module.create_deck()
    assert len(deck_module.deck) == 108


def test_deck_cpu_should_have_7_cards(deck_module):
    """CPU should have 7 cards."""
    deck_module.create_deck()
    local_cpu = udm.CPU1()
    local_cpu.create_hand()
    assert len(local_cpu.hand) == 7


def test_deck_should_have_80_cards_after_dealing(deck_module):
    """The deck should have 80 cards after dealing."""
    deck_module.create_deck()
    local_cpu1 = udm.CPU1()
    local_cpu1.create_hand()
    local_cpu2 = udm.CPU2()
    local_cpu2.create_hand()
    local_cpu3 = udm.CPU3()
    local_cpu3.create_hand()
    local_p1 = udm.Player()
    local_p1.create_hand()
    assert len(deck_module.deck) == 80


def test_deck_pass_4_cards_to_cpu(deck_module):
    """Pass 4 cards to CPU. Deck should have 97 (108-7-4) cards."""
    deck_module.create_deck()
    local_cpu = udm.CPU1()
    local_cpu.create_hand()
    deck_module.draw_cards(local_cpu, 4)
    assert len(local_cpu.hand) == 11
    assert len(deck_module.deck) == 97


def test_deck_pass_40_cards_to_cpu(deck_module):
    """Pass 40 cards to CPU, large volume test. Deck should have 97 (108-7-40) cards."""
    deck_module.create_deck()
    local_cpu = udm.CPU1()
    local_cpu.create_hand()
    deck_module.draw_cards(local_cpu, 40)
    assert len(local_cpu.hand) == 47
    assert len(deck_module.deck) == 61


def test_deck_create_two_decks(deck_module):
    """Create 2 decks. Should have 216 cards."""
    deck_module.create_deck()
    deck_module.create_deck()
    assert len(deck_module.deck) == 216


def test_deck_create_x10_decks(deck_module):
    """Create x10 decks. Should have 1080 cards."""
    for i in range(10):
        deck_module.create_deck()
    assert len(deck_module.deck) == 1080


def test_deck_create_x100_decks(deck_module):
    """Create x100 decks. Should have 10800 cards."""
    for i in range(100):
        deck_module.create_deck()
    assert len(deck_module.deck) == 10800


"""UNO_Core.py tests"""


@pytest.fixture
def core_module():
    """Fixture for the core module."""
    udm.deck.clear()
    return UNO_Game()


def test_core_start_up_check(core_module):
    """Check all variables are set to default values."""
    assert core_module.overall_turn == 0
    assert core_module.current_turn == 0
    assert core_module.current_game == 0
    assert core_module.actions_played == 0
    assert core_module.game_ended is False
    assert core_module.winner is None


def test_core_active_variables_check(core_module):
    """Check all hot variables are set to default values."""
    assert core_module.playing_player == core_module.player0
    assert core_module.playing_player_number == 0
    assert core_module.clockwise is True
    assert core_module.current_color is None
    assert core_module.current_card is None
    assert core_module.round_skipped is False


def test_core_loopback_clockwise(core_module):
    """Test the loopback on core module, should go from 3 to 0, incrementing by 1"""
    core_module.playing_player_number = 3
    new_id = core_module.four_loopback(core_module.playing_player_number, 1)
    assert new_id == 0


def test_core_loopback_counter_clockwise(core_module):
    """Test the loopback on core module, should go from 3 to 2, decrementing by 1"""
    core_module.playing_player_number = 3
    core_module.clockwise = False
    new_id = core_module.four_loopback(core_module.playing_player_number, 1)
    assert new_id == 2


def test_core_loopback_counter_clockwise_0_to_3(core_module):
    """Test the loopback on core module, should go from 0 to 3, decrementing by 1"""
    core_module.playing_player_number = 0
    core_module.clockwise = False
    new_id = core_module.four_loopback(core_module.playing_player_number, 1)
    assert new_id == 3


def test_core_return_assignment_on_cpu1(core_module):
    """Test the return assignment on core module, should return CPU1"""
    core_module.playing_player_number = 1
    new_player = core_module.return_assignment(core_module.playing_player_number)
    assert new_player == core_module.player1


def test_core_return_assignment_cpu2_loopback(core_module):
    """Test the return assignment on core module while using the loopback function, should return CPU2"""
    core_module.playing_player_number = 1
    new_id = core_module.four_loopback(core_module.playing_player_number, 1)
    new_player = core_module.return_assignment(new_id)
    assert new_player == core_module.player2


def test_core_if_card_can_be_played_card_true(core_module):
    """Checks if a card can be played. Should return True"""
    synthetic_card = udm.Card("blue", 5)
    core_module.current_card = synthetic_card
    matching_card = udm.Card("blue", 8)
    assert core_module.check_if_card_can_be_played(matching_card) is True


def test_core_if_card_can_be_played_card_false(core_module):
    """Checks if a card can be played. Should return False"""
    synthetic_card = udm.Card("blue", 2)
    core_module.current_card = synthetic_card
    matching_card = udm.Card("yellow", 8)
    assert core_module.check_if_card_can_be_played(matching_card) is False


def test_core_card_can_be_played_card_true_wild(core_module):
    """Checks if a card can be played. Wilds should ALWAYS return True"""
    synthetic_card = udm.Card("red", "+2")
    core_module.current_card = synthetic_card
    matching_card = udm.Card("wild", "wild")
    assert core_module.check_if_card_can_be_played(matching_card) is True


def test_core_next_turn(core_module):
    """Test if the next turn is correctly assigned."""
    core_module.playing_player_number = 0
    core_module.next_turn()
    assert core_module.playing_player_number == 1


def test_core_draw_cards_cpu1(core_module):
    """Draw cards on UNO_Core.py, CPU1. 4 Cards to draw, should have 11 in hand."""
    core_module.playing_player = core_module.player1
    core_module.draw_card(core_module.player1, 4)
    assert len(core_module.playing_player.hand) == 11


def test_core_draw_cards_cpu1_negative(core_module):
    """Draw negative amount of cards, should raise ValueError."""
    with pytest.raises(ValueError):
        core_module.draw_card(core_module.player1, -1)


def test_core_draw_cards_cpu1_zero(core_module):
    """Draw no cards (somehow), should raise ValueError."""
    with pytest.raises(ValueError):
        core_module.draw_card(core_module.player1, 0)


def test_core_draw_cards_cpu1_string(core_module):
    """Draw a 'string', should raise TypeError."""
    with pytest.raises(TypeError):
        core_module.draw_card(core_module.player1, "string")


def test_core_play_card_cpu1(core_module):
    """Play a card with same functions from gameplay on CPU1, hand should have 6 cards
    after they play a card from their hand, which should start with 7."""
    core_module.playing_player = core_module.player1
    core_module.play_card(core_module.player1, core_module.player1.hand[0])
    assert len(core_module.playing_player.hand) == 6


def test_core_new_deck(core_module):
    """New deck is created with this function however
    this calls from the UNO_Core.py script
    after the cards are played it will
    refill the deck with 188 cards."""
    core_module.new_deck()
    assert len(core_module.deck) == 188
