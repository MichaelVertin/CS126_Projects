# This program is based off my previous 'self_san_snake'. 
# rather than creating multiple functions that allow the snake the snake to 
  # take certain paths when conditions were met, the direction is determined 
  # by first calculating which of 4 directions (left, right, up, down), are 
  # blocked. Of the possible options, the snake will determine which path
  # will produce the quickest path to the apple. 
# compared to the original 'self_ran_snake', the algorithm process of snake's direction
  # significantly simpler, although it is less efficient because this snake
  # currently only calculates the best path up to one square in advance. 
# the code for this snake is slightly longer, although 300 lines are only to 
  # create the main path

import math
import turtle
import sys
import time
import keyboard
import random
import pdb ###
POT_APPLES_BOARD = -.9 # closer to 0 means the board_size has smaller impact
EMPTY_AREA_POWER = .2 # reduces the effect of ratio of board_size to empty_area
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
DOT_COLOR4 = "green"
MIDDOT_COLOR = "black"
CENTERDOT_COLOR = "red"
INITIALDELAY = .00 # Initial Time
DELAYMOD = .8
REPLAYCOLOR = "blue"
SCOREINCREMENT = 10
DOTS = False
TEXTCOLOR = "white"
SHORT_MULT = .75
SHORT_SUB = 0
POT_APPLES = 4 # snake can only eat apples until it starts following the tail
REMOVE_SHORTCUT1 = False
POT_APPLE_MULT = 1.2
END_GAME_MESSAGE = False

# the main game
def main():
    turty,replay_turtle,board_turtle,write_turtle,\
            replay_turtle2,direction,settings_dict = before_game_begins()
    initialize_dir_list(settings_dict)
    while settings_dict["play_again"]:
        settings_dict["num_games"] += 1
        print("\n\n\n\nGame Number ",settings_dict["num_games"],":",sep="")
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
        turty.clear()
    turtle.bye()

    
    
# create the initial_dir_list
def initialize_dir_list(settings_dict):
    standard_directions = []
    width_list_sect1 = []
    width_list_sect2 = []
    width_list_sect3 = []
    for iteration in range(settings_dict["board_height"]):
        extra_width = settings_dict["board_width"]-3
        width_constant = extra_width*2/3
        width2 = math.floor(extra_width-width_constant)
        width1 = math.ceil(width_constant)
        width_list_sect1.append(width1)
        width_list_sect3.append(3)
        width_list_sect2.append(width2)
        #print(f'1: {width_list_sect2[0]},  2: {width_list_sect3[0]},  3: {width_list_sect1[0]}')
    # starting at bottom, moving left
    result_list = create_list_bottom_constants(width_list_sect2[0],width_list_sect3[0],width_list_sect1[0])
    standard_directions += result_list
    result_list = create_list_sect1(width_list_sect1[3:-3],settings_dict["board_height"]-6)
    standard_directions += result_list
    result_list = create_list_NE_constants(width_list_sect2[0],width_list_sect3[0],width_list_sect1[0])
    standard_directions += result_list
    result_list = create_list_sect3(width_list_sect3,settings_dict["board_height"]-6)
    standard_directions += result_list
    result_list = create_list_NW_constants(width_list_sect2[0],width_list_sect3[0],width_list_sect1[0])
    standard_directions += result_list
    result_list = create_list_sect2(width_list_sect2[0],settings_dict["board_height"]-6)
    standard_directions += result_list
    standard_directions.append(270)
    settings_dict["standard_locations"] = create_location_list(standard_directions,[0,1])
    settings_dict["standard_dir_list"] = standard_directions
    return result_list

def create_list_sect1(width_list,sect_height):
    #print("sect_height = ",sect_height)
    return_list = []
    width_index = 0
    for row_group in range(sect_height//4):
        result_list = create_double_bar_sect1(width_list[width_index])
        return_list += result_list
        width_index += 4
    if len(width_list)%4 == 2:
        width_index -= 2
        return_list += create_single_bar_sect1(width_list[width_index])
    return return_list

def create_single_bar_sect1(width):
    dir_list = []
    for val in range(width-1):
        dir_list.append(180)
    dir_list.append(90)
    for val in range(width-1):
        dir_list.append(0)
    dir_list.append(90)
    return dir_list
    
def create_double_bar_sect1(width):
    # create a list of directions
    dir_list = []
    # for the length of the width - 1:
    for val in range(width-1):
        # add 180 to the list
        dir_list.append(180)
    # add 90
    dir_list.append(90)
    # for the length of the width - 3:
    for val in range(width-3):
        # add 0
        dir_list.append(0)
    # add 90
    dir_list.append(90)
    # for the length of the width - 3:
    for val in range(width-3):
        # add 180
        dir_list.append(180)
    # add 90
    dir_list.append(90)
    # for the length of the width - 2:
    for val in range(width-2):
        # add 0
        dir_list.append(0)
    # add 270
    dir_list.append(270)
    # add 270
    dir_list.append(270)
    # add 0
    dir_list.append(0)
    # add 90
    dir_list.append(90)
    # add 90
    dir_list.append(90)
    dir_list.append(90)
    # return the direction list
    return dir_list
    
def create_list_sect3(width_list,height):
    # create a list of directions
    return_list = []
    return_list.append(270)
    width_index = len(width_list)-1
    # initially orientated "zero"
    orientation_val = 0
    option = 0
    for row_group in range(height//2-1):
        if option%2 == 0:
            result_list = create_double_bar_sect3_down(width_list[width_index],orientation_val,270)
            return_list += (result_list)
        else:
            return_list.append(270)
            return_list.append(270)
        option += 1
        width_index -= 1
    orientation_val = 180
    return_list += create_end_bar_sect3(width_list[width_index],180)
    width_index = 0
    for row_group in range(height//2):
        if option%2 == 0:
            result_list = create_double_bar_sect3_down(width_list[width_index],orientation_val,90)
            return_list += result_list
        else:
            return_list.append(90)
            return_list.append(90)
        width_index +=1
        option += 1
    return return_list

def create_double_bar_sect3_down(width,orientation,direction):
    # create a list of directions
    dir_list = []
    for val in range(width-2):
        dir_list.append((180+orientation)%360)
    dir_list.append(direction)
    for val in range(width-2):
        dir_list.append(0+orientation)
    dir_list.append(direction)
    return dir_list
    
def create_end_bar_sect3(width,direction):
    dir_list = []
    for val in range(width-1):
        dir_list.append(180)
    dir_list.append(90)
    return dir_list

def create_list_bottom_constants(width_1,width_2,width_3):
    dir_list = []
    dir_list.append(270)
    dir_list.append(0)
    for val in range((width_1-1)//2):
        dir_list += bottom_create_bar(3)
    # if the first width is even and the total width is even:
        # need to "add" an extra row
            # remove the previous row
            # add a "squiggle_row"
    if (width_1+width_2+width_3)%2==0:
        if width_1%2 == 0:
            # remove the last 3 parts
            dir_list = dir_list[:-3] # Maybe 4?
            # move 1 right,1 down, 1 left, 1 down, 2 right
            dir_list.append(0)
            dir_list.append(270)
            dir_list.append(180)
            dir_list.append(270)
            dir_list.append(0)
            dir_list.append(0)
        else:
            # remove the last two
            dir_list = dir_list[:-9]
            # move 1 right,1 down, 1 left, 1 down, 2 right
            dir_list.append(0)
            dir_list.append(270)
            dir_list.append(180)
            dir_list.append(270)
            dir_list.append(0)
            dir_list.append(0)
    dir_list.append(90)
    dir_list.append(90)
    for val in range(width_2-1):
        dir_list.append(0)
    dir_list.append(270)
    for val in range(width_2-2):
        dir_list.append(180)
    dir_list.append(270)
    for val in range(width_2-2):
        dir_list.append(0)
    dir_list.append(0)
    for iteration in range((width_3)//2):
        dir_list += bottom_create_bar(3)
    if ((width_3))==0:
        dir_list += draw_squiggle()
    else:
        dir_list.append(90)
        dir_list.append(90)
        dir_list.append(90)
    return dir_list

def draw_squiggle():
    dir_list = []
    dir_list.append(0)
    dir_list.append(90)
    dir_list.append(180)
    dir_list.append(90)
    dir_list.append(0)
    dir_list.append(90)
    return dir_list

def draw_squiggle_top():
    dir_list = []
    dir_list.append(180)
    dir_list.append(270)
    dir_list.append(0)
    dir_list.append(270)
    dir_list.append(180)
    dir_list.append(270)
    return dir_list

    
def bottom_create_bar(height):
    dir_list = []
    for y_val in range(height-1):
        dir_list.append(90)
    dir_list.append(0)
    for y_val in range(height-1):
        dir_list.append(270)
    dir_list.append(0)
    return dir_list
    
def create_list_NE_constants(width1,width2,width3):
    # dtermine the lengths of the two sections
    len_sect_1 = (width3+1)//2
    len_sect_2 = (width3+1)//2
    if (width3+1)%2 == 1:
        len_sect_2 += 1
    dir_list = []
    # move to top
    for val in range(2):
        dir_list.append(90)
    # move to 
    for val in range(len_sect_1-1):
        dir_list.append(180)
    dir_list.append(270)
    for val in range(len_sect_1-2):
        dir_list.append(0)
    dir_list.append(270)
    for val in range(len_sect_1-2):
        dir_list.append(180)
    dir_list.append(180)
    dir_list.append(90)
    dir_list.append(90)
    for val in range(len_sect_2-1):
        dir_list.append(180)
    dir_list.append(270)
    for val in range(len_sect_2-2):
        dir_list.append(0)
    dir_list.append(270)
    for val in range(len_sect_2-2):
        dir_list.append(180)
    dir_list.append(270)
    return dir_list

def create_list_NW_constants(width1,width2,width3):
    # create a direction list
    dir_list = []
    for val in range(width2-2):
        dir_list.append(0)
    dir_list.append(90)
    for val in range(width2-2):
        dir_list.append(180)
    dir_list.append(180)
    for val in range((width1-1)//2):
        dir_list += create_bar_top(3)
    if width1%2 == 1:
        dir_list.append(270)
        dir_list.append(270)
        dir_list.append(270)
    else:
        dir_list += draw_squiggle_top()
    return dir_list

def create_bar_top(height):
    dir_list = []
    for val in range(height-1):
        dir_list.append(270)
    dir_list.append(180)
    for val in range(height-1):
        dir_list.append(90)
    dir_list.append(180)
    return dir_list
        
    
def create_list_sect2(width,height):
    dir_list = []
    for bar in range(height//2):
        result = create_bar_sect2(width)
        dir_list += result
    return dir_list
        
    
    
def create_bar_sect2(width):
    dir_list = []
    for val in range(width-1):
        dir_list.append(0)
    dir_list.append(270)
    for val in range(width-1):
        dir_list.append(180)
    dir_list.append(270)
    return dir_list
    
    

def create_location_list(dir_list,init_loc):
    location_list = [init_loc.copy()]
    for element in dir_list:
        # move one forward
        if element%360 == 0:
            location_list.append([location_list[-1][0]+1,location_list[-1][1]])
        elif element%360 == 90:
            location_list.append([location_list[-1][0],location_list[-1][1]+1])
        elif element%360 == 180:
            location_list.append([location_list[-1][0]-1,location_list[-1][1]])
        elif element%360 == 270:
            location_list.append([location_list[-1][0],location_list[-1][1]-1])
        else:
            print("Invalid direction")
            raise ValueError
    return location_list
    










###########################################################################
#                          SHORTEN FUNCTIONS                              #
###########################################################################
# given the current index of the head, tail, apple, and desired location:
# determine if the head can move paths
def det_legal_switch(desired_ind,pot_apples,board_size,location_list,snake_list):
    blocking_index = find_blocking_part(snake_list,location_list,board_size,desired_ind)
    path_distance = blocking_index-desired_ind
    if path_distance<0:
        path_distance += board_size
    # if the "path_distance" between the desired_location and tail is less than POT_APPLES:
    if path_distance<=(pot_apples):
        # the path cannot be taken
        return False
    # else:
    else:
        # the path can be taken
        return True
    
    

# given a location and the standard_locations:
# determine potential indeces that are exactly on "direct_motion" away from the location
def det_switch_indices(location,location_list):
    loc_x = location[0]
    loc_y = location[1]
    loc1 = [loc_x+1,loc_y]
    loc2 = [loc_x,loc_y+1]
    loc3 = [loc_x,loc_y-1]
    loc4 = [loc_x-1,loc_y]
    indices = []
    for loc_val in [loc1,loc2,loc3,loc4]:
        # only append if the location is in the location_list
        if loc_val in location_list:
            indices.append(location_list.index(loc_val))
    return indices

# determine the direction of the snake
def get_direction(snake_list,apple_loc,settings_dict,direction,pot_apples):
    board_size = settings_dict["board_height"]*settings_dict["board_width"]
    location_list = settings_dict["standard_locations"]
    direction_list = settings_dict["standard_dir_list"]
    # find the index of the snake_head and snake_tail and apple_loc
    head_index = location_list.index(snake_list[-1])
    tail_index = location_list.index(snake_list[0])
    apple_index = location_list.index(apple_loc)
    # determine potential indeces for snake
    pot_indices = det_switch_indices(snake_list[-1],location_list)
    # determine if the switches are legal
    pot2_indices = []
    for index in pot_indices:
        valid_index = det_legal_switch(index,pot_apples,board_size,location_list,snake_list)
        if valid_index:
            pot2_indices.append(index)
    smallest_index = det_smallest_path(pot2_indices,location_list,apple_index,settings_dict)
    if smallest_index:
        # determine which direction can get to the location of the smallest_index
        # return which path has the smallest distance to the apple
        direction[0] = det_dir_to_get_to_loc(snake_list[-1],location_list[smallest_index])
    else:
        direction[0] = direction_list[location_list.index(snake_list[-1])]

def det_dir_to_get_to_loc(init_loc,final_loc):
    if init_loc[0] == final_loc[0]+1:
        return 180
    if init_loc[0] == final_loc[0]-1:
        return 0
    if init_loc[1] == final_loc[1]+1:
        return 270
    if init_loc[1] == final_loc[1]-1:
        return 90
    raise ValueError
    
def det_smallest_path(indices,location_list,apple_index,settings_dict):
    smallest_index = False
    smallest_path = len(location_list)
    for index in indices:
        location = location_list[index]
        current_distance = apple_index - index
        # determine the distance
        if current_distance<0:
            current_distance += settings_dict["board_width"]*settings_dict["board_height"]
        if current_distance<smallest_path:
            smallest_path = current_distance
            smallest_index = index
    return smallest_index
        
def calc_pot_apples(snake_list,settings_dict):
    board_size = (settings_dict["board_height"]*settings_dict["board_width"])
    empty_area = board_size-len(snake_list)
    # the "potential apples" will increase as the board size decreases
    board_mult = board_size**(POT_APPLES_BOARD)
    # as empty area decreases, the multiplier increases
    empty_mult = (board_size/empty_area)**EMPTY_AREA_POWER
    return_result = settings_dict["board_height"]+settings_dict["board_width"]
    return_result = (settings_dict["board_height"]+settings_dict["board_width"])                     
    #return_result = len(snake_list)//2
    return return_result
    #return board_mult*empty_mult



    
def find_blocking_part(snake_list,location_list,board_size,start_index):
    found_part = False
    index = start_index - 1
    while not found_part:
        index = (index + 1)%len(location_list)
        if location_list[index] in snake_list:
            found_part = True
    return index
        









##########################################################################
def play_instance_of_game(apple_loc,snake_list,settings_dict,direction,\
                turty,replay_turtle,board_turtle,write_turtle,replay_turtle2):
    while settings_dict["move_snake"]: # while the snake is moving...
        ##########################################
        pot_apples = calc_pot_apples(snake_list,settings_dict)
        # get the direction
        get_direction(snake_list,apple_loc,settings_dict,direction,pot_apples)
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
    print("GAME OVER")
    print_stats(settings_dict)
    turtle.update()
    if not settings_dict["win"]:
        while not settings_dict["quit_game"][0]:
            if not settings_dict["quit_game"][0]:
                time.sleep(1)
    turtle.tracer(False)
    if settings_dict["usable_record"]:
        settings_dict["play_again"] = False

def print_stats(settings_dict):
    print("apple_record =\n\n",settings_dict["apple_record"])
    settings_dict["total_tiles"] += settings_dict["tiles_moved"]
    average_tiles = settings_dict["total_tiles"]/settings_dict["num_games"]
    print("average_tiles = ",average_tiles)

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
        board_width = 9
        board_height = 8
    else:
        board_width = int(sys.argv[1])
        if board_width%2 == 0:
            if board_width < 16:
                print("board_width cannot be an even value less than 16")
                board_width += 1
        if board_width%2 == 1:
            if board_width < 9:
                print("board_width cannot be less than 9")
                board_width  = 9
        board_height = int(sys.argv[2])
        if board_height < 8:
            print("board_height cannot be less than 8")
            board_height = 8
        if board_height%2 == 1:
            print("board_height cannot be odd")
            board_height += 1
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
    settings_dict["usable_record"] = False# [[3, 1], [3, 2], [0, 4], [0, 3], [0, 0], [0, 4], [2, 1], [5, 5], [0, 5], [3, 4], [3, 1], [2, 0], [3, 5], [5, 5], [3, 4], [0, 0], [1, 1], [5, 5], [4, 0], [2, 0], [0, 5], [2, 5], [2, 2]]
    
    settings_dict["record_index"] = 0
    settings_dict["total_tiles"] = 0
    settings_dict["num_games"] = 0
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
    if random.randint(1,UPDATE_VAL) == 1:
        turtle.update()
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

def check_conditions(snake_list,apple_loc,settings_dict):
    pot_area = (apple_loc[1])*(settings_dict["board_width"]-apple_loc[0])-1
    path_area = int(((settings_dict["board_height"]-1-apple_loc[1])*2+settings_dict["board_height"]-1-apple_loc[0])/POT_APPLE_MULT)-2-POT_APPLES
    possible_extra_area = pot_area-path_area
    if not(apple_loc[1] == snake_list[-1][1] and apple_loc[0]>snake_list[-1][0]\
               and snake_list[-1][1]<settings_dict["board_height"]-1 and settings_dict["shortcut_list"]=="None"\
               and apple_loc[0]!=settings_dict["board_width"]-1):
        return False
    if possible_extra_area<=0:
        return False
    return True

def replay_option(turtle_name,winloss,turtle_name2,settings_dict):
    time.sleep(1)
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
        snake_list.append([snake_location,0])
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
    alternator = True
    for location in snake_list[-2::-1]:
        # change the color every three locations
        if alternator:
            color = DOT_COLOR1
            alternator = False
        elif color == DOT_COLOR1:
            color = DOT_COLOR2
        elif color == DOT_COLOR2:
            color = DOT_COLOR3
        elif color == DOT_COLOR3:
            color = DOT_COLOR4
            alternator = True
        
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
