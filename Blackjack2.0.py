# game of blackjack:
    # players have ability to double down, buy insurance, and bet.
    # 6 decks of cards are used, and the deck is reshufled
        # after there are 60-75 cards remaining
        

import random
number_of_decks = 6
min_cards=random.randint(0,15)+60
minimum_bet = 2
maximum_bet = 500
# name : [bet value, points, chips, revealed cards, hidden cards, aces, split?] 
import pdb

def main():
    global deck
    global player_dict
    global side_deck
    side_deck = []
    deck = create_deck()
    player_dict = determine_players()
    keep_playing = True
    player_list = []
    for player in player_dict.keys():
        player_list.append(player)
    while keep_playing:
        # is there a better way to remvoe keys? 
        player_list2 = []
        for player in player_dict.keys(): 
            if player not in player_list:
                player_list2.append(player)
        for player in player_list2:
            player_dict.pop(player)
        #####
        determine_bets()
        blackjack_list = initial_draw()
        if player_dict["The Banker"][3][0][1] == "Ace":
            insurance()
        if "The Banker" not in blackjack_list:
            for player in player_list:
                if player not in blackjack_list:
                    player_turn(player)
        else:
            # set every other player's score to 0
            for player,stats in player_dict.items():
                if player != "The Banker":
                    player_dict[player][1] = 0
                    player_dict[player][5] = 0
        settle(blackjack_list)
        keep_playing = input("\nWould you like to continue?(y/n) ")=='y'
    # create a sorted list
    player_dict2 = {}
    for player in player_list:
        if player_dict[player][2] not in player_dict2.keys():
            player_dict2[player_dict[player][2]]=player
        else:
            player_dict2[player_dict[player][2]] += ', '+player
    sorted_dict = sorted(player_dict2.items(),reverse=True)
    count = 1
    for stats in sorted_dict:
        if stats[1]!="The Banker":
            print(str(count)+":",stats[1],"has",stats[0],"chips.")
        else:
            if player_dict["The Banker"][2]<0:
                print(str(count)+": The Banker made a net loss of "+str(player_dict["The Banker"][2]*-1)+" chips")
            else:
                print(str(count)+": The Banker made a net gain of "+str(player_dict["The Banker"][2])+" chips")

        count += 1

def split(player,card1,card2):
    player_dict[player][3] = [card1]
    player_dict[player][1] = player_dict[player][1]//2
    player_dict[player][6] = True
    player_dict[player][5] = player_dict[player][5]//2
    initial = player_dict[player]
    # create a temporary player with similar stats
    temp_name = player+"(split hand)"
    player_dict[temp_name] =[initial[0],initial[1],0,[card2],[],initial[5],True]
    drawn_card = draw_card(player)
    reveal_card(player,drawn_card,False,"receives")
    drawn_card = draw_card(temp_name)
    reveal_card(temp_name,drawn_card,False,"receives")
    player_turn(player)
    player_turn(temp_name)

def player_turn(player):
    if player!="The Banker":
        # do not run this code if a result of the split function:
        split_first = False
        if not player_dict[player][6]:
            print("\nIt is "+player+"'s turn!")
            if player_dict[player][3][0][1]==player_dict[player][3][1][1] and player_dict[player][2]>=player_dict[player][0]*2:
                print(player+" has two "+player_dict[player][3][0][1]+"s.")
                if input("Do you want to split?(y/n) ")[0]=='y':
                    split(player,player_dict[player][3][0][1],player_dict[player][3][1][1])
                    split_first = True
        # do not run when player split hands
        if not split_first:
            reveal_points(player)
            user_doubles="0"
            if player_dict[player][2]>=player_dict[player][0]*2:
                user_doubles = input("Double down?(y/n) ")
            ########################
            if user_doubles.lower()=="y":
                ################
                if player_dict[player][2]>=player_dict[player][0]*2:
                    draw_card(player)
                    print(player+" places one card on the table face down.")
                    player_dict[player][0] *= 2
                ##################
            else:
                draw_cards(player)
    else:
        print("\nIt is "+player+"'s turn!")
        banker_turn()

def draw_cards(player):
    end = False
    if input(player+", do you want to \"hit\" or \"drop\"? ")[:1].lower() != "h"\
       or player_dict[player][1]+player_dict[player][5]>=21:
        end = True
    while not end:
        drawn_card = draw_card(player)
        reveal_card(player,drawn_card,True,"draws")
        if player_dict[player][1]+player_dict[player][5]>=21:
            end = True
        elif input("\n"+player+", do you want to \"hit\" or \"drop\"? ")[:1].lower() != "h":
            end = True
            
def banker_turn():
    aces = player_dict["The Banker"][5]
    reveal_card("The Banker",player_dict["The Banker"][4][0],False,"reveals")
    while (player_dict["The Banker"][1]+aces*11<=16) \
          or ((player_dict["The Banker"][1]+aces*11>=21) and \
              (player_dict["The Banker"][1]+aces*1<=16)):
        drawn_card = draw_card("The Banker")
        reveal_card("The Banker",drawn_card,False,"draws")
        aces = player_dict["The Banker"][5]
    reveal_points("The Banker")
    print()

def initial_draw():
    blackjack_list = []
    for player in player_dict.keys():
        for card in range(2):
            drawn_card = draw_card(player)
            if player != "The Banker" or card!= 1:
                reveal_card(player,drawn_card,card,"draws")
            else:
                print("The Banker keeps one card face down on the table.")
        if player_dict[player][1] == 10 and player_dict[player][5]:###
            # do not print if the player is the banker and the first revealed value is 0
            if player != "The Banker" or player_dict["The Banker"][3][0][0]!=0:
                print(player+" made a natural blackjack.")
            if player == "The Banker":
                return ["The Banker"]
            else:
                blackjack_list.append(player)
        print()
    return blackjack_list
        
def reveal_card(player,drawn_card,points,verb):
    print(player,verb,"a "+drawn_card[1]+" of "+drawn_card[2]+".")
    #remove drawn_card from player_dict[player][4] and add to player_dict[player][3]
    player_dict[player][3].append(drawn_card)
    player_dict[player][4].remove(drawn_card)
    if points:
        reveal_points(player)
        
def reveal_points(player):
    ace_count = player_dict[player][5]
    points = player_dict[player][1]
    if ace_count == 0:
        print(player+" has",points,"points.")
    else:
        print(player+" has",points,"points, not including", \
              ace_count,"ace"+"s"*(ace_count!=1)+".")
    if ace_count + points > 21:
        print(player+" has gone 'bust'!")

def create_deck():                                
    deck = []
    for card in range(1,52*number_of_decks):
        card_value = card%13
        if card_value>10:
            card_value = 10
        if card%4 == 0:
            card_type = "hearts"
        elif card%4 == 1:
            card_type = "diamonds"
        elif card%4 == 2:
            card_type = "spades"
        else:
            card_type = "clubs"
        if card%13 == 1:
            card_name = "Ace"
            card_value = 0 #use 0 for the value of an ace
        elif card%13 == 11:
            card_name = "Jack"
        elif card%13 == 12:
            card_name = "Queen"
        elif card%13 == 0:
            card_name = "King"
            card_value = 10
        else:
            card_name = str(card_value)
        deck.append([card_value,card_name,card_type])
    return deck

# returns [value, card_name, card_type]
def draw_card(player):
    global deck
    global side_deck
    deck = deck
    if len(deck)==min_cards:
        print("There are not enough cards left in the deck. \
                The side cards are added to the deck.")
        for card in side_deck:
            deck.append(card)
        random.shuffle(deck)
        side_deck=[]
    card_number = random.randint(0,len(deck)-1)
    drawn_card = deck[card_number]
    ###############################
    #test_card = random.randint(0,1) # create test card (50%)
    #if test_card==1:
        #drawn_card = [0,'Ace','TEST'+str(random.randint(0,100))]
    #else:
        #drawn_card = [10,'10','TEST2.0'+str(random.randint(0,100))]
    ###############################
    deck.pop(card_number)
    player_dict[player][1] += drawn_card[0]
    if drawn_card[1] == "Ace":
        player_dict[player][5] += 1
    player_dict[player][4].append(drawn_card)
    return drawn_card

def determine_players():
    number_of_players = int(input("How many players? "))
    player_dict = {}
    for player in range(1,number_of_players+1):
        invalid_name = True
        while invalid_name:
            name = input("player "+str(player)+" name: ")
            if name not in player_dict and "(split hand)" not in name and name!="The Banker":
                invalid_name = False
            else:
                print("Choose a different name.")
        user_chips = int(float(input("How many chips will you use? ")))
        player_dict[name] = [0,0,user_chips,[],[],0,False]
    player_dict["The Banker"] = [0,0,0,[],[],0,False]
    return player_dict

def determine_bets():
    for player in player_dict.keys():
        if player!= "The Banker":
            bet = minimum_bet-1
            while True:
                try:
                    bet = int(input("How many chips will "+player+" bet? "))
                    if bet > player_dict[player][2]:
                        print("You cannot wager more chips than you have.")
                        print(player+" has "+str(player_dict[player][2])+" chips.")
                    if (bet>=minimum_bet and bet<=maximum_bet) and bet<=player_dict[player][2]:
                        break
                    else:
                        int("5.3")
                except ValueError:
                    bet = print("Choose an integer between "+str(minimum_bet)+" and "+\
                                str(maximum_bet)+".")  
            player_dict[player][0] = bet

def det_double_down():
    for player,player_stats in player_dict.items():
        if player_stats[4] != []:
            print(player+" reveals the face down card.")
            reveal_card(player,player_stats[4][0],True,"revealed")

def insurance():
    no_ten = player_dict["The Banker"][1] != 10
    did_bet = False
    for player in player_dict.keys():
        if player != "The Banker":
            bet = 0
            # only run if user_chips-bet_value is greater than 1.
            if player_dict[player][2]-player_dict[player][0]>=1:
                insured = 'y'==input("Will "+player+" bet that The Banker has a 10 card?(y/n) ")
                while insured:
                    try:
                        bet = int(input("How much will "+player+" bet that The Banker has a 10 card? "))
                        if not (bet<=player_dict[player][0]//2 and bet>0):
                            int("3.14")
                        else:
                            did_bet = True
                            break
                    except ValueError:
                        # must be less than chips-bet and less than half bet.
                        half_bet = player_dict[player][0]//2
                        over_0 = player_dict[player][2]-player_dict[player][0]
                        if over_0<half_bet:
                            minimum = over_0
                        else:
                            minimum = half_bet
                                
                        print("Choose an integer between 0 and "+str(minimum)+". ")
                if no_ten:
                    player_dict[player][2] -= bet
                    player_dict["The Banker"][2] += bet
                else:
                    player_dict[player][2] += 2*bet
                    player_dict["The Banker"][2] -= 2*bet
            else:
                print(player+" may not be able to afford insurance this hand.")
    if did_bet:
        if no_ten:
            print("The Banker does not have a card of value 10.")
        for player in player_dict.keys():
            print(player+" now has "+str(player_dict[player][2])+" chips.")

def calculate_points():
    print()
    for player in player_dict:
        aces = player_dict[player][5]
        current = player_dict[player][1]
        # while the player can use one of their aces as 11:
        while aces + 10 + current <= 21 and aces>0:
            # replace an ace with 11 points
            aces -= 1
            current += 11
        points = aces + current
        player_dict[player][1] = points
        player_dict[player][5] = 0
        reveal_points(player)
    print()

def settle(blackjack_list):
    det_double_down()
    calculate_points()
    banker_score = player_dict["The Banker"][1]
    if banker_score>21:
        banker_score = 0
    for player,player_values in player_dict.items():
        if player != "The Banker":
            if "(split hand)" in player:
                # change player to exclude the string "(hand 2)"
                player = player[:-12]
            # only reference the chips of the original player
            chips = player_dict[player][2]
            points = player_values[1]
            bet = player_values[0]
            aces = player_values[5]
            if points<banker_score or points>21 or "The Banker" in blackjack_list:
                player_dict["The Banker"][2] += bet
                chips -= bet
                print(player+" lost "+str(bet)+" chips to the banker.")
                print(player+" now has "+str(chips)+" chips.")
            elif points>banker_score or player in blackjack_list:
                player_dict["The Banker"][2] -= bet
                chips += bet
                print(player+" gained "+str(bet)+" chips from the banker.")
                print(player+" now has "+str(chips)+" chips.")
            else:
                print(player+" still has "+str(chips)+" chips.")
            player_dict[player][2] = chips
        for card in player_dict[player][3]:
            side_deck.append(card)
        player_dict[player][3] = []
        player_dict[player][0] = 0
        player_dict[player][1] = 0
    if player_dict["The Banker"][2]<0:
        print("The Banker made a net loss of "+str(player_dict["The Banker"][2]*-1)+" chips")
    else:
        print("The Banker made a net gain of "+str(player_dict["The Banker"][2])+" chips")

main()
