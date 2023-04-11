instructions = '''
Cards:
    The majority of the cards in the deck come in 4 colors:
        Red
        Blue
        Yellow
        Green'''
instructions2 = '''
    The only cards that don't have a specific color are:
        Wild:
            When a Wild is played, the person that played the card must pick a color for the card to be
        Wild Draw 4:
            When a Wild +4 is played, the person that played the card must pick a color for the card to be and the
             next player must draw 4 cards, also skipping their turn.'''
instructions3 = '''
    Colored cards can be:
        1-9
        Action Cards:
            Draw 2:
                When a Draw 2 is played, the following player draws 2 cards and
                is not able to play a card.
            Reverse:
                When a Reverse is played, the direction of play is reversed.
            Skip:
                When a Skip is played, the following player loses their turn.'''
rules = '''
Rules:
    The object of the game is to play all the cards in your hand.
    At the start of the game, each player is dealt 7 random cards from the deck.
    After the cards are dealt, a random card will be picked from the deck to start the discard pile and be played on top of.
    If the card is a Wild Draw 4, another card will be picked.
    If the card is an action card, the action will be carried out by the first player.
    Colored cards can be played if their color or number/symbol matches the card on top of the discard pile.
    When you have 1 card remaining in your hand, you must type "uno" and press enter within 3 seconds of you 
    dealing your second to last card in your hand.
    There are no stacking rules for action cards.
    If you cannot play a card, you must draw a card from the deck.
    You may also draw a card at any time during your turn.
    A winning condition is: any player must play all your cards in their hand.
'''

input_string = """@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@######&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#############################&    &@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#############################  .@@@(   *&@@*  %@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#############################* .@/ ...............@. @@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@#######################(    .##  @@ ................... @& @@@
@@@@@@@@@@@@@@@@@@@@@@@@&#####################   @@@   @   @@ ......,@@@@@@@@@ ...... @  @
@@@@@@@@@@@@@@@@@@@@@@######################  @#@...... @@@@ ..... @@@@@@@@@###@ ..... @  
@@@@@@@@@@@@@@@@@@@#############    @,  ### &%###@ ..... @@@ .... @ *####  @###@@ ..... @ 
@@@@@@@@@@@@@@@@@########,   @@@  .... @@    @##@@@ ..... @@ .... @ *###### @@##@@ .....@ 
@@@@@@@@@@@@@@@#####( (@@(  . @@ ......... @@ @##@@@ ..... @ ..... @ ####### @@@@@..... @ 
@@@@@@@@@@@@ .####  @%#@*..... @@ ............ @@@@@@ ......@ ..... @, ##### @@@@ .....,@ 
@@@@@    @@@&# ### (@###@...... @@ ..... ........ .@@@ .....*@ ...... ,@@#/@@@,.......,@ @
@@  @@@ .....@/ ### &&@@#@ ..... @@ ......@@ ........ @ .....(@@ ................... @  @@
  @@@@@@......@, ### @%#@@@ ..... @@ .....@@@@@@ .............&@@@@ ............. @@/ @@@@
@  @@@@@@..... @  ### @@@@@@ ..... @@ .....@@@@@@@@  ..........@@@@@@@@@@@@@@@@@@@  @@@@@@
@@ .@@@@@#..... @ .### @@@@@@ ..... @@ .....&@@@@@@@@@@ ....... @@@@@@@@@@@@@@#  @@@@@@@@@
@@@ *@@@@@,..... @ /##( @@@@@@ .....@@@ .....@  @@@@@@@@@@@   @@@@          #@@@@@@@@@@@@@
@@@@ (&###@ ..... @ (##/ @@@@@ .....*@@@......@  .  @@@@@@@@@@@  ##########@@@@@@@@@@@@@@@
@@@@@ &%#@@@ ..... @* ##  @@@ ......@@@@%..... @  ###.       ,###########@@@@@@@@@@@@@@@@@
@@@@@@ @@##@@........ @@@@  .......%@@@@@/&@@@@. #####################@@@@@@@@@@@@@@@@@@@@
@@@@@@@ @@@@@@@ .................*@ (@@@@@@@*  ####################&@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@ ,@@@@@@@% .........  @@% ,# &   ,######################@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@  &@@@@@@@@@@@@@@@@@@  #############################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@  /@@@@@@@@@@@   ###########################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@....*#############################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@%##################%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""


def bordered(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)


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


def start():
    print("                                         WELCOME TO...")
    print(bordered(input_string))
    if not y_n_response(f'\nHave you played UNO!™ before? (yes/no)\n>'):
        print(f"Hello user! These are the UNO rules below. \n", instructions)
        input("\nPress enter...")
        print(instructions2)
        input("\nPress enter...")
        print(instructions3)
        input("\nPress enter...")
        print(rules)
        input("\nPress enter to start playing!")
