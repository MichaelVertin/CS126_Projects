# if the apple is below the snake:
    # only move down if the area between the apple and snake head is \
                # less than one-third of the remaining board_space
# allow for odd board_widths
# create a 'respective board height' if the apple is left of the snake \
    # and the entire snake is below the head y-val
# remove area_check
# if the snake is taking shortcut1:
    # allow the snake to take shortcut1 again
    # if snake_head is one from the top:
        # if the apple is to the left of the snake:
            # allow the snake to move to the left
            # the snake does not move down until it is at an odd space
# when the snake eats apple during shortcut:
    # create a function that re-evaluates its options


# WHEN CALCULATING PARTS IN WAY:(rather than including the top row):
    # if the snake part is one away from the top:
        # if a snake part is directly above that part:
            # if the magnitude of difference between those two parts are equal to 1:
                # add one to "parts in way"

import turtle
import sys
import time
import keyboard
import random
import pdb ###
UPDATE_VAL = 1

TITLE = "SNAKE!"
BOXSIZE = 20
SNAKESIZE = 5
SNAKECOLOR = "green"
COLOR1 = "white"
COLOR2 = "black"
DOT_COLOR1 = "green"
DOT_COLOR2 = "yellow"
DOT_COLOR3 = "white"
MIDDOT_COLOR = "black"
CENTERDOT_COLOR = "red"
INITIALDELAY = 0# Time
DELAYMOD = .9
REPLAYCOLOR = "blue"
SCOREINCREMENT = 10
DOTS = False
TEXTCOLOR = "white"
SHORT_MULT = .750
SHORT_SUB = 0
POT_APPLES = 4 # snake can only eat apples until it starts following the tail
REMOVE_SHORTCUT1 = False
POT_APPLE_MULT = 1.2
MAX_AREA_RATIO = .3
END_GAME_MESSAGE = False

# when moving down or up:
    # allow the snake to <move 1 left and turn around(shortcut)
        # do not do this if a shortcut is already being used
# create more functions to find shortcuts:
# if the snake is moving horizontally:
    # if no snake part is located under the head
        # if the apple is located to the left of the head:
            # start the snake moving downwards
# apply buffer to more shortcuts

# the main game
def main():
    turty,replay_turtle,board_turtle,write_turtle,\
            replay_turtle2,direction,settings_dict = before_game_begins()
    while settings_dict["play_again"]:
        apple_loc,snake_list,\
                = before_motion_begins(direction,turty,write_turtle,settings_dict)
        play_instance_of_game(apple_loc,snake_list,settings_dict,direction,\
                turty,replay_turtle,board_turtle,write_turtle,replay_turtle2)
        if settings_dict["win"]:
            print("You Win!")
            if END_GAME_MESSAGE:
                settings_dict["play_again"] = replay_option(replay_turtle,"WON",replay_turtle2,settings_dict)
        else:
            print("You lose!")
            if END_GAME_MESSAGE:
                settings_dict["play_again"] = replay_option(replay_turtle,"LOST",replay_turtle2,settings_dict)
        if settings_dict["usable_record"]:
            settings_dict["play_again"] = False
        turty.clear()
    turtle.bye()

def det_under_head(apple_loc,snake_list,settings_dict):
    under_head = True
    # if the head of the snake is at the top and the apple is not to the right of the snake:
    if apple_loc[0]<=snake_list[-1][0]:
        under_head = False
        # determine if the snake is under the head
        check_list = []
        for ver_val in range(0,settings_dict["board_height"]-1):
            if [snake_list[-1][0],ver_val] in snake_list[:-1]:
                under_head = True
        # if the snake is at an even location:
        if snake_list[-1][0]%2 == 0:
            # do not move the snake down
            under_head = True
    # the head can follow the same path as the tail(consider for length)
        # the minimum index is the index of the tail where enters border(left side)
    know_snake_part = False
    no_part = False
    hor_val = 0
    part_loc = "None"
    # while a there is not a known snake part and there could be a part in the top row:
    while (not know_snake_part) and (not no_part) and (not under_head):
        # try to find a snake part reference on the top border
        part_loc = [hor_val,settings_dict["board_height"]-1]
        know_snake_part = part_loc in snake_list
        # if the check reached the end of the board
        if hor_val==settings_dict["board_width"]-1:
            # there are no parts to check
            no_part = True
        hor_val += 1
        if know_snake_part:
            break

    # if there is a part location:
    if know_snake_part and (not under_head):
        # find the index of that part
##########################################################
        #### THIS IS THE INCORRECT VALUE:
            # THE FIRST INDEX WILL NOT BE THE SAME AS THE FIRST PART OF THE SNAKE
        min_index = int(snake_list.index(part_loc)/POT_APPLE_MULT) - POT_APPLES


        # the minimum index will be no smaller than twice the board_height and the board_width
#############THIS CODE OVERRIDES THE ORGINAL MIN_INDEX # -3 for the corners
        min_index = 2*settings_dict["board_height"] + snake_list[-1][0] - POT_APPLES - 3
##########################################################
        if min_index<0:
            min_index = 0
        # the hor_val is the furthest point left (0)
        init_hor_val = 0
        if not (check_top_row(snake_list,min_index,init_hor_val,settings_dict)):
            turtle.update()
            under_head = True
    return under_head
    



def check_condition2(snake_list,apple_loc,settings_dict):
    in_way = True
    if apple_loc[0]>snake_list[-1][0] and snake_list[-1][1]==settings_dict["board_height"]-2\
       and [snake_list[-1][0],snake_list[-1][1]+1] not in snake_list\
       and [snake_list[-1][0]+1,snake_list[-1][1]+1] not in snake_list\
       and [snake_list[-1][0]+2,snake_list[-1][1]+1] not in snake_list:
        in_way = False
        # only turn up if there is enough space for the tail to move out of the
            # way from the top of the board
        # find the index of the closest tail
        # for every hor_val between the snake head and end of board:
        closest_index = "None"
        closest_hor_val = "None"
        for hor_val in range(snake_list[-1][0],settings_dict["board_width"]-1):
            # if that value is occupied at the top of the board:
            if [hor_val,settings_dict["board_height"]-1] in snake_list[:-1]:
                # attain that index
                closest_index = snake_list.index([hor_val,settings_dict["board_height"]-1])
                    # also attain the hor_val
                hor_val = hor_val
                # stop attaining indices
                # if there is an index:
                # if the distance from the head to that value (include apple buffer)
                if (hor_val-snake_list[-1][0])+int(((settings_dict["board_height"]-1)-snake_list[-1][1])<closest_index*POT_APPLE_MULT)+POT_APPLES:
                                        # is greater than the index:
                    # do not run the shortcut
                    in_way = True
    return not in_way
    
def play_instance_of_game(apple_loc,snake_list,settings_dict,direction,\
                turty,replay_turtle,board_turtle,write_turtle,replay_turtle2):
    settings_dict["num_games"] += 1
    print("\n\n\n\nGame Number ",settings_dict["num_games"],":",sep="")
    while settings_dict["move_snake"]: # while the snake is moving...
# STOP CODE FROM RUNNING
        if len(snake_list)>=settings_dict["board_width"]*settings_dict["board_width"]*1.00:
            settings_dict["win"] = True
            settings_dict["move_snake"] = False
        # stop shortening converted for boards:
        # as the board size decreases:
            # increase the percent
        percent_mult = SHORT_MULT*(settings_dict["board_width"]**(-1/2))
        con_val = settings_dict["board_width"]*settings_dict["board_width"]*(1-percent_mult)*SHORT_MULT
        if len(snake_list)>con_val and settings_dict["shorten"]:
            settings_dict["shorten"] = False
            print("No longer shortens")
        # stop taking short-cuts after the snake reaches a certain size
        if len(snake_list)>(settings_dict["board_width"]-SHORT_SUB)*settings_dict["board_height"]*SHORT_MULT-5 and settings_dict["shorten"]:
            settings_dict["shorten"] = False
            print("No longer shortens")
        # if the snake head at the same y-location of the apple location
            # and the snake is not 'moving horizontally':
            # and not already moving toward the apple
        if settings_dict["shorten"]:
            # move_toward_apple conditions are here
            if snake_list[-1][1] == apple_loc[1] and settings_dict["move_hor"] == False and \
               not settings_dict["move_toward_apple"] and snake_list[-1][0]>apple_loc[0]\
               and snake_list[-1][1]!=settings_dict["board_height"]-1:
                in_way = False
                buffer = (snake_list[-1][0]-apple_loc[0])
                # calculate the 'values' of each snake that is between the apple and snake
                # ignore buffer and moving up/down
                in_way_val =0
                greatest_hor_val = 0
                # find every location that can be in the way
                for hor_val in range(apple_loc[0]-1,snake_list[-1][0]):# include both for buffer
                    for ver_val in range(0,settings_dict["board_height"]-1):# stop before the top of the boar
#### REMOVED -1 from "ver_val's range" SO THAT ACCOUNTS FOR TOP ROW:
# USE INDEXING TO DETERMINE WHETHER THE SNAKE CAN BE IMPACTED
                        # if that location is in the snake_list:
                        if [hor_val,ver_val] in snake_list[:-1]:
                            in_way_val += 1
                            # include the snake part is one from the top:
                            if ver_val == settings_dict["board_height"]-2 and \
                               [hor_val,ver_val+1] in snake_list:
                                if abs(snake_list.index([hor_val,ver_val])-snake_list.index([hor_val,ver_val+1])) == 1:
                                    in_way_val += 1
                    # THIS IS WHERE BUFFER WOULD GO
                    # if shares the same y-val as the head:
                    if [hor_val,snake_list[-1][1]] in snake_list[:-1]:
                        in_way=True
                # always want this code to run
                if in_way_val>=buffer:
                    in_way=True
# REMOVED POT_APPLES HERE:
# NEED TO ACCOUNT FOR THIS IF APPLES CAN CAUSE A LOSS
                # the minimum index is distance the snake needs to move
                            # to get to the top of the board
                    # distance from left side of board to snake head and
                    # distance from head y-val to top of board
                min_index = (snake_list[-1][0]-0)+\
                        int(((settings_dict["board_height"]-1)-snake_list[-1][1]-POT_APPLES)/POT_APPLE_MULT)
                init_hor_val = apple_loc[0]-1
                # if the top row check failed:
                if not in_way:
                    if not check_top_row(snake_list,min_index,init_hor_val,settings_dict):
                        # it is in the way
                        in_way = True
                # determine if the snake is in the way:
                parts_in_way = 0
                for location in snake_list:
                    if location[0]<snake_list[-1][0] and location[0]>apple_loc[0]\
                       and location[1]!=settings_dict["board_height"]-1:
                        parts_in_way += 1
                if not in_way:
                    # create a shorten_option
                    target_loc = shorten_option(snake_list,apple_loc,\
                        direction,settings_dict)
                    settings_dict["move_toward_apple"] = True
       # if the apple is 'behind' the snake and the snake is 1 from the top:
            # move to the top and start 'move_hor'
        conditions = check_conditions(snake_list,apple_loc,settings_dict)
        if conditions:
            find_shortcut1(snake_list,apple_loc,settings_dict)
            if settings_dict["shortcut_list"] == False:
                settings_dict["shortcut_list"] = "None"
            else:
                settings_dict["apple_loc_short1"] = apple_loc
        if settings_dict["shortcut_list"] == "None" and apple_loc[1]!=settings_dict["board_height"]-1\
           and snake_list[-1][0]<settings_dict["board_width"]-2 and snake_list[-1][0]%2 == 1: # only down on odd columns
            # must be same x-val and at the top
            if (apple_loc[0] == snake_list[-1][0] or apple_loc[0] == snake_list[-1][0]+1)\
               and snake_list[-1][1]== settings_dict["board_height"]-1:
                pot_list = move_down_option(snake_list,apple_loc,settings_dict)
                if pot_list:
                    settings_dict["shortcut_list"] = pot_list
                    
        # turn to the left of the board early
        if check_condition2(snake_list,apple_loc,settings_dict):
            # turn the direciton up
            direction[0] = 90
        elif settings_dict["move_hor"] == True:
            move_hor_option(snake_list,\
                    direction,apple_loc,settings_dict)
            # it is changing the direction
        elif settings_dict["move_toward_apple"]:
            move_to_apple_opt(snake_list,target_loc,direction,settings_dict)
        else:
            option_4(direction,snake_list,\
                    settings_dict)
        if snake_list[-1][1] == settings_dict["board_height"]-1 and snake_list[-1][0] != settings_dict["board_width"]-1:
            # if the snake is not directly above or above and left of the snake head:
            direction[0] = 0
            settings_dict["move_hor"] = True
            move_hor_option(snake_list,\
                    direction,apple_loc,settings_dict)
                    # the snake starts to move horizontally
        # use the shortcut list
        if settings_dict["shortcut_list"]!="None":
            run_shortcut_option(direction,snake_list,apple_loc,settings_dict)
        if apple_loc[0]<snake_list[-1][0] and apple_loc[1] == settings_dict["board_height"]-1\
           and settings_dict["shortcut_list"] == "None" and snake_list[-1][1]!=settings_dict["board_height"]-1:
            my_list = get_to_top_row(apple_loc,snake_list,settings_dict)
            if my_list!=False:
                settings_dict["shortcut_list"] = my_list
                # initialize the movement of the shortcut immidiately
                direction[0] = settings_dict["shortcut_list"][settings_dict["shortcut_list_index"]]
                settings_dict["shortcut_list_index"] += 1
        # want to allow snake to curve around here
        if settings_dict["apple_loc_short1"][0] == snake_list[-1][0]:
            apple_loc_short1 = "None"
        # ensure snake does not move into border
        if snake_list[-1][0] == 0 and direction == [180]:
            direction[0] = 90
        if snake_list[-1][1] == settings_dict["board_height"]-1 and direction!=[270]:
            direction[0] = 0
        if snake_list[-1] == [settings_dict["board_width"]-1,settings_dict["board_height"]-1]:
            direction[0] = 270
        if snake_list[-1] == [settings_dict["board_width"]-1,0]:
            direction[0] = 180
        if snake_list[-1][1] == 0 and direction == [270]:
            if snake_list[-1][0]%2 == 0:
                direction[0] = 90
            else:
                direction[0] = 180
            print("Overwrote at bottom")
        # if the snake head is at the top of the board
            # do not run shortcuts
        if check_border(snake_list,direction,settings_dict):
            settings_dict["move_snake"] = False
        if settings_dict["move_snake"]:
            # move the snake one forward
            # check if the head occupies the same location as the apple
            if snake_list[-1] == apple_loc:
                # print("ate apple at: ",apple_loc)
                # do not erase tail
                move_snake_1(snake_list,direction,turty,False,settings_dict)
                apple_loc = generate_apple(snake_list,turty,settings_dict)
                settings_dict["total_score"] += SCOREINCREMENT
                if settings_dict["total_score"]>settings_dict["best_score"]:
                    settings_dict["best_score"] = settings_dict["total_score"]
                # write changable values
                write_scores(write_turtle,settings_dict)
                # decrease pause_time
                settings_dict["pause_time"][0] *= DELAYMOD
            else:
                # erase tail
                move_snake_1(snake_list,direction,turty,True,settings_dict)
        # if the snake hit moved around the board 10 times:
        apple_loc=stuff_after_moved(direction,apple_loc,snake_list,\
                turty,settings_dict)
    print_stats(settings_dict)
    turtle.update()
    if not settings_dict["win"]:
        while not settings_dict["quit_game"][0]:
            if not settings_dict["quit_game"][0]:
                time.sleep(1)
    turtle.tracer(False)

def print_stats(settings_dict):
    print("apple_record =\n\n",settings_dict["apple_record"])
    settings_dict["total_tiles"] += settings_dict["tiles_moved"]
    average_tiles = settings_dict["total_tiles"]/settings_dict["num_games"]
    print("average_tiles = ",average_tiles)

# given a "min_index" and a "initial_top_location":
                        # only horizontal value where snake would enter the top row
    # for the top row:
        # check if the index is too long for the snake to fit in
def check_top_row(snake_list,min_index,init_hor_val,settings_dict):
    # for every hor_value that will be iterated over
    for hor_val in range(init_hor_val,settings_dict["board_width"]-1):
        # if that value is in the snake:
            # ignore the first "min_indices"
        if [hor_val,settings_dict["board_height"]-1] in snake_list[min_index:-1]:
            return False # the check failed
        # add one value (as the buffer) to the min_index
        min_index += 1
    return True # the check passed all tests


# ALSO NEED TO APPLY THE "AREA RULE"
def move_down_option(snake_list,apple_loc,settings_dict):
##########################################################
    # determine if the ratio of area between the snake and apple to the rest of \
                    # the board is too large
    # the area between the apple and snake is twice the difference in y-vals
    apple_snake_area = snake_list[-1][1]-apple_loc[1]
    # the empty area is the board_size - snake_size
    empty_area = settings_dict["board_height"]*settings_dict["board_width"]-len(snake_list)
    # the area_ratio is the ... 'ratio' of them
    apple_to_empty_ratio = apple_snake_area/empty_area
    if apple_to_empty_ratio>MAX_AREA_RATIO:
        return False
##########################################################
    if not settings_dict["shorten"]:
        return False
    # ENSURE THIS DOES NOT INTERFERE WITH MOVE STRAIGHT DOWN:
        # put as an else...
    # if the area is "too small"
        # return False
    # DO NOT RUN IF THERE IS NO SNAKE BELOW THE APPLE
    # have a more efficient function to do this
    snake_below_apple = False
    for ver_val in range(0,apple_loc[1]):
        if [snake_list[-1][0],ver_val] in snake_list[:-1]:
            snake_below_apple = True
    for ver_val in range(0,apple_loc[1]):
        if [snake_list[-1][0]+1,ver_val] in snake_list[:-1]:
            snake_below_apple = True
    # if there is not a snake below the apple, do not run
    if not snake_below_apple:
        return False
    run_code = True
    # if the snake is not between the y-vals of the snake head and the apple
    for ver_val in range(apple_loc[1],snake_list[-1][1]+1):
        # FOR HOR_VAL EQUAL TO SNAKE HEAD AND ONE MORE:
        if [snake_list[-1][0],ver_val] in snake_list[:-1] or\
            [snake_list[-1][0]+1,ver_val] in snake_list[:-1]:
            # do not run the code
            run_code = False
    y_dif = snake_list[-1][1]-apple_loc[1]
    # if "the code is ran":
    if run_code:
        # make a list of every direction in the path
        dir_list = []
        # for every location between the snake head and the apple:
        for ver_val in range(y_dif):
            dir_list.append(270)
            # add "down" to the list of directions
        # add one "left"
        dir_list.append(0)
        # for every location between the snake head and the apple:
        for ver_val in range(y_dif):
            dir_list.append(90)
            # add "up" to the list of directions
        # return the list of directions
        return dir_list
    # else:
    else:
        return False
        # return False


        
def get_to_top_row(apple_loc,snake_list,settings_dict):
    head_loc = snake_list[-1]
    # check if the snake is in the way:
    # initialize a valid path
    valid_path = True
    location_list = []
    dir_list = []
    # for every location in the path:
    for hor_val in range(head_loc[0]-apple_loc[0]):
        # add that location
        location_list.append([head_loc[0]-hor_val,head_loc[1]])
        dir_list.append(180)
    for ver_val in range(apple_loc[1]-head_loc[1]):#############
        location_list.append([apple_loc[0],ver_val+head_loc[1]])
        dir_list.append(90)
    for location in location_list:
        if location in snake_list[:-1]:
            return False
    # the minimum index is the hor_distance between the apple and head plus \
            # the ver_distance between the top of the board and snake_head
    min_index = int(((snake_list[-1][0]-apple_loc[0]) + \
                (apple_loc[1] - snake_list[-1][1]))/POT_APPLE_MULT) - POT_APPLES
    # the snake enters the top row at the apple_x_val
    init_hor_val = apple_loc[0]
    if (check_top_row(snake_list,min_index,init_hor_val,settings_dict)):
        return dir_list
    return False

def shorten_option(snake_list,apple_loc,\
                   direction,settings_dict):
    direction[0] = 180
    target_loc = apple_loc.copy()
    # if at the bottom or top:
    if target_loc[1] == 0:
        # if it would move down
        if target_loc[0]%2 == 1:
            # instead make the snake move one further
            target_loc[0] -= 1
    elif target_loc[1] == settings_dict["board_height"]-2:
        # if it would move up (exclude last location on board)
        if target_loc[0]%2 == 0 and target_loc[0]!=0:
            target_loc[0] -= 1    
    #print("Moving toward apple...")
    return target_loc

###########################################################
#         functions for simplifying main: options        #
###########################################################
# CHANGE TO ONLY MOVE DOWN ON EVEN BOARD_SQUARES
def move_hor_option(snake_list,direction,apple_loc,settings_dict):
    under_head = det_under_head(apple_loc,snake_list,settings_dict)
    # when the snake head reaches the border:
    if (snake_list[-1][0] == settings_dict["board_width"]-1) or not under_head:#####
        # turn down
        direction[0] = 270
        settings_dict["move_hor"] = False
        settings_dict["previous_dir"] = "down"

def move_to_apple_opt(snake_list,target_loc,direction,settings_dict):
# CHECK IF THE TARGET LOCATION IS OCCUPIED BY THE SNAKE
# CHECKMARK1: # don't move up when snake is above
    # if the snake is before the previous location:
        # proceed as normal
    if snake_list[-1][0]==target_loc[0]:
        settings_dict["move_toward_apple"] = False
        # if the snake head is at a odd x-coor:
        if snake_list[-1][0]%2 == 0:
            # needs to move up
            new_dir = 90
            settings_dict["previous_dir"] = "up"
        else:
            # move down
            new_dir = 270
            settings_dict["previous_dir"] = "down"
        # change the direction
        direction[0] = new_dir

def option_4(direction,snake_list,settings_dict):
    turn_early_condition = ((([snake_list[-1][0],snake_list[-1][1]+1] in snake_list)\
                    and direction == [90]))
    # if the snake is one left and one up of the snake\
        # and that part of the snake is moving upward
        # (the next index in the snake is one above the current index
    if ([snake_list[-1][0]-1,snake_list[-1][1]+1] in snake_list) and direction == [90]:
        current_index = snake_list.index([snake_list[-1][0]-1,snake_list[-1][1]+1])
        if snake_list[current_index+1] == [snake_list[-1][0]-1,snake_list[-1][1]+2]:
            turn_early_condition = True
    if direction == [270] and snake_list[-1][1]==0:
        direction[0] = 180
    elif direction == [180]:
        if settings_dict["previous_dir"] == "down" and snake_list[-1][0]%2 == 0:
            min_index = 0 # the snake will move to the top row directly onto the snake head
            init_hor_val = snake_list[-1][0] # directly above the head
            # only start to move up if the snake is not directly above the head
            if [snake_list[-1][0],snake_list[-1][1]+1] not in snake_list[1:]:
                direction[0] = 90
                settings_dict["previous_dir"] = "up"
        elif settings_dict["previous_dir"] == "up":
            direction[0] = 270
            settings_dict["previous_dir"] = "down"
        else:
            direction[0] = 270
    elif direction == [90] and (snake_list[-1][1] == settings_dict["board_height"]-2\
         or turn_early_condition):### added turn_early_condition
        option=4.2
        if snake_list[-1][0] != 0:
            direction[0] = 180

def run_shortcut_option(direction,snake_list,apple_loc,settings_dict):
    if not REMOVE_SHORTCUT1:
        direction[0] = settings_dict["shortcut_list"][settings_dict["shortcut_list_index"]]
        if settings_dict["shortcut_list_index"]==len(settings_dict["shortcut_list"])-1:
            settings_dict["shortcut_list"] = "None"
            settings_dict["shortcut_list_index"] = 0
        else:
            settings_dict["shortcut_list_index"] += 1
        if snake_list[-1] == apple_loc:
            #print("before check_conditions")
            conditions = check_conditions(snake_list,apple_loc,settings_dict)
            if conditions:
                find_shortcut1(snake_list,apple_loc,settings_dict)
                #print("pass condition tests(2)")
                if settings_dict["shortcut_list"] == False:
                    settings_dict["shortcut_list"] = "None"
                    #print("find_shortcut1 overrode")

##############################################################################
#                             hotkey functions                               #
##############################################################################
def manual_apples(settings_dict,on_off):
    if on_off:
        settings_dict["man_apple"][0] = True
    else:
        settings_dict["man_apple"][0] = False


def make_break(settings_dict,par):
    pause_time = settings_dict["pause_time"]
    if par == "fast" and pause_time[0]>=.05:
        pause_time[0] -= .05
    elif par == "slow":
        pause_time[0] += .05
    elif par == "veryslow":
        pause_time[0] += .5
    elif par == "veryfast":
        pause_time[0] = 0

def before_game_begins():
    # define the grid size
    if len(sys.argv) == 1:
        board_width = 10
        board_height = 10
    else:
        board_width = int(sys.argv[1])
        board_height = int(sys.argv[2])
        if board_width%2 == 1:
            print("board_width cannot be an odd value")
            board_width += 1
    settings_dict = {}
    settings_dict["pause_time"] = [INITIALDELAY]
    settings_dict["man_apples"] = [False]
    settings_dict["board_width"] = board_width
    settings_dict["board_height"] = board_height
    settings_dict["best_score"] = 0
    settings_dict["play_again"] = True
    settings_dict["direction"] = ["Hello, World!"]
    settings_dict["quit_game"] = ["Hello, World!"]
    settings_dict["man_apple"] = [False]
    # create a apple record of apple locations
    settings_dict["apple_record"] = []
    # ASSIGN USABLE RECORD
    # ASSIGN APPLE RECORD
    settings_dict["usable_record"] = False#[[1, 5], [0, 0], [1, 5], [5, 1], [0, 4], [0, 0], [2, 2], [2, 4], [2, 0], [1, 0], [0, 4], [5, 2], [3, 4], [1, 0], [1, 2], [5, 5], [5, 3], [5, 1], [4, 3], [3, 3], [0, 1], [0, 3], [0, 5], [2, 5], [2, 4]]
    
    
    settings_dict["record_index"] = 0
    settings_dict["total_tiles"] = 0
    settings_dict["num_games"] = 0
##############
    # defire turtle
    turty = turtle.Turtle()
    write_turtle = turtle.Turtle()
    replay_turtle = turtle.Turtle()
    board_turtle = turtle.Turtle()
    write_turtle.hideturtle()
    replay_turtle2 = turtle.Turtle()
    replay_turtle2.hideturtle()
    best_score = 0
    direction = ["Hello, World!"]
    # Create the board
    create_gameboard(board_turtle,settings_dict)
    turty.hideturtle()
    board_turtle.hideturtle()
    replay_turtle.hideturtle()
    turtle.hideturtle()
    write_turtle.hideturtle()
    #keyboard.add_hotkey('q',quit_game_fun,[settings_dict])
    keyboard.add_hotkey("x",make_break,[settings_dict,"fast"])
    keyboard.add_hotkey("v",make_break,[settings_dict,"slow"])
    keyboard.add_hotkey("b",make_break,[settings_dict,"veryslow"])
    keyboard.add_hotkey("z",make_break,[settings_dict,"veryfast"])
    #keyboard.add_hotkey("1",manual_apples,[settings_dict,True])
    #keyboard.add_hotkey("2",manual_apples,[settings_dict,False])
    return turty,replay_turtle,board_turtle,\
           write_turtle,replay_turtle2,\
           direction,settings_dict

def stuff_after_moved(direction,apple_loc,snake_list,turty,settings_dict):
    # if the snake hit moved around the board 10 times:
    if len(snake_list)==(settings_dict["board_width"]*settings_dict["board_height"]):
        settings_dict["win"] = True
        settings_dict["move_snake"] = False
        print("You win!")
    settings_dict["tiles_moved"] += 1
    #######
    if random.randint(1,UPDATE_VAL) == 1:
        turtle.update()
    #######
    time.sleep(settings_dict["pause_time"][0])
    if settings_dict["quit_game"][0]:
        settings_dict["move_snake"] = False
    turtle.delay(0)
    settings_dict["move_counter"] += 1
    if settings_dict["move_counter"]%2==0: # redraw snake
        turty.clear()
        draw_snake(snake_list,turty,settings_dict["board_width"])
        draw_snake_head(snake_list[-1],direction[0],turty,settings_dict["board_width"])
        if settings_dict["move_snake"]:
            draw_apple(apple_loc,turty)
    return apple_loc

def before_motion_begins(direction,\
            turty,write_turtle,settings_dict):
    turtle.tracer(False)
    # create the snake
    snake_list = create_snake(turty,settings_dict)
    # draw the snake
    apple_loc = generate_apple(snake_list,turty,settings_dict)
    # initialize changed_direction variable
    direction[0] = "None"
    # initialize snake_movement
    settings_dict["tiles_moved"] = 0
    settings_dict["quit_game"][0] = False
    total_score = 0
    settings_dict["pause_time"][0] = INITIALDELAY
    # assign bot variables
    move_hor = True
    direction[0] = 0
    settings_dict["total_score"] = 0
    settings_dict["direction"] = direction
    settings_dict["move_snake"] = True
    settings_dict["tiles_moved"] = 0
    settings_dict["quit_game"] = [False]
    settings_dict["pause_time"][0] = INITIALDELAY
    settings_dict["win"] = False
    settings_dict["move_counter"] = 0
    settings_dict["move_hor"] = move_hor
    settings_dict["previous_dir"] = "None"
    settings_dict["move_toward_apple"] = False
    settings_dict["shorten"] = True
    settings_dict["shortcut_list"] = "None"
    settings_dict["shortcut_list_index"] = 0
    settings_dict["apple_loc_short1"] = "None"
    write_scores(write_turtle,settings_dict)
    # Create a record of apples
    settings_dict["apple_record"] = []
    settings_dict["record_index"] = 0
    return apple_loc,snake_list


# returns alist of directions from the snake head to a location above the apple
        # at the top of the board
def find_shortcut1(snake_list,apple_loc,settings_dict):
    head_loc = snake_list[-1]
    valid_path = True
    path_list = []
    # for every horizontal space between the snake head and apple:
    for hor_val in range(apple_loc[0]-head_loc[0]):
        # no locations in snake_list may have same x-value and be between the head and apple
        if [head_loc[0]+hor_val+1,apple_loc[1]] in snake_list[:-1]:
            valid_path = False
    for ver_val in range((settings_dict["board_height"])-apple_loc[1]):
        if [apple_loc[0],apple_loc[1]+ver_val] in snake_list:
            valid_path = False
    if valid_path:
        # left for the difference in x, y for the dif in height and y-val
        return ([0]*(apple_loc[0]-head_loc[0]))+[90]*(settings_dict["board_height"]-apple_loc[1]-1)
    else:
        return False
        
def check_conditions(snake_list,apple_loc,settings_dict):
    pot_area = (apple_loc[1])*(settings_dict["board_width"]-apple_loc[0])-1
    path_area = int(((settings_dict["board_height"]-1-apple_loc[1])*2+settings_dict["board_height"]-1-apple_loc[0])/POT_APPLE_MULT)-2-POT_APPLES
    possible_extra_area = pot_area-path_area
    if not(apple_loc[1] == snake_list[-1][1] and apple_loc[0]>snake_list[-1][0]\
               and snake_list[-1][1]<settings_dict["board_height"]-1 and settings_dict["shortcut_list"]=="None"\
               and apple_loc[0]!=settings_dict["board_width"]-1):
        return False
    # the area of the rectangle bottom left of the apple must be greater than the snake_list
    if possible_extra_area<=0:
        return False
        #print("not enough area")
    #print("enough area")
    return True

def replay_option(turtle_name,winloss,turtle_name2,settings_dict):
    turtle_name.hideturtle()
    bool_list = ["None"]
    keyboard.add_hotkey('y',play_more,[bool_list,"y"])
    keyboard.add_hotkey('n',play_more,[bool_list,"n"])
    need_input = True
    end_game(turtle_name,turtle_name2,settings_dict)
    turtle_name.hideturtle()
    time.sleep(1)
    turtle.tracer(False)
    turtle_name.up()
    draw_rect(settings_dict["board_width"]*.25*BOXSIZE,settings_dict["board_height"]*.25*BOXSIZE,\
              settings_dict["board_width"]*.5*BOXSIZE,settings_dict["board_height"]*.5*BOXSIZE,REPLAYCOLOR,turtle_name2)
    turtle_name.goto(settings_dict["board_width"]*BOXSIZE*.48-BOXSIZE*.5,(settings_dict["board_height"]-1)*BOXSIZE*.5)
    color = "yellow"
    turtle_name.hideturtle()
    turtle_name2.hideturtle()
    while bool_list==["None"]:
        turtle_name.pencolor(color) # word color
        turtle_name.write("YOU  "+winloss+"\nPlay Again?\n\n     (y/n)",font=(250))
        turtle.tracer(True)
        time.sleep(1)
        turtle_name.clear()
        if color == "yellow":
            color = "red"
        else:
            color = "yellow"
    turtle_name.clear()
    turtle_name2.clear()
    return bool_list[0]
          
def play_more(boolean_list,response):
    if response == "y":
        boolean_list[0] = True
    else:
        boolean_list[0] = False

def quit_game_fun(settings_dict):
    settings_dict["quit_game"][0] = True
        


def write_scores(turtle_name,settings_dict):
    turtle_name.color(TEXTCOLOR)
    turtle_name.hideturtle()
    turtle_name.clear()
    turtle_name.up()
    turtle_name.goto(0,settings_dict["board_height"]*BOXSIZE + BOXSIZE)
    turtle_name.write("Best Score: "+str(settings_dict["best_score"]),font=(30))
    turtle_name.goto(0,settings_dict["board_height"]*BOXSIZE + BOXSIZE*2)
    turtle_name.write("Total Score: "+str(settings_dict["total_score"]),font=(30))


# creates a gameboard containing vertical and horizonal squares
def create_gameboard(turtle_name,settings_dict):
    max_x,max_y = grid_to_screen(settings_dict["board_width"],settings_dict["board_height"])
    turtle.setworldcoordinates(-30,0,max_x+30,max_y+60)
    turtle_name.hideturtle()
    turtle.tracer(False)
    turtle.title(TITLE)
    turtle.bgcolor(COLOR2)
    # create an equation to represent the squares' colors
    for box_number_width in range(settings_dict["board_width"]):
        # for every row:
        for box_number_ver in range(settings_dict["board_height"]):
            # add one to color_num
            # if the number is odd:
            if (box_number_ver+box_number_width)%2==1:
                # the color is grey
                color = COLOR1
            else:
                # the color is white
                color = COLOR2
            #draw the rectangle
            draw_rect(box_number_width*BOXSIZE, box_number_ver*BOXSIZE, \
                      BOXSIZE, BOXSIZE, color,turtle_name)
    turtle_name.hideturtle()

# modified draw_rect function from lab 02
def draw_rect(x, y, x_size, y_size, color,turtle_name):
    # Save current location and state
    # current_position = pos()
    pen_state = turtle_name.pen()
    # Set rectangle colors
    turtle_name.fillcolor(color)
    turtle_name.pencolor(color)
    # Move Turtle to x,y without drawing a line
    turtle_name.up()
    turtle_name.goto(x,y)
    # Draw the rectangle and fill it
    turtle_name.down()
    turtle_name.setheading(90)
    turtle_name.begin_fill()
    turtle_name.forward(x_size)
    turtle_name.right(90)
    turtle_name.forward(y_size)
    turtle_name.right(90)
    turtle_name.forward(x_size)
    turtle_name.right(90)
    turtle_name.forward(y_size)
    turtle_name.end_fill()
    turtle_name.up()
    # Reset position, color, and state
    # goto(current_position)
    turtle_name.pen(pen_state)

# initializes the snake_list
def create_snake(turtle_name,settings_dict):
    snake_list = []
    for snake_location in range(0,SNAKESIZE):
        snake_list.append([snake_location,settings_dict["board_height"]//2])
    draw_snake(snake_list,turtle_name,settings_dict["board_width"])
    return snake_list

# checks to see if the snake is at the border
# if the snake is at the border, the snake stops moving
def check_border(snake_list,direction,settings_dict):
    # if the head is at the border:
    if (snake_list[-1][1] == 0 and direction[0] == 270)\
       or (snake_list[-1][1] == settings_dict["board_height"]-1 and direction[0] == 90) or \
               (snake_list[-1][0] == 0 and direction[0] == 180)\
               or (snake_list[-1][0] == settings_dict["board_width"]-1 and direction[0] == 0):
        return True
    # lost if snake touches it's body
    if snake_list[-1] in snake_list[:-1]:
        return True
    return False

# draws the snake given the snake_list
def draw_snake(snake_list,turtle_name,board_width):
    for location in snake_list[:-1]:
        loc_x,loc_y = grid_to_screen(location[0],location[1])
        draw_rect(loc_x+BOXSIZE*.1,loc_y+BOXSIZE*.1,BOXSIZE*.8,BOXSIZE*.8,\
                  SNAKECOLOR,turtle_name)
    turtle_name.down()
    draw_snake_head(snake_list[-1],0,turtle_name,board_width)
    if DOTS:
        redistribute_dots(snake_list,turtle_name,board_width)

# 'moves' the snake one location
def move_snake_1(snake_list,direction,turtle_name,tail_move,settings_dict):
    turtle.tracer(False)
    previous_loc = snake_list[-1]
    # if the tail shold move:
    # if the location is not outside of the grid:
    if snake_list[0][0]>=0 and snake_list[0][0]<settings_dict["board_width"]:
        # find the color of the inner grid
        color_num = snake_list[0][0]+snake_list[0][1]
    else:
        color_num = "Black"
    if color_num == "Black":
        color = COLOR2
    else:
        if color_num%2==1:
            color = COLOR1
        else:
            color = COLOR2
    if tail_move:#####
        # the replacement color is the 'eveness' of the sum of the rows and columns
        base_x,base_y = grid_to_screen(snake_list[0][0],snake_list[0][1])
        # draw the rectangle
        draw_rect(base_x,base_y,BOXSIZE,BOXSIZE,color,turtle_name)
        # remove the tail of the snake
        #if len(snake_list)==100:## # make longer
        snake_list.pop(0)
    if snake_list[-1][0]>=0 and snake_list[-1][0]<settings_dict["board_width"]:
        color_num = snake_list[-1][0]+snake_list[-1][1]
        if color_num%2==1:
            color = COLOR1
        else:
            color = COLOR2
    else:
        color = COLOR2
    base_x,base_y = grid_to_screen(snake_list[-1][0],snake_list[-1][1])
    draw_rect(base_x,base_y,BOXSIZE,BOXSIZE,color,turtle_name)
    draw_rect(snake_list[-1][0]*BOXSIZE+BOXSIZE/10,snake_list[-1][1]*BOXSIZE+\
              BOXSIZE/10,BOXSIZE*.8,BOXSIZE*.8,SNAKECOLOR,turtle_name)
    if direction[0] == 0:
        snake_list.append([previous_loc[0]+1,previous_loc[1]])
    elif direction[0] == 180:
        snake_list.append([previous_loc[0]-1,previous_loc[1]])
    elif direction[0] == 90:
        snake_list.append([previous_loc[0],previous_loc[1]+1])
    else:
        snake_list.append([previous_loc[0],previous_loc[1]-1])
    if DOTS:
        redistribute_dots(snake_list,turtle_name,settings_dict["board_width"])
    draw_snake_head(snake_list[-1],direction[0],turtle_name,settings_dict["board_width"])

# draws the head of the snake for the given location and direction
def draw_snake_head(location,direction,turtle_name,board_width):
    eye_radius = BOXSIZE/8
    turtle_name.pencolor("white")
    turtle_name.fillcolor("black")
    turtle_name.up()
    loc_x,loc_y = grid_to_screen(location[0],location[1])
    # add the border colors if the location is within the border
    if location[0]>=0 and location[0]<board_width:
        if (location[0]+location[1])%2==1:
            color = COLOR1
        else:
            color = COLOR2
    # else make the outer color black
    else:
        color = COLOR2
    draw_rect(loc_x,loc_y,BOXSIZE,BOXSIZE,color,turtle_name)
    # if moving right or moving down:
    if direction == 90 or direction == 180:
        draw_rect(loc_x+BOXSIZE/2+BOXSIZE*.05,loc_y+BOXSIZE*.05,BOXSIZE/2\
                  *.8,BOXSIZE/2*.8,SNAKECOLOR,turtle_name)
        # lower right eye
        turtle_name.goto(loc_x+BOXSIZE*3/4,location[1]*BOXSIZE+BOXSIZE/8)
        draw_eye(eye_radius,turtle_name)
    if direction == 270 or direction == 180:
        draw_rect(loc_x+BOXSIZE/2+BOXSIZE*.05,loc_y+BOXSIZE/2+BOXSIZE*\
                  .05,BOXSIZE/2*.8,BOXSIZE/2*.8,SNAKECOLOR,turtle_name)
        # upper right eye
        turtle_name.goto(loc_x+BOXSIZE*3/4,loc_y+BOXSIZE*5/8)
        draw_eye(eye_radius,turtle_name)
    if direction == 270 or direction == 0:
        draw_rect(loc_x+BOXSIZE*.05,loc_y+BOXSIZE/2+BOXSIZE*.05,\
                  BOXSIZE/2*.8,BOXSIZE/2*.8,SNAKECOLOR,turtle_name)
        # upper left eye
        turtle_name.goto(loc_x+BOXSIZE*1/4,loc_y+BOXSIZE*5/8)
        draw_eye(eye_radius,turtle_name)  
    if direction == 0 or direction == 90:
        draw_rect(loc_x+BOXSIZE*.05,loc_y+BOXSIZE*.05,BOXSIZE/2*.8,\
                  BOXSIZE/2*.8,SNAKECOLOR,turtle_name)
        # lower left eye
        turtle_name.goto(loc_x+BOXSIZE*1/4,loc_y+BOXSIZE/8)
        draw_eye(eye_radius,turtle_name)
    draw_tongue(location,direction,turtle_name)

# draws a single eye
def draw_eye(eye_radius,turtle_name):
    turtle_name.setheading(0)
    turtle_name.down()
    turtle_name.begin_fill()
    turtle_name.circle(eye_radius)
    turtle_name.end_fill()
    turtle_name.up()

# draws the tongue
def draw_tongue(location,direction,turtle_name):
    turtle_name.up()
    turtle_name.fillcolor("red")
    turtle_name.pencolor("red")
    loc_x,loc_y = grid_to_screen(location[0],location[1])
    if direction == 0:
        # draw the 'body' of the tongue
        draw_rect(loc_x+BOXSIZE*1/2,loc_y+BOXSIZE*3/8,BOXSIZE/4,BOXSIZE/6\
                  ,"red",turtle_name)
        # draw the 'tip' of the tongue
        turtle_name.goto(loc_x+BOXSIZE*4/6,loc_y+BOXSIZE*5/8)
        turtle_name.down()
        turtle_name.begin_fill()
        turtle_name.goto(loc_x+BOXSIZE,loc_y+BOXSIZE)
        turtle_name.goto(loc_x+BOXSIZE*3/4,loc_y+BOXSIZE/2)
        turtle_name.goto(loc_x+BOXSIZE,loc_y)
        turtle_name.goto(loc_x+BOXSIZE*2/3,loc_y+BOXSIZE*3/8)
        turtle_name.goto(loc_x+BOXSIZE*2/3,loc_y+BOXSIZE*5/8)
        turtle_name.end_fill()
    if direction == 90:
        # draw the 'body' of the tongue
        draw_rect(loc_x+BOXSIZE*3/8,loc_y+BOXSIZE*1/2,BOXSIZE/6,BOXSIZE/4,\
                  "red",turtle_name)
        # draw the 'tip' of the tongue
        turtle_name.goto(loc_x+BOXSIZE*5/8,loc_y+BOXSIZE*4/6)
        turtle_name.down()
        turtle_name.begin_fill()
        turtle_name.goto(loc_x+BOXSIZE,loc_y+BOXSIZE)
        turtle_name.goto(loc_x+BOXSIZE/2,loc_y+BOXSIZE*3/4)
        turtle_name.goto(loc_x,loc_y+BOXSIZE)
        turtle_name.goto(loc_x+BOXSIZE*3/8,loc_y+BOXSIZE*2/3)
        turtle_name.goto(loc_x+BOXSIZE*5/8,loc_y+BOXSIZE*2/3)
        turtle_name.end_fill()
    if direction == 180:
        # draw the 'body' of the tongue
        draw_rect(loc_x+BOXSIZE*2/6,loc_y+BOXSIZE*3/8,BOXSIZE/4,BOXSIZE/6,\
                  "red",turtle_name)
        # draw the 'tip' of the tongue
        turtle_name.goto(loc_x+BOXSIZE*2/6,loc_y+BOXSIZE*3/8)
        turtle_name.down()
        turtle_name.begin_fill()
        turtle_name.goto(loc_x,location[1]*BOXSIZE)
        turtle_name.goto(loc_x+BOXSIZE/4,loc_y+BOXSIZE/2)
        turtle_name.goto(loc_x,loc_y+BOXSIZE)
        turtle_name.goto(loc_x+BOXSIZE*2/6,loc_y+BOXSIZE*5/8)
        turtle_name.goto(loc_x+BOXSIZE*2/6,loc_y+BOXSIZE*3/8)
        turtle_name.end_fill()
    if direction == 270:
        # draw the 'body' of the tongue
        draw_rect(loc_x+BOXSIZE*3/8,loc_y+BOXSIZE*2/6,BOXSIZE/6,BOXSIZE/4,\
                  "red",turtle_name)
        # draw the 'tip' of the tongue
        turtle_name.goto(loc_x+BOXSIZE*3/8,loc_y+BOXSIZE*2/6)
        turtle_name.down()
        turtle_name.begin_fill()
        turtle_name.goto(loc_x,loc_y)
        turtle_name.goto(loc_x+BOXSIZE/2,loc_y+BOXSIZE/4)
        turtle_name.goto(loc_x+BOXSIZE,loc_y)
        turtle_name.goto(loc_x+BOXSIZE*5/8,loc_y+BOXSIZE*2/6)
        turtle_name.goto(loc_x+BOXSIZE*3/8,loc_y+BOXSIZE*2/6)
        turtle_name.end_fill()

# convert grid coordinates to screen coordinates
def grid_to_screen(grid_x,grid_y):
    return grid_x*BOXSIZE,grid_y*BOXSIZE

# creates dots distributed from the head of the snake to the tail
def redistribute_dots(snake_list,turtle_name,board_width):
    # for every location in the snake:
    # iterate from head to tail
    turtle.tracer(False)
    color = DOT_COLOR1
    for location in snake_list[-2::-1]:
        # change the color every three locations
        if color == DOT_COLOR1:
            color = DOT_COLOR2
        elif color == DOT_COLOR2:
            color = DOT_COLOR3
        else:
            color = DOT_COLOR1
        turtle_name.up()
        loc_x,loc_y = grid_to_screen(location[0],location[1])
        turtle_name.goto(loc_x+BOXSIZE/2,loc_y+BOXSIZE/2)
        turtle_name.down()
        turtle_name.dot(350/board_width,color)
        if color != SNAKECOLOR:
            turtle_name.dot(250/board_width,MIDDOT_COLOR)
            turtle_name.dot(125/board_width,CENTERDOT_COLOR)

def generate_apple(snake_list,turtle_name,settings_dict):
    turtle.update()
    apple_gen=False
    while not apple_gen:
        random_height = random.randint(0,settings_dict["board_height"])%settings_dict["board_height"]
        random_width = random.randint(0,settings_dict["board_width"])%settings_dict["board_width"]
        location = [random_width,random_height]
        #if random.randint(1,4)==2:
            #location = [1,settings_dict["board_height"]-1]
        if settings_dict["man_apple"][0]:
            valid_loc = False
            loc_x = "Hello"
            loc_y = "Hello"
            while True:
                try:
                    loc_x= int(input("Type an apple location x: "))
                    break
                except:
                    ValueError
            while True:
                try:
                    loc_y= int(input("Type an apple location y: "))
                    break
                except:
                    ValueError
            location = [loc_x,loc_y]
        if location not in snake_list:
            draw_apple(location,turtle_name)
            apple_gen = True
        if len(snake_list)==settings_dict["board_height"]*settings_dict["board_width"]:
            apple_gen = True
    settings_dict["apple_record"].append(location)
#################################
    # use previous apple records
    if settings_dict["usable_record"]:
        if settings_dict["record_index"]==len(settings_dict["usable_record"]):
            print("started generating new apples")
            time.sleep(5)
        if settings_dict["record_index"]<=len(settings_dict["usable_record"])-1:
            location = settings_dict["usable_record"][settings_dict["record_index"]]
    
        if location in snake_list[:-2]:
            print("The apple was generated inside the snake")
            time.sleep(60)
    settings_dict["record_index"] += 1
    return location

def draw_apple(location, turtle_name):
    # outline in black
    turtle_name.pencolor("black")
    turtle.tracer(False)
    turtle_name.up()
    loc_x,loc_y = grid_to_screen(location[0],location[1])
    center_x = loc_x+BOXSIZE/2
    center_y = loc_y + BOXSIZE/2
    turtle_name.goto(center_x,center_y)
    # draw the stems
    turtle_name.down()
    # face upward
    turtle_name.setheading(90)
    # drraw the 1/4 circle of radius = half the boxsize
    turtle_name.begin_fill()
    turtle_name.fillcolor("green")
    turtle_name.circle(BOXSIZE/2,90)
    turtle_name.goto(center_x,center_y)
    turtle_name.setheading(270)
    turtle_name.circle(BOXSIZE/2,-90)
    turtle_name.end_fill()
    turtle_name.goto(center_x,center_y)
    turtle_name.begin_fill()
    turtle_name.setheading(0)
    turtle_name.circle(BOXSIZE/2,90)
    turtle_name.goto(center_x,center_y)
    turtle_name.setheading(0)
    turtle_name.circle(BOXSIZE/2,-90)
    turtle_name.end_fill()
    # draw the base of the apple
    turtle_name.up()
    turtle_name.goto(loc_x+BOXSIZE/2,loc_y)
    turtle_name.down()
    turtle_name.setheading(0)
    turtle_name.fillcolor("red")
    turtle_name.begin_fill()
    turtle_name.circle(BOXSIZE*.70/2)
    turtle_name.end_fill()
#    turtle.update()

def end_game(turtle_name,turtle_name2,settings_dict):
    snake_size = 5
    list_of_snakes = []
    # for every other square in the height
    for snake_num in range(settings_dict["board_height"]//2):
        # create a list for that snake
        snake_list = []
        for snake_box in range(snake_size):
            # increase x-vals by 1 for each snake_box and 1 for each snake(max at center)
            snake_list.append([snake_box+-2*abs(snake_num-settings_dict["board_height"]//4)-snake_size-\
                               settings_dict["board_height"]//2+2,snake_num*2])
        list_of_snakes.append(snake_list)
        draw_snake(snake_list,turtle_name,settings_dict["board_width"])
        # append a 'snake' to the list_of_snakes
    # copy the above, except multiply increase the x-values by the width of the screen
        # increase y-locations by +1(alteranate snakes)
    list_of_snakes2 = []
    # for every other square in the height
    for snake_num in range(settings_dict["board_height"]//2):
        # create a list for that snake
        snake_list = []
        for snake_box in range(snake_size):
            # increase x-vals by 1 for each snake_box and 1 for each snake(max at center)
            snake_list.append([2*abs(snake_num-settings_dict["board_height"]//4)-snake_box+settings_dict["board_width"]+\
                               snake_size+settings_dict["board_height"]//2-3,snake_num*2+1])
        # append the 'snake' to the list_of_snakes
        list_of_snakes2.append(snake_list)
        draw_snake(snake_list,turtle_name,settings_dict["board_width"])
    # for every square the snakes will move:
    for movement_num in range(settings_dict["board_width"]*2+snake_size):
        for snake in list_of_snakes:
            # move the snake 'non-normal'
            move_snake_1(snake,[0],turtle_name,True,settings_dict)
            # draw the black rectangles with turtle2
            loc_x,loc_y=grid_to_screen(snake[0][0]-1,snake[0][1])
            draw_rect(loc_x,loc_y,BOXSIZE,BOXSIZE,COLOR2,turtle_name2)
        # copy the above, except reverse direction
        for snake in list_of_snakes2:
            # move the snake 'non-normal'
            move_snake_1(snake,[180],turtle_name,True,settings_dict)
            # draw the black rectangles with turtle2
            loc_x,loc_y=grid_to_screen(snake[0][0]+1,snake[0][1])
            draw_rect(loc_x,loc_y,BOXSIZE,BOXSIZE,COLOR2,turtle_name2)
        # redraw the snakes every 3 iterations
        if movement_num%3 == 0:
            turtle_name.clear()
            for snake in list_of_snakes:
                draw_snake(snake,turtle_name,settings_dict["board_width"])
                draw_snake_head(snake[-1],0,turtle_name,settings_dict["board_width"])
            for snake in list_of_snakes2:
                draw_snake(snake,turtle_name,settings_dict["board_width"])
                draw_snake_head(snake[-1],180,turtle_name,settings_dict["board_width"])
        turtle.update()

main()
