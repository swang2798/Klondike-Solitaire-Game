import cards        
###########################################################################
#
#   "Klondike" solitaire game
#
###########################################################################
YAY_BANNER = """
__   __             __        ___                       _ _ _ 
\ \ / /_ _ _   _    \ \      / (_)_ __  _ __   ___ _ __| | | |
 \ V / _` | | | |    \ \ /\ / /| | '_ \| '_ \ / _ \ '__| | | |
  | | (_| | |_| |_    \ V  V / | | | | | | | |  __/ |  |_|_|_|
  |_|\__,_|\__, ( )    \_/\_/  |_|_| |_|_| |_|\___|_|  (_|_|_)
           |___/|/                                            

"""

RULES = """
    *------------------------------------------------------*
    *-------------* Thumb and Pouch Solitaire *------------*
    *------------------------------------------------------*
    Foundation: Columns are numbered 1, 2, ..., 4; built 
                up by rank and by suit from Ace to King. 
                You can't move any card from foundation, 
                you can just put in.

    Tableau:    Columns are numbered 1, 2, 3, ..., 7; built 
                down by rank only, but cards can't be laid on 
                one another if they are from the same suit. 
                You can move one or more faced-up cards from 
                one tableau to another. An empty spot can be 
                filled with any card(s) from any tableau or 
                the top card from the waste.
     
     To win, all cards must be in the Foundation.
"""

MENU = """
Game commands:
    TF x y     Move card from Tableau column x to Foundation y.
    TT x y n   Move pile of length n >= 1 from Tableau column x 
                to Tableau column y.
    WF x       Move the top card from the waste to Foundation x                
    WT x       Move the top card from the waste to Tableau column x        
    SW         Draw one card from Stock to Waste
    R          Restart the game with a re-shuffle.
    H          Display this menu of choices
    Q          Quit the game
"""

def valid_fnd_move(src_card, dest_card):
    """
        Checks to see if you can move a card to the foundation
    """
    if not src_card:
        return False
    elif dest_card == ""  and src_card.rank() == 1:
        return True
    elif src_card.suit() == dest_card.suit() and src_card.rank() + 1 == dest_card.rank():
        return True
    else:
        return False
        
def valid_tab_move(src_card, dest_card):
    """
        Checks to see if you can move a card to tableau
    """    
    if not src_card:
        return False
    elif not tab:
        return True
    elif src_card.suit() != dest_card.suit() and src_card.rank() + 1 == dest_card.rank():
        return True
    else:
        return False
            
def tableau_to_foundation(tab, found):
    """
        Moves card(s) from the tableau to the foundation
    """
    try:
        card = tab.pop()
        if valid_fnd_move(card, found[-1]) == True:
            found[0] = card
            if tab[-1] == "":
                pass
            if tab[-1].is_face_up() != True:
                tab[-1].flip_card()
            
    except RuntimeError as error_message:
       print("{:s}\nTry again.".format(str(error_message)))
            

def tableau_to_tableau(tab1, tab2, n):
    """
        Moves card(s) from one row to another row in the tableau
    """  
    tab_N = tab1[-n:]
    try:
        if valid_tab_move(tab_N[0], tab2[-1]) == True:
            tab1[-n:] = []
            tab2.extend(tab_N)
            if len(tab1) == 0:
                pass
            elif tab1[-1].is_face_up() != True:
                tab1[-1].flip_card()  
    except RuntimeError as error_message:
       print("{:s}\nTry again.".format(str(error_message))) 

def waste_to_foundation(waste, found):
    """
        Moves a card from the waste pile to the foundation
    """    
    try:
        card = waste.pop()
        if valid_fnd_move(card, found[-1]) == True:
            found[0] = card
    except RuntimeError as error_message:
       print("{:s}\nTry again.".format(str(error_message)))

def waste_to_tableau(waste, tab):
    """
        Moves a card from the waste pile to the tableau
    """    
    try:
        card = waste.pop()
        if valid_tab_move(card, tab[-1]) == True:
            tab.append(card)
    except RuntimeError as error_message:
       print("{:s}\nTry again.".format(str(error_message)))
                    
def stock_to_waste(stock, waste):
    """
        Draws a card from the stock
    """    
    try:
        waste.append(stock.deal())
    except RuntimeError as error_message:
       print("{:s}\nTry again.".format(str(error_message)))
                            
def is_winner(foundation):
    """
        Prints banner if you complete the game
    """    
    if (foundation[0][0].rank() == 13 & foundation[1][0].rank() == 13 & foundation[2][0].rank() == 13 & foundation[3][0].rank() == 13):
        return True
def setup_game():
    """
        The game setup function, it has 4 foundation piles, 7 tableau piles, 
        1 stock and 1 waste pile. All of them are currently empty. This 
        function populates the tableau and the stock pile from a standard 
        card deck. 

        7 Tableau: There will be one card in the first pile, two cards in the 
        second, three in the third, and so on. The top card in each pile is 
        dealt face up, all others are face down. Total 28 cards.

        Stock: All the cards left on the deck (52 - 28 = 24 cards) will go 
        into the stock pile. 

        Waste: Initially, the top card from the stock will be moved into the 
        waste for play. Therefore, the waste will have 1 card and the stock 
        will be left with 23 cards at the initial set-up.

        This function will return a tuple: (foundation, tableau, stock, waste)
    """
    # you must use this deck for the entire game.
    # the stock works best as a 'deck' so initialize it as a 'deck'
    stock = cards.Deck()
    stock.shuffle()
    # the game piles are here, you must use these.
    foundation = [[""], [""], [""], [""]]           # list of 4 lists
    tableau = [[], [], [], [], [], [], []]  # list of 7 lists
    waste = []                              # one list
    
    # Creates tableau
    for i in range(7):
        tableau[i].append(stock.deal())
        for j in range(i+1,7):
            card = stock.deal()
            card.flip_card()
            tableau[j].append(card) 
    
    # Creates waste
    waste.append(stock.deal())
    
    return foundation, tableau, stock, waste


def display_game(foundation, tableau, stock, waste):
    """
    Displays the game after each command using the given parameters
    """    
    print("="*17,"FOUNDATION","="*17)
    print("{:<10}{:<10}{:<10}{:<10}".format("f1","f2","f3","f4"))
    print("[{!s:>3}]".format(foundation[0][0])," "*3,"[{!s:>3}]".format(foundation[1][0])," "*3,"[{!s:>3}]".format(foundation[2][0])," "*3,"[{!s:>3}]".format(foundation[3][0]," "*3))
    print("="*18," TABLEAU ","="*17)
    print("","{:<7}{:<7}{:<7}{:<7}{:<7}{:<7}{:<7}".format("t1","t2","t3","t4","t5","t6","t7"))

    print( "{:9s}{:9s}{:9s}{:9s}{:9s}{:9s}{:9s}".format( "t1", "t2", "t3", "t4", "t5", "t6", "t7" ) ) 
    print(tableau[0][0]," "*5,tableau[1][0]," "*5,tableau[2][0]," "*5,tableau[3][0]," "*5,tableau[4][0]," "*5,tableau[5][0]," "*5,tableau[6][0])
    print("{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}".format(" ",tableau[1][1],tableau[2][1],tableau[3][1],tableau[4][1],tableau[5][1],tableau[6][1]))
    print("{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}".format(" "," ",tableau[2][2],tableau[3][2],tableau[4][2],tableau[5][2],tableau[6][2]))
    print("{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}".format(" "," "," ",tableau[3][3],tableau[4][3],tableau[5][3],tableau[6][3]))
    print("{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}".format(" "," "," "," ",tableau[4][4],tableau[5][4],tableau[6][4]))
    print("{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}".format(" "," "," "," "," ",tableau[5][5],tableau[6][5]))
    print("{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}{!s:9s}".format(" "," "," "," "," "," ",tableau[6][6]))
      
    print("=" * 19, " STOCK/WASTE ", "=" * 19)
    print("Stock #("+str(len(stock))+") -->",waste[-1])

print(RULES)
fnd, tab, stock, waste = setup_game()
display_game(fnd, tab, stock, waste)
print(MENU)
user_input = input("prompt :> ")
command = user_input.strip().lower()
while command != 'q':
    try:
        if command == "h": # Reopens menu
            
            display_game(fnd, tab, stock, waste)
            print(MENU)
        elif command == "r":
            print(RULES)
            fnd, tab, stock, waste = setup_game()
            display_game(fnd, tab, stock, waste)
            print(MENU)   
        elif command == "sw":
            stock_to_waste(stock, waste)
            display_game(fnd, tab, stock, waste)
        elif "wt" in command:
            x = int(command[-1]) - 1
            waste_to_tableau(waste, tab[x])
            display_game(fnd, tab, stock, waste)
        elif "wf" in command:
            x = int(command[-1]) - 1
            waste_to_foundation(waste, fnd[x])
            display_game(fnd, tab, stock, waste)
#            if is_winner(fnd) == True:
#                print(YAY_BANNER)
        elif "tt" in command:
            x = int(command[-5]) - 1
            y = int(command[-3]) - 1
            n = int(command[-1])
            tableau_to_tableau(tab[x], tab[y], n)
            display_game(fnd, tab, stock, waste)
        elif "tf" in command:
            x = int(command[-3]) - 1
            y = int(command[-1]) - 1
            tableau_to_foundation(tab[x], fnd[y])
            display_game(fnd, tab, stock, waste)
#            if is_winner(fnd) == True:
#                print(YAY_BANNER)
    except RuntimeError as error_message:  # any RuntimeError you raise lands here
        print("{:s}\nTry again.".format(str(error_message)))       
    user_input = input("prompt :> ")
    command = user_input.strip().lower()
