import discord
import json
import asyncio
from discord.ext import commands
import requests.packages.urllib3
import xml
import xml.etree.ElementTree as ET 
import random
#import discord.ext import commands
import os
import traceback
import tkinter as tk
import sys
import datetime, time
from dotenv import load_dotenv
load_dotenv()
 
# ------------ Admin args
admin_discord_handle = ""
bot_username = ""
# ------------ Discord Client Setup
requests.packages.urllib3.disable_warnings()
intents = discord.Intents.default()
intents.message_content = True
#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix = '!', intents=intents)
discotoken = os.getenv('discordtoken')

# ------------- Brandi vars and funcs
# mojis
square_b = ":on:" # low character limit alternative for testing
#square_b = ":black_circle:"
emoji_up = ":arrow_up:"
emoji_right = ":arrow_right:"
emoji_down = ":arrow_down:"
emoji_left = ":arrow_left:"

class marble_data():
    marble_id = 0
    marble_pid = 0
    marble_origin = 0
    marble_location = 0
    marble_locked = True
    marble_home = True
    marble_emoji_temp = None
    marble_owner = None
    def __init__(self, marb_id, marb_loc, marb_pid, marble_owner):
        #pid is in a bad order because I didn't add it until later
        # don't wanna refactor that right now
        # I also put in owner instead of pid (player id) later because I wanted to get more useful information
        # and not have to jump through hoops to find the player object
        # someday I'll trim this shit down
        self.marble_id = marb_id
        self.marble_pid = marb_pid
        self.marble_location = marb_loc
        self.marble_origin = marb_loc
        self.marble_locked = True
        self.marble_home = True
        self.marble_emoji_temp = None
        self.marble_owner = marble_owner
    
    def start_marble(self, starting_spot):
        self.marble_location = starting_spot
        landing_spot = game_manager.board_state[starting_spot]
        if landing_spot.marble is not None:
            if landing_spot.marble.marble_locked:
                print("this case should hit if a player is trying to start a marble on top of their own marble")
                print("but I should still stop this at move predictor")
                raise Exception("start_marble - starting on top of a started")
            landing_spot.marble.reset_marble()
        landing_spot.marble = self
        self.marble_locked = True
        self.marble_home = False          
    
    def set_marble(self, new_location, final_zone=False):
        self.marble_location = new_location
        self.marble_locked = final_zone
        self.marble_home = False
        
    def reset_marble(self):
        self.marble_location = self.marble_origin
        self.marble_locked = True
        self.marble_home = True
    
    def move_marble_to_location(self, newlocation):
        leaving_spot = game_manager.board_state[self.marble_location]
        leaving_spot.marble = None        
        self.marble_location = newlocation
        self.marble_home = False
        if isinstance(newlocation, str):
            # the marble has moved into a home spot
            # hopefully I didn't try to move it home like that (use resetmarble)            
            self.marble_locked = True
        elif isinstance(newlocation, int):
            # check landing spot
            self.marble_locked = False            
            landing_spot = game_manager.board_state[newlocation]
            if landing_spot.marble is not None:
                if landing_spot.marble.marble_locked:
                    print("move_marble - I did something stupid, move predictor should have stopped moving onto a locked marble")
                    raise Exception("move_marble - I did something stupid, move predictor should have stopped moving onto a locked marble")
                landing_spot.marble.reset_marble()
        else:
            # I did something dumb
            print("move_marble - I did something stupid, new spot is not valid type")
            raise Exception("move_marble - I did something stupid, new spot is not valid type")                    
        landing_spot.marble = self
        
        

class player_data():
    player_num = ""
    player_name = ""
    player_hand = []
    player_home_marble = 4 # this might be unnecassary
    player_home_location = 0
    player_emoji = ""
    player_marbles = []
    player_hand_view = None
    playerping = None
    handswap = None
    
    def __init__(self, p_num, p_name, p_emoji=None):
        # player order matters here - 1 3 2 4
        self.handswap = None
        self.playerping = None
        self.player_num = p_num
        if self.player_num == 2:
            self.player_home_location = 32
        elif self.player_num == 3:
            self.player_home_location = 16
        elif self.player_num == 4:
            self.player_home_location = 48
        self.player_name = p_name
        self.player_hand = list([])
        self.player_home_marble = 4
        self.player_marbles = [marble_data(1,"P{}1".format(p_num),p_num,self),
                               marble_data(2,"P{}2".format(p_num),p_num,self),
                               marble_data(3,"P{}3".format(p_num),p_num,self),
                               marble_data(4,"P{}4".format(p_num),p_num,self)]
        player_hand_view = None
        if p_emoji is None:
            self.player_emoji = [":orange_circle:",":blue_circle:",":purple_circle:",":green_circle:"][p_num-1]
        else:
            self.player_emoji = p_emoji
    
    def start_marble(self):
        errorFlag = True
        for mymarble in self.player_marbles:
            if mymarble.marble_home == True:
                mymarble.marble_home = False
                mymarble.marble_location = self.player_home_location
                mymarble.marble_locked = True
                errorFlag = False
                break
        if errorFlag:
            print("Something bad happened in start_marble")
        
    def move_marble_dist(self, marblenum, move_distance):
        #this is gonna be obsolete soon
        if marblenum <= 0:
            marblenum = 0
        elif marblenum >= 3:
            marblenum = 3
        new_location = self.player_marbles[marblenum].marble_location + move_distance
        if new_location >= 64:
            new_location -= 64        
        self.player_marbles[marblenum].set_marble(new_location, False)
        #if marblenum+1 <= len(self.player_marble_location):
            #new_location = self.player_marble_location[marblenum] + move_distance
            #if new_location >= 64:
                #new_location -= 64
            #self.player_marble_location[marblenum] = new_location
    
    def move_marble_to_location(self, marblenum, newlocation):
        # why did I even put this in player data? I think I'm going to make another one in the marble object
        return

# TODO: this shouldn't be here. Should init with game
player_one = player_data(1, "")
player_two = player_data(2, "")
player_three = player_data(3, "")
player_four = player_data(4, "")
game_manager = None

def assign_player(playervar, playername, playerping):
    if playervar is not None:
        if playervar.player_name == playername:
            playervar.player_name = ""
            playervar.playerping = playerping
        elif playervar.player_name == "":
            playervar.player_name = playername
            playervar.playerping = playerping
    playerliststring = ""
    
    if player_one.player_name:
        playerliststring += "{} claimed P1".format(player_one.player_name)
    else:
        playerliststring += "Empty P1"
        
    if player_two.player_name:
        playerliststring += "\n{} claimed P2".format(player_two.player_name)
    else:
        playerliststring += "\nEmpty P2"
    
    if player_three.player_name:
        playerliststring += "\n{} claimed P3".format(player_three.player_name)
    else:
        playerliststring += "\nEmpty P3"
    
    if player_four.player_name:
        playerliststring += "\n{} claimed P4".format(player_four.player_name)
    else:
        playerliststring += "\nEmpty P4"
    
    return playerliststring

class boardspace():
    flow = 1
    space_num = 0
    next_space = None # TIL all objects of a class will share arrays/lists set here
    graphic_blank = ""
    graphic_move = ""
    graphic_set = ""
    goal_space = 0
    marble = None
    def __init__(self, space_num, direction, goal_space):
        self.next_space = list() #making a new list here makes them individual per object
        self.flow = 1
        self.space_num = 0
        self.graphic_blank = ""
        self.graphic_move = ""
        self.graphic_set = ""
        self.goal_space = 0
        self.marble = None
        if goal_space == 0:
            self.graphic_blank = ":white_circle:"
        else:
            self.graphic_blank = ":o:"
        self.graphic_set = self.graphic_blank
        self.space_num = space_num
        nextspace = None
        if isinstance(space_num, str) and space_num[2:] != "4":
            nextspace = space_num[:2] + str(int(space_num[2:]) + 1)
        elif isinstance(space_num, str):
            # does end in 4
            nextspace = None
        else:
            nextspace = space_num + 1
            if nextspace >= 64:
                nextspace -= 64
        self.next_space.append(nextspace)
        self.set_direction(direction)
        self.goal_space = goal_space
        # goal spaces are 0, 16, 32, 48
        # todo: settle on a proper annocation for goal spaces
        if space_num == 0:
            self.next_space.append("G11")
        elif space_num == 16:
            self.next_space.append("G31")
        elif space_num == 32:
            self.next_space.append("G21")
        elif space_num == 48:
            self.next_space.append("G41")
        #print("boardspace {} init result: goal:{} next:{}".format(self.space_num, self.goal_space, self.next_space))
    
    def set_direction(self, direction):
        self.flow = direction
        if direction == 1:
            self.graphic_move = emoji_up
        elif direction == 2:
            self.graphic_move = emoji_right
        elif direction == 3:
            self.graphic_move = emoji_down
        elif direction == 4:
            self.graphic_move = emoji_left
    
    def graphic_update(newgraphic=None):
        if newgraphic:
            self.graphic_set = newgraphic
        elif goal_space == 0:
            self.graphic_blank = ":white_circle:"
        else:
            self.graphic_blank = ":o:"            
    
    def graphic():
        #TODO: this isn't the right way to make a property
        return self.graphic_set

class brandi_manager():
    card_deck = []
    hand_size = 6
    turn_player = None
    turn_player_num = 0
    turn_player_phase = 1
    game_state_message = None
    board_visual = None
    board_state = None
    board_visual_text = None
    board_visual_temp = None
    hosting_channel = None
    tempmessage = None
    round_counter = None
    round_player_num = 0
    round_player = None
    swap_phase = None
    playcard_card_original = None
    playcard_card_effective = None
    playcard_step = None
    # I probably don't need separate storages for each offramp
    # since only one needs to be used at a time
    # but I just want this done for now
    playcard_jack_storage = None
    playcard_seven_storage = None
    def __init__(self, channel, p1, p2, p3, p4):
        self.hosting_channel = channel
        self.playcard_card = None
        self.playcard_step = None
        self.tempmessage = None
        self.playcard_jack_storage = None
        self.playcard_seven_storage = None
        self.board_visual_temp = None
        # --- Building deck
        self.build_deck()
        self.swap_phase = True
        
        # --- Set Up Player Hand
        self.dealhand()
        print("brandi_manager Init complete")
        print("P1 - {}".format(str(player_one.player_hand)))
        print("P2 - {}".format(str(player_two.player_hand)))
        print("P3 - {}".format(str(player_three.player_hand)))
        print("P4 - {}".format(str(player_four.player_hand)))
        print("remaining deck len - {}".format(str(self.card_deck)))
        print("remaining deck - {}".format(str(len(self.card_deck))))
        
        # --- Build Game Board
        self.board_visual = []
        self.board_state = []
        # space 0 - P1 start
        self.board_state.append(boardspace(0, 2, 1))
        # space 1-3 - NW edge
        for board_space in range(1,4):
            self.board_state.append(boardspace(board_space, 2,0))
        #space 4-7 - Inner NW
        for board_space in range(4,8):
            self.board_state.append(boardspace(board_space, 3,0))        
        #space 8-11 - Inner N
        for board_space in range(8,12):
            self.board_state.append(boardspace(board_space, 2,0))
        #space 12-15 - Inner NE
        for board_space in range(12,16):
            self.board_state.append(boardspace(board_space, 1,0))   
        #space 16 - P2 start
        self.board_state.append(boardspace(16, 2, 3))
        #space 17-19 - NE edge
        for board_space in range(17,20):
            self.board_state.append(boardspace(board_space, 2,0))
        #space 20-31 - E edge
        for board_space in range(20,32):
            self.board_state.append(boardspace(board_space, 3,0))
        #space 32 - P3 start
        self.board_state.append(boardspace(32, 4, 2))
        # space 32-35 - SE edge
        for board_space in range(33,36):
            self.board_state.append(boardspace(board_space, 4,0))
        #space 36-39 - Inner SE
        for board_space in range(36,40):
            self.board_state.append(boardspace(board_space, 1,0))        
        #space 40-43 - Inner S
        for board_space in range(40,44):
            self.board_state.append(boardspace(board_space, 4,0))         
        #space 44-46 - Inner SW
        for board_space in range(44,48):
            self.board_state.append(boardspace(board_space, 3,0))
        # space 48 - P4 start
        self.board_state.append(boardspace(48, 4, 4))
        #space 48-50 - NE edge
        for board_space in range(49,51):
            self.board_state.append(boardspace(board_space, 4,0))
        #space 51-63 - E edge
        for board_space in range(51,64):
            self.board_state.append(boardspace(board_space, 1,0))
        for board_space in [1,3,2,4]:
            self.board_state.append(boardspace("G{}1".format(board_space), 1,0)) # 64 72 80 88
            self.board_state.append(boardspace("G{}2".format(board_space), 1,0)) # 65 73 81 89
            self.board_state.append(boardspace("G{}3".format(board_space), 1,0)) # 66 74 82 90
            self.board_state.append(boardspace("G{}4".format(board_space), 1,0)) # 67 75 83 91
            self.board_state.append(boardspace("P{}1".format(board_space), 1,0)) # 68 76 84 92
            self.board_state.append(boardspace("P{}2".format(board_space), 1,0)) # 69 77 85 93
            self.board_state.append(boardspace("P{}3".format(board_space), 1,0)) # 70 78 86 94
            self.board_state.append(boardspace("P{}4".format(board_space), 1,0)) # 71 79 87 95
        print("total spaces: {}".format(len(self.board_state)))
        
        # TODO: Pick a random person between 1 2 3 4
        self.turn_player_num = 1
        self.turn_player = player_one
        self.turn_player_phase = 1
        self.round_player_num = 1
        self.round_player = player_one
        self.round_counter = 1
        
        #print("sanity check")
        #for eachspace in self.board_state:
            #print("spacenum:{} - goalspace:{} - nextspace{}".format(eachspace.space_num, eachspace.goal_space, eachspace.next_space))
        
        """ # Old board design
        self.board_visual = [[ "P11","P12","P13","P14", None, None, None, None, None, None, None, None, None ],
                             [int(0),   63,   62,   61,   60,   59,   58,   57,   56,   55,   54,   53,   52 ],
                             [     1, None, None, None, None, None, None, None, None, None, None, None,   51 ],
                             [     2, None, None, None, None, None, None, None, None, None, None, None,   50 ],
                             [     3, None, None, None, None, None, None, None, None, None, None, None,   49 ],
                             [     4,    5,    6,    7,    8, None, None, None,   44,   45,   46,   47,   48 ],
                             [  None, None, None, None,    9, None, None, None,   43,"P41","P42","P43","P44" ],
                             [  None, None, None, None,   10, None, None, None,   42, None, None, None, None ],
                             [ "P31","P32","P33","P34",   11, None, None, None,   41, None, None, None, None ],
                             [    16,   15,   14,   13,   12, None, None, None,   40,   39,   38,   37,   36 ],
                             [    17, None, None, None, None, None, None, None, None, None, None, None,   35 ],
                             [    18, None, None, None, None, None, None, None, None, None, None, None,   34 ],
                             [    19, None, None, None, None, None, None, None, None, None, None, None,   33 ],
                             [    20,   21,   22,   23,   24,   25,   26,   27,   28,   29,   30,   31,   32 ],
                             [  None, None, None, None, None, None, None, None, None,"P24","P23","P22","P21" ]]
        
        self.board_visual = [[int(0),   63,   62,   61,   60,   59,   58,   57,   56,   55,   54,   53,   52 ],
                             [     1,"G11","P11","P12","P13","P14", None, None, None, None, None, None,   51 ],
                             [     2, None,"G12","G13","G14", None, None, None,"G44","G43","G42", None,   50 ],
                             [     3, None, None, None, None, None, None, None, None, None, None,"G41",   49 ],
                             [     4,    5,    6,    7,    8,    9, None,   43,   44,   45,   46,   47,   48 ],
                             [  None,"P31","P32","P33","P34",   10, None,   42,"P44","P43","P42","P41", None ],
                             [    16,   15,   14,   13,   12,   11, None,   41,   40,   39,   38,   37,   36 ],
                             [    17,"G31", None, None, None, None, None, None, None, None, None, None,   35 ],
                             [    18, None,"G32","G33","G34", None, None, None,"G24","G23","G22", None,   34 ],
                             [    19, None, None, None, None, None, None,"P24","P23","P22","P21","G21",   33 ],
                             [    20,   21,   22,   23,   24,   25,   26,   27,   28,   29,   30,   31,   32 ]]    
        
        self.board_visual_text = ""
        board_line_1 = ""
        board_line_2 = "\n"
        board_line_3 = "\n"
        board_line_4 = "\n"
        board_line_5 = "\n"
        board_line_6 = "\n"
        board_line_7 = "\n"
        board_line_8 = "\n"
        board_line_9 = "\n"
        board_line_10 = "\n"
        board_line_11 = "\n"
        board_line_12 = "\n"
        board_line_13 = "\n"
        for col_num in range(0, 11):
            board_line_1 += self.emoji_evaluate(self.board_visual[col_num][0])
            board_line_2 += self.emoji_evaluate(self.board_visual[col_num][1])
            board_line_3 += self.emoji_evaluate(self.board_visual[col_num][2])
            board_line_4 += self.emoji_evaluate(self.board_visual[col_num][3])
            board_line_5 += self.emoji_evaluate(self.board_visual[col_num][4])
            board_line_6 += self.emoji_evaluate(self.board_visual[col_num][5])
            board_line_7 += self.emoji_evaluate(self.board_visual[col_num][6])
            board_line_8 += self.emoji_evaluate(self.board_visual[col_num][7])
            board_line_9 += self.emoji_evaluate(self.board_visual[col_num][8])
            board_line_10 += self.emoji_evaluate(self.board_visual[col_num][9])
            board_line_11 += self.emoji_evaluate(self.board_visual[col_num][10])
            board_line_12 += self.emoji_evaluate(self.board_visual[col_num][11])
            board_line_13 += self.emoji_evaluate(self.board_visual[col_num][12])
        
        self.board_visual_text = board_line_1 + board_line_2 + board_line_3 + board_line_4 + board_line_5 + \
                                 board_line_6 + board_line_7 + board_line_8 + board_line_9 + board_line_10 + \
                                 board_line_11 + board_line_12 + board_line_13

        print("current length - {}".format(len(self.board_visual_text)))
        """

    def build_deck(self):
        self.card_deck = []
        leftovers_temp = []
        leftovers_temp += player_one.player_hand
        leftovers_temp += player_two.player_hand
        leftovers_temp += player_three.player_hand
        leftovers_temp += player_four.player_hand
        print("build_deck leftovers was {}".format(leftovers_temp))
        
        def check_add(card_label):
            if card_label in leftovers_temp:
                leftovers_temp.remove(card_label)
            else:
                self.card_deck.append(card_label)                
        
        for cardnum in range(1, 14):
            #s - spade, c - club, d - diamond, h - heart
            if cardnum == 1:
                cardnum = "A"
            elif cardnum == 11:
                cardnum = "J"
            elif cardnum == 12:
                cardnum = "Q"
            elif cardnum == 13:
                cardnum = "K"
            check_add("S{}".format(cardnum))
            check_add("S{}".format(cardnum))
            check_add("C{}".format(cardnum))
            check_add("C{}".format(cardnum))
            check_add("D{}".format(cardnum))
            check_add("D{}".format(cardnum))
            check_add("H{}".format(cardnum))
            check_add("H{}".format(cardnum))
        check_add("J")
        check_add("J")
        check_add("J")
        check_add("J")
        #fresh deck should be 108
        print("build_deck complete - deck is {} - {}".format(len(self.card_deck), self.card_deck))
        

    def next_order(self, playernumber):
        if playernumber == 1:
            return 3
        elif playernumber == 3:
            return 2
        elif playernumber == 2:
            return 4
        elif playernumber == 4:
            return 1
        else:
            print("nextorder error, number that isn't 1 2 3 4 entered")


    def next_turn(self):
        # TODO probably more passing turn things here, like opening next players hand automatically
        # Or that might end up happening in building board visual when resolving previous played card
        inf_protection = 6
        nextplayer = self.turn_player_num
        while inf_protection:
            nextplayer = self.next_order(nextplayer)
            if nextplayer == 1 and player_one.player_hand:
                self.turn_player_num = 1
                self.turn_player = player_one
                return
            elif nextplayer == 3 and player_three.player_hand:
                self.turn_player_num = 3
                self.turn_player = player_three
                return
            elif nextplayer == 2 and player_two.player_hand:
                self.turn_player_num = 2
                self.turn_player = player_two
                return
            elif nextplayer == 4 and player_four.player_hand:
                self.turn_player_num = 4
                self.turn_player = player_four
                return
            else:
                print("Nextturn failure - player_num wasn't 1 2 3 or 4?")
            inf_protection -= 1
        print("next_turn failure - inf protection reached?")

    def next_round(self):
        print("nextround triggered {}".format(self.round_player_num))
        nextplayer = self.next_order(self.round_player_num)
        if nextplayer == 1:
            self.round_player_num = 1
            self.round_player = player_one
            self.turn_player_num = 1
            self.turn_player = player_one            
        elif nextplayer == 3:
            self.round_player_num = 3
            self.round_player = player_three
            self.turn_player_num = 3
            self.turn_player = player_three            
        elif nextplayer == 2:
            self.round_player_num = 2
            self.round_player = player_two
            self.turn_player_num = 2
            self.turn_player = player_two            
        elif nextplayer == 4:
            self.round_player_num = 4
            self.round_player = player_four
            self.turn_player_num = 4
            self.turn_player = player_four            
        else:
            print("Nextturn failure - player_num wasn't 1 2 3 or 4?")
        print("nextround decided {}".format(self.round_player_num))
        self.swap_phase = True
        # deal cards
        self.dealhand()
        
        
        

    def label_to_space_array(self, s_label):
        if isinstance(s_label, int):
            #print("label_to_space_array - no conv needed {}".format(s_label))
            return self.board_state[s_label]
        elif isinstance(s_label, str):
            #I had this clever formula here which worked as long as players were on the board in order of 1, 2, 3 ,4
            # but they aren't, it's 1, 3, 2, 4, because 1 and 2 are teammates and need to sit opposite, not adjacent
            # so now I have to add some stupid if-elses here
            basenum = 63
            if s_label[0:1] == "P":
                basenum += 4
            if int(s_label[1:2]) == 1:
                pass # no adjustment for player 1
            elif int(s_label[1:2]) == 3:
                basenum += 8
            elif int(s_label[1:2]) == 2:
                basenum += 16
            elif int(s_label[1:2]) == 4:
                basenum += 24
            else:
                print("this shouldn't happen - label_to_space_array player number is not 1 2 3 4")
            basenum += int(s_label[2:])
            print("label_to_space_array converted {} to {}".format(s_label, basenum))
            return self.board_state[basenum]
        else:
            print("this shouldn't happen and someone did something wrong - label_to_space_array")
            return None

    def emoji_evaluate(self, inputval):
        if inputval is None:
            return square_b
        elif isinstance(inputval, int):
            #code for converting number to boardspace to emoji
            #print("board_space {} - {}".format(inputval, self.board_state[inputval].graphic_blank))
            return self.board_state[inputval].graphic_blank
        elif isinstance(inputval, str):
            if inputval[:1] == ":" and inputval[-1:] == ":":
                return inputval
            ### This section is being refactored
            ### New code for putting marbles on spaces make this obsolete
            if inputval == "P1":
                return player_one.player_emoji
            elif inputval == "P2":
                return player_two.player_emoji
            elif inputval == "P3":
                return player_three.player_emoji
            elif inputval == "P4":
                return player_four.player_emoji            
            elif inputval[0] == "P": #So far always true, but leaving room to refactor
                return ":o:"
                #marblenum = int(inputval[2])
                #if inputval[1] == "1":
                    #if player_one.player_home_marble >= marblenum: # this is definately going to cause problems later when P14 is on the board?
                        #return player_one.player_emoji
                    ##else: # I may not need this if I have a catchall at the end; but playing a marble triggers this right now
                        ##return square_b
                #elif inputval[1] == "2":
                    #if player_two.player_home_marble >= marblenum:
                        #return player_two.player_emoji                    
                #elif inputval[1] == "3":
                    #if player_three.player_home_marble >= marblenum:
                        #return player_three.player_emoji                    
                #elif inputval[1] == "4":
                    #if player_four.player_home_marble >= marblenum:
                        #return player_four.player_emoji
            elif inputval[0] == "G":
                return ":o:"
            else:
                print("this shouldn't happen - {}".format(inputval))
        else:
            print("this shouldn't happen - {}".format(inputval))
            return square_b
        # This case happens when a player marble isn't home, and it wants to render that home space. Find different emoji to mark player home with?
        print("if statements didn't work?")
        return square_b

    def dealhand(self):
        #sanity check
        for p_hand in [player_one, player_two, player_three, player_four]:
            if len(p_hand.player_hand) > 0:
                raise Exception("Cards still need to be played")
        # you need to check if deck needs to be reshuffled eventually
        for count in range(0, self.hand_size):
            for p_hand in [player_one, player_two, player_three, player_four]:
                if len(self.card_deck) == 0:
                    print("dealhand - ran out of cards, calling builddeck")
                    self.build_deck()
                if count == 0:
                    #this is just a placeholder so that test hands always have a test card
                    p_hand.player_hand.append("DA")
                elif count == 1:
                    p_hand.player_hand.append("DJ")
                elif count == 2:
                    p_hand.player_hand.append("D7")
                elif count == 3:
                    p_hand.player_hand.append("D4")
                else:
                    p_hand.player_hand.append(str(self.card_deck.pop(random.randint(0, len(self.card_deck)-1))))
        self.hand_size -= 1
        if self.hand_size <= 1:
            self.hand_size = 6
    
    async def build_board_state(self, tempimages=False):
        # you have to redo this to copy the self.board_visual properly
        # there's probably a better way to do it in general really
        """ # Old design
        new_visual = [[ "P11","P12","P13","P14", None, None, None, None, None, None, None, None, None ],
                      [int(0),   63,   62,   61,   60,   59,   58,   57,   56,   55,   54,   53,   52 ],
                      [     1, None, None, None, None, None, None, None, None, None, None, None,   51 ],
                      [     2, None, None, None, None, None, None, None, None, None, None, None,   50 ],
                      [     3, None, None, None, None, None, None, None, None, None, None, None,   49 ],
                      [     4,    5,    6,    7,    8, None, None, None,   44,   45,   46,   47,   48 ],
                      [  None, None, None, None,    9, None, None, None,   43,"P41","P42","P43","P44" ],
                      [  None, None, None, None,   10, None, None, None,   42, None, None, None, None ],
                      [ "P31","P32","P33","P34",   11, None, None, None,   41, None, None, None, None ],
                      [    16,   15,   14,   13,   12, None, None, None,   40,   39,   38,   37,   36 ],
                      [    17, None, None, None, None, None, None, None, None, None, None, None,   35 ],
                      [    18, None, None, None, None, None, None, None, None, None, None, None,   34 ],
                      [    19, None, None, None, None, None, None, None, None, None, None, None,   33 ],
                      [    20,   21,   22,   23,   24,   25,   26,   27,   28,   29,   30,   31,   32 ],
                      [  None, None, None, None, None, None, None, None, None,"P24","P23","P22","P21" ]]
        """
        
        new_visual = [[int(0),   63,   62,   61,   60,   59,   58,   57,   56,   55,   54,   53,   52 ],
                      [     1,"G11","P11","P12","P13","P14", None, None, None, None, None, None,   51 ],
                      [     2, None,"G12","G13","G14", None, None, None,"G44","G43","G42", None,   50 ],
                      [     3, None, None, None, None, None, None, None, None, None, None,"G41",   49 ],
                      [     4,    5,    6,    7,    8,    9, None,   43,   44,   45,   46,   47,   48 ],
                      [  None,"P31","P32","P33","P34",   10, None,   42,"P44","P43","P42","P41", None ],
                      [    16,   15,   14,   13,   12,   11, None,   41,   40,   39,   38,   37,   36 ],
                      [    17,"G31", None, None, None, None, None, None, None, None, None, None,   35 ],
                      [    18, None,"G32","G33","G34", None, None, None,"G24","G23","G22", None,   34 ],
                      [    19, None, None, None, None, None, None,"P24","P23","P22","P21","G21",   33 ],
                      [    20,   21,   22,   23,   24,   25,   26,   27,   28,   29,   30,   31,   32 ]]       
        
        print("build_board_state begin")
        print("p1 - {}".format([x.marble_location for x in player_one.player_marbles]))
        print("p2 - {}".format([x.marble_location for x in player_two.player_marbles]))
        print("p3 - {}".format([x.marble_location for x in player_three.player_marbles]))
        print("p4 - {}".format([x.marble_location for x in player_four.player_marbles]))
        
        for y_axis in range(0,11):
            for x_axis in range(0,13):
                if new_visual[y_axis][x_axis] is None:
                    # exclusively to skip processes on tiles that can never change
                    continue
                #this could be done better too
                for p1marble in player_one.player_marbles:
                    if new_visual[y_axis][x_axis] == p1marble.marble_location:
                        new_visual[y_axis][x_axis] = p1marble.marble_emoji_temp if tempimages and p1marble.marble_emoji_temp else "P1"
                for p2marble in player_two.player_marbles:
                    if new_visual[y_axis][x_axis] == p2marble.marble_location:
                        new_visual[y_axis][x_axis] = p2marble.marble_emoji_temp if tempimages and p2marble.marble_emoji_temp else "P2"
                for p3marble in player_three.player_marbles:
                    if new_visual[y_axis][x_axis] == p3marble.marble_location:
                        new_visual[y_axis][x_axis] = p3marble.marble_emoji_temp if tempimages and p3marble.marble_emoji_temp else "P3"
                for p4marble in player_four.player_marbles:
                    if new_visual[y_axis][x_axis] == p4marble.marble_location:
                        new_visual[y_axis][x_axis] = p4marble.marble_emoji_temp if tempimages and p4marble.marble_emoji_temp else "P4"
                #taken out of each conditional: not p4marble.marble_home and
        
        self.board_visual_text = ""
        board_line_1 = ""
        board_line_2 = "\n"
        board_line_3 = "\n"
        board_line_4 = "\n"
        board_line_5 = "\n"
        board_line_6 = "\n"
        board_line_7 = "\n"
        board_line_8 = "\n"
        board_line_9 = "\n"
        board_line_10 = "\n"
        board_line_11 = "\n"
        board_line_12 = "\n"
        board_line_13 = "\n"
        for col_num in range(0, 11):
            board_line_1 += self.emoji_evaluate(new_visual[col_num][0])
            board_line_2 += self.emoji_evaluate(new_visual[col_num][1])
            board_line_3 += self.emoji_evaluate(new_visual[col_num][2])
            board_line_4 += self.emoji_evaluate(new_visual[col_num][3])
            board_line_5 += self.emoji_evaluate(new_visual[col_num][4])
            board_line_6 += self.emoji_evaluate(new_visual[col_num][5])
            board_line_7 += self.emoji_evaluate(new_visual[col_num][6])
            board_line_8 += self.emoji_evaluate(new_visual[col_num][7])
            board_line_9 += self.emoji_evaluate(new_visual[col_num][8])
            board_line_10 += self.emoji_evaluate(new_visual[col_num][9])
            board_line_11 += self.emoji_evaluate(new_visual[col_num][10])
            board_line_12 += self.emoji_evaluate(new_visual[col_num][11])
            board_line_13 += self.emoji_evaluate(new_visual[col_num][12])
        
        if not tempimages:
            board_line_2 += "     Cards In Hand:"
            board_line_3 += "     {}:<@{}>".format(len(player_one.player_hand), player_one.playerping)
            board_line_4 += "     {}:<@{}>".format(len(player_three.player_hand), player_three.playerping)
            board_line_5 += "     {}:<@{}>".format(len(player_two.player_hand), player_two.playerping)
            board_line_6 += "     {}:<@{}>".format(len(player_four.player_hand), player_four.playerping)
            board_line_9 += "     Round {}".format(game_manager.round_counter)
            board_line_10 += "     Current round started by: <@{}>".format(game_manager.round_player.playerping)
            curturn = "     Current turn: <@{}>".format(game_manager.turn_player.playerping)
            if self.swap_phase:
                curturn = "     Current turn: Card Swap"
            board_line_12 += curturn
            # Turn order and possibly other things
            self.board_visual_text = board_line_1 + board_line_2 + board_line_3 + board_line_4 + board_line_5 + \
                                     board_line_6 + board_line_7 + board_line_8 + board_line_9 + board_line_10 + \
                                     board_line_11 + board_line_12 + board_line_13        
        else:
            self.board_visual_temp = board_line_1 + board_line_2 + board_line_3 + board_line_4 + board_line_5 + \
                                     board_line_6 + board_line_7 + board_line_8 + board_line_9 + board_line_10 + \
                                     board_line_11 + board_line_12 + board_line_13
            print("build_board_state temp called")
            self.reset_temps()
        
        print("current length - {}".format(len(self.board_visual_text)))
        
    
    def reset_temps(self):
        for pl in [player_one, player_two, player_three, player_four]:
            for ma in pl.player_marbles:
                ma.marble_emoji_temp = None
    
    def num_to_emoji_disc(self, num):
        # there's a third num_to_emoji that I forgot about
        # that one is used to display cards in hand
        # this and the next one are used to number marbles on the board
        if num == 1:
            return ":one:", "1"
        elif num == 2:
            return ":two:", "2"
        elif num == 3:
            return ":three:", "3"
        elif num == 4:
            return ":four:", "4"
        elif num == 5:
            return ":five:", "5"
        elif num == 6:
            return ":six:", "6"
        elif num == 7:
            return ":seven:", "7"
        elif num == 8:
            return ":eight:", "8"
        elif num == 9:
            return ":nine:", "9"
        elif num == 10:
            return ":zero:", "0"
        elif num == 11:
            return ":hash:", "#"
        elif num == 12:
            return ":asterisk:", "*"
        else:
            return num, num
        # I hope I don't need more than this     
        
    async def update_board_visual(self):
        await game_manager.game_state_message.edit(content=self.board_visual_text)
    
    async def swapcard(self, interaction):
        if player_one.handswap and player_two.handswap and player_three.handswap and player_four.handswap:
            player_one.player_hand.append(player_two.handswap)
            player_two.handswap = None
            
            player_two.player_hand.append(player_one.handswap)
            player_one.handswap = None
            
            player_three.player_hand.append(player_four.handswap)
            player_four.handswap = None
            
            player_four.player_hand.append(player_three.handswap)
            player_three.handswap = None
            
            game_manager.swap_phase = False
            # do handswap, begin round
            await self.build_board_state()
            await self.update_board_visual()
            await send_turn_player_alert(game_manager.turn_player)             
        else:
            pass
            # nothing but wait        
    
    def buttongen(self, attach_view, callback_func, button_row, button_id, button_cusid, button_emo, button_label, button_disable):
        button_gen = discord.ui.Button(
                row=button_row,
                id=button_id, # don't use a variable directly; it may take the variable at it's final state rather than at it's current state
                custom_id=button_cusid,
                emoji=button_emo, 
                label=button_label, 
                style=discord.ButtonStyle.blurple, 
                disabled=button_disable,
            )
        button_gen.callback = callback_func
        attach_view.add_item(button_gen)
        return
    
    
    async def playcard_callback(self, interaction):
        if game_manager.turn_player.player_name != interaction.user.name:
            print("------")
            print("nobody but the turn player should have gotten to here")
            print("------")
            return
        player_obj = game_manager.turn_player
        button_data = interaction.data["custom_id"].split(".")
        jokercontent = "Select card to play Joker as"
        if button_data[0] == "joker":
            validmoves = move_predictor(player_obj, (button_data[1], []))
            any_valid = move_set[1][0][1] + move_set[1][1][1] + move_set[1][2][1] + move_set[1][3][1]
            if any_valid:
                game_manager.playcard_card_effective = button_data[1]
            else:
                jokercontent = "Cannot find a valid move for card: {}".format(button_data[1])
        play_card = game_manager.playcard_card_effective
        
        if game_manager.playcard_step == 1:
            # step 1, joker check
            if play_card[0].lower() == "j":
                newview = discord.ui.View(timeout=None)
                game_manager.buttongen(newview, playcard_callback, 1, 1, "joker.2", None, "2", False)
                game_manager.buttongen(newview, playcard_callback, 1, 2, "joker.3", None, "3", False)
                game_manager.buttongen(newview, playcard_callback, 1, 3, "joker.4", None, "4", False)
                game_manager.buttongen(newview, playcard_callback, 1, 4, "joker.5", None, "5", False)
                
                game_manager.buttongen(newview, playcard_callback, 2, 5, "joker.6", None, "6", False)
                game_manager.buttongen(newview, playcard_callback, 2, 6, "joker.7", None, "7", False)
                game_manager.buttongen(newview, playcard_callback, 2, 7, "joker.8", None, "8", False)
                game_manager.buttongen(newview, playcard_callback, 2, 8, "joker.9", None, "9", False)
                
                game_manager.buttongen(newview, playcard_callback, 3, 9, "joker.10", None, "10", False)
                game_manager.buttongen(newview, playcard_callback, 3, 10, "joker.J", None, "J", False)
                game_manager.buttongen(newview, playcard_callback, 3, 11, "joker.Q", None, "Q", False)
                game_manager.buttongen(newview, playcard_callback, 3, 12, "joker.K", None, "K", False)
                game_manager.buttongen(newview, playcard_callback, 3, 13, "joker.A", None, "A", False)
                game_manager.playcard_step = 2
                await interaction.response.edit_message(content="Select card to play Joker as",view=newview) # delete_after=1
                return
            #bypass joker check
            game_manager.playcard_card_effective = play_card[1:] #drop the suite
            play_card = play_card[1:]
            game_manager.playcard_step = 2
        
        
        if play_card == "J":
            #we've already resolved jokers; so this must be Jack
            # Jack has no movement, so we can resolve it early and branch off
            game_manager.playcard_jack_storage = []
            await game_manager.playcard_jack_offramp(interaction)
            return
        
        move_valid = False
        start_valid = False
        if game_manager.playcard_step == 2:
            if game_manager.playcard_card_original == "J":
                #we got here from a joker check; grab new value
                game_manager.playcard_card_effective = interaction.data["custom_id"]
                play_card = interaction.data["custom_id"]
                print("playcard_callback - joker check - {}".format(interaction.data["custom_id"]))
                
            #step 2: check for starts
            if play_card in ["K","A"]:
                card_var, move_set = move_predictor(player_obj, (play_card,[]))
                #check to see if the cards have any possible non-starts
                # move predictor; first is the tuple of card + data, second (data) is a list of marbles
                #                 third (inside marble) is a tuple of marbleid + movelist, fourth is individual move 
                movelist = move_set[0][1] + move_set[1][1] + move_set[2][1] + move_set[3][1]
                if True in movelist:
                    start_valid = True
                movelist = [x for x in movelist if not isinstance(x, bool)]
                if movelist:
                    move_valid = True
                if start_valid and move_valid:
                    #more than one option; prompt player to decide
                    newview = discord.ui.View(timeout=None)
                    game_manager.buttongen(newview, playcard_phase2_offramp, 1, 2, "Start", None, "Start", False) # offramp function, because we're done
                    game_manager.buttongen(newview, playcard_callback, 1, 3, "Move", None, "Move", False) # callback here to phase 3
                    game_manager.playcard_step = 3
                    await interaction.response.edit_message(content="Start or Move?",view=newview) # delete_after=1
                    return                    
                elif start_valid:
                    #only start valid. Just go do it
                    player_obj.start_marble()
                    await interaction.response.edit_message(delete_after=1,view=None)
                    await game_manager.playcard_final()
                    return
                elif move_valid:
                    #move to phase 3 - fall through to below
                    game_manager.playcard_step = 3
                else:
                    print("playcard_callback - move_predictor evaluated moves from A/K but none valid?")
            else:
                # not K or A, just fall through to below
                game_manager.playcard_step = 3
        
        #the step system might have been unnecassary after Joker, but it was still useful for ace/king starts too
        if game_manager.playcard_step == 3:
            if play_card == "7":
                #seven offramp
                #we're assuming that because the button was enabled
                #that this is valid and will work out
                playcard_seven_offramp(interaction)
            #elif play_card == "4":
                #special move_predictor that counts backwards
                # We'll see how passing 4 directly into standard move predictor works
                # it should be coded to handle it properly
            else:
                playcard_movement_offramp(interaction)
                #standard move predictor + possibilities
            
            #we've already checked for starts, so any A or K getting this far is treated as movement
            # 2 3 5 6 8 9 10 Q K A - 4 7
            # for 4, distance algorith but add backwards
            # for 7, just do marble select one move at a time
            # predictor alg should have already cleared these as having one valid option, so we won't worry about that here
            
            pass
            
        return
    
    async def playcard_movement_offramp(self, interaction):
        options = move_predictor()
        return    
    
    async def playcard_seven_offramp(self, interaction):
        player_obj = game_manager.turn_player
        team_obj = None
        marble_select = None
        route_select = None
        thismarble = None
        valid_marbles = []
        movecounter = 0
        if player_obj.player_num == 1:
            team_obj = player_two
        elif player_obj.player_num == 2:
            team_obj = player_one
        elif player_obj.player_num == 3:
            team_obj = player_four
        elif player_obj.player_num == 4:
            team_obj = player_three
        else:
            print("playcard_seven_offramp - player not properly detected")
        
        if game_manager.playcard_seven_storage:
            valid_marbles, movecounter, marble_select, route_select = game_manager.playcard_seven_storage
        else: 
            # this should only run on the first pass
            _, marb_ids = move_predictor(player_obj, ("1",[]))
            valid_marbles += [x for x, y in zip(player_obj.player_marbles, marb_ids) if y[1]]
            _, marb_ids = move_predictor(team_obj, ("1",[]))
            valid_marbles += [x for x, y in zip(team_obj.player_marbles, marb_ids) if y[1]]
            game_manager.playcard_seven_storage = [valid_marbles, movecounter, marble_select, route_select]
        
        print(game_manager.playcard_seven_storage)
        print(valid_marbles)

        #look for input from previous interaction
        button_data = interaction.data["custom_id"].split(".")
        if button_data[0] == "seven":
            if button_data[1] == "route":
                route_select = button_data[2]
                game_manager.playcard_seven_storage[3] = route_select
            else:
                # move marble selected from previous input
                marble_select = button_data
                game_manager.playcard_seven_storage[2] = marble_select
        #look for single option choices
        if marble_select:
            #it's been selected by user input; bypass other cases
            pass
        elif len(valid_marbles) == 1:
            marble_select = valid_marbles[0]
        elif len(valid_marbles) < 1:
            print("seven_offramp - how did we get here?")
        
        # verify if we have/need choices - check for nones, and prompt user to fill them
        if marble_select is None:
            # ephemeral UI to prompt player
            newview = discord.ui.View(timeout=None)
            new_button_data = "seven.{}.{}"
            tempindex = 0
            #start at 0 for this because it's indexes of an array later
            for p_marble in valid_marbles:
                p_marble.marble_emoji_temp, texttemp = self.num_to_emoji_disc(tempindex+1)
                buttonval = new_button_data.format(p_marble.marble_pid, p_marble.marble_id)
                game_manager.buttongen(newview, game_manager.playcard_jack_offramp, 1, tempindex, buttonval, None, texttemp, False)
                tempindex += 1
            await game_manager.build_board_state(tempimages=True)
            await interaction.response.edit_message(content=game_manager.board_visual_temp,view=newview)
            return            
        elif isinstance(marble_select, str):
            # received from player
            thismarble = [x for x in valid_marbles if x.marble_pid == button_data[1] and x.marble_id == button_data[2]]
            game_manager.playcard_seven_storage[2] = thismarble
        else:
            #it's already an object, probably because solo option
            thismarble = marble_select
        
        #look for single option route choices
        if route_select is None:
            _, findroutes = move_predictor(player_obj if player_obj.player_num == thismarble.marble_pid else team_obj, ("1",[]), onlyone=True)
            findroutes = findroutes[1]
            if len(findroutes) > 1:
                # ephemeral UI to prompt player
                newview = discord.ui.View(timeout=None)
                new_button_data = "seven.route.{}"
                tempindex = 0
                #start at 0 for this because it's indexes of an array later
                for p_marble in valid_marbles:
                    """ TODO
                    ### You need to re-evaluate route options after a potential move to see if there are still enough valid moves if that choice is made
                    ### this is mostly to consider if a marble moves into the goal and there are no other possible moves to make after doing so
                    ### because otherwise that marble needs to be forced to move along the main path instead
                    p_marble.marble_emoji_temp, texttemp = self.num_to_emoji_disc(tempindex+1)
                    buttonval = new_button_data.format(p_marble.marble_pid, p_marble.marble_id)
                    game_manager.buttongen(newview, game_manager.playcard_jack_offramp, 1, tempindex, buttonval, None, texttemp, False)
                    tempindex += 1
                    """
                await game_manager.build_board_state(tempimages=True)
                await interaction.response.edit_message(content=game_manager.board_visual_temp,view=newview)
                return
            elif len(findroutes) == 1:
                route_select = findroutes[0]
            else:
                print("seven offramp - 0 routes? Somehow? Valid checker should have blocked this")    
        else:

        # do seven.playerid.marbleid
        
        # step 0: reconstruct valid_marbles
            for eachmarb in player_obj.player_marbles:
                valid_marbles.append(eachmarb)
            for eachmarb in team_obj.player_marbles:
                valid_marbles.append(eachmarb)
        
        for marb in valid_marbles:
            print("seven offramp - player marbles - {} - {}".format(marb.marble_pid, marb.marble_id))       
        
        
        if len(valid_marbles) > 1:
            #prompt selection
            newview = discord.ui.View(timeout=None)
            new_button_data = "seven.1.{}"
            tempindex = 0
            #start at 0 for this because it's indexes of an array later
            for p_marble in valid_marbles:
                p_marble.marble_emoji_temp, texttemp = self.num_to_emoji_disc(tempindex+1)
                game_manager.buttongen(newview, game_manager.playcard_seven_offramp, 1, tempindex, new_button_data.format(tempindex), None, texttemp, False)
                tempindex += 1
            await game_manager.build_board_state(tempimages=True)
            await interaction.response.edit_message(content=game_manager.board_visual_temp,view=newview)
            return
        elif len(valid_marbles) == 1:
            pass
            #auto select
        else:
            print("seven offramp - somehow, no valid player marbles; how did we get here?")    

        await game_manager.playcard_final()        
        return
    
    async def jack_marble_sorter(self, player_obj):
        valid_player_marbles = []
        valid_opp_marbles = []
        for p_marble in player_one.player_marbles:
            if not p_marble.marble_locked:
                if player_obj.player_num == player_one.player_num:
                    valid_player_marbles.append(p_marble)
                else:
                    valid_opp_marbles.append(p_marble)
        for p_marble in player_two.player_marbles:
            if not p_marble.marble_locked:
                if player_obj.player_num == player_two.player_num:
                    valid_player_marbles.append(p_marble)
                else:
                    valid_opp_marbles.append(p_marble)
        for p_marble in player_three.player_marbles:
            if not p_marble.marble_locked:
                if player_obj.player_num == player_three.player_num:
                    valid_player_marbles.append(p_marble)
                else:
                    valid_opp_marbles.append(p_marble)
        for p_marble in player_four.player_marbles:
            if not p_marble.marble_locked:
                if player_obj.player_num == player_four.player_num:
                    valid_player_marbles.append(p_marble)
                else:
                    valid_opp_marbles.append(p_marble)        
        return valid_player_marbles, valid_opp_marbles
    
    async def playcard_jack_offramp(self, interaction):
        player_obj = game_manager.turn_player
        valid_player_marbles = []
        valid_opp_marbles = []
        button_data = interaction.data["custom_id"].split(".")
        
        # this definately could have been collapsed into a smaller algorithm
        # for player in [p1 p2 p3 p4]?
        if not game_manager.playcard_jack_storage:
            # construct lists and store
            valid_player_marbles, valid_opp_marbles = await self.jack_marble_sorter(player_obj)
            game_manager.playcard_jack_storage = [valid_player_marbles,valid_opp_marbles]
        else:
            #retrieve from storage
            valid_player_marbles = game_manager.playcard_jack_storage[0]
            valid_opp_marbles = game_manager.playcard_jack_storage[1]
        
        print(game_manager.playcard_jack_storage)
        print(valid_player_marbles)
        for marb in valid_player_marbles:
            print("jack offramp - player marbles - {} - {}".format(marb.marble_pid, marb.marble_id))
        print(valid_opp_marbles)
        for marb in valid_opp_marbles:
            print("jack offramp - opp marbles - {} - {}".format(marb.marble_pid, marb.marble_id))        
        
        if button_data[0] == "jack":
            #do we have pending user input?
            if button_data[1] == "1":
                valid_player_marbles = [valid_player_marbles[int(button_data[2])]]
            elif button_data[1] == "2":
                valid_opp_marbles = [valid_opp_marbles[int(button_data[2])]]        
        
        if len(valid_player_marbles) > 1:
            #prompt selection
            newview = discord.ui.View(timeout=None)
            new_button_data = "jack.1.{}"
            tempindex = 0
            #start at 0 for this because it's indexes of an array later
            for p_marble in valid_player_marbles:
                p_marble.marble_emoji_temp, texttemp = self.num_to_emoji_disc(tempindex+1)
                game_manager.buttongen(newview, game_manager.playcard_jack_offramp, 1, tempindex, new_button_data.format(tempindex), None, texttemp, False)
                tempindex += 1
            await game_manager.build_board_state(tempimages=True)
            await interaction.response.edit_message(content=game_manager.board_visual_temp,view=newview)
            return
        elif len(valid_player_marbles) == 1:
            pass
            #auto select
        else:
            print("jack offramp - somehow, no valid player marbles; how did we get here?")
        
        if len(valid_opp_marbles) > 1:
            newview = discord.ui.View(timeout=None)
            new_button_data = "jack.2.{}"
            tempindex = 0
            #start at 0 for this because it's indexes of an array later
            for p_marble in valid_opp_marbles:
                p_marble.marble_emoji_temp, texttemp = self.num_to_emoji_disc(tempindex+1)
                game_manager.buttongen(newview, game_manager.playcard_jack_offramp, 1, tempindex, new_button_data.format(tempindex), None, texttemp, False)
                tempindex += 1
            await game_manager.build_board_state(tempimages=True)
            await interaction.response.edit_message(content=game_manager.board_visual_temp,view=newview)
            return
            #prompt selection
        elif len(valid_opp_marbles) == 1:
            pass
            #auto select
        else:
            print("jack offramp - somehow, no valid opp marbles; how did we get here?")        
        
        # at this point, there should be one marble in each list left
        tempstore = valid_player_marbles[0].marble_location
        valid_player_marbles[0].marble_location = valid_opp_marbles[0].marble_location
        valid_opp_marbles[0].marble_location = tempstore
        await game_manager.playcard_final()
        return
    
    async def playcard_phase2_offramp(self, interaction):
        # ace and king starts
        player_object.start_marble()
        await interaction.response.edit_message(delete_after=1,view=None)
        await game_manager.playcard_final()        
    
    async def playcard_final(self):
        #manage hand turn end and change
        print("playcard_final running")
        player_object = game_manager.turn_player
        player_object.player_hand.remove(game_manager.playcard_card_original)
        game_manager.playcard_step = 1
        game_manager.playcard_card_effective = None
        game_manager.playcard_card_original = None
        if len(player_one.player_hand + player_two.player_hand + player_three.player_hand + player_four.player_hand) == 0:
            game_manager.next_round()
        else:
            game_manager.next_turn()
        print("playcard_final printing")
        await self.build_board_state()
        await self.update_board_visual()
        await send_turn_player_alert(game_manager.turn_player)
        print("playcard_final finish")
    
    
    async def playcard(self, interaction, player_object=None, play_card="callback"):
        # I don't remember why I put the default value as callback
        # but it'll be stuck like that until I do a refactoring pass
        # this needs to be redone too, parse suit out of card properly
        if play_card not in player_object.player_hand:
            print("playcard -- sanity check failed?")
        
        # TODO: play_card being a tuple is going to cause problems
        
        self.playcard_card_original = play_card
        self.playcard_card_effective = play_card
        self.playcard_step = 1

        print("-playcard func")
        #print(player_object)
        print("card found - {}".format(play_card))
        #print(interaction)
        #print(interaction.data["custom_id"].split("."))
        
        #Checklist
        # -1. count how many marbles are home and on board
        # 0. Find possible moves to make, associate them with cards?
        # 1. Display list of cards for player to play. (grey out cards with no valid moves?)
        # 2. When card is selected, display list of card-specific possible moves (auto-select if none/one?)
        # 3. Repeat until card resolved
        # 4. Recalculate options (Go back to -1)
        
        # step 1: check for joker - decide on card to play as
        # step 2: check for starts (K, A), prompt for start or move
        # step 3: decide which marble to target (can skip if 1; need to check ally marbles for 7)
        # step 3.1: decide which opponent marble to target for Jack
        # step 4: decide which path to take. Usually only one path; but check for goal path, and also 4 backwards path
        
        # temporarily take out for testing
        if play_card.lower() == "j":
            # joker, not jack
            # this will get removed later (will require player to pick K or A from joker menu)
            player_object.start_marble()
        #elif play_card[1:].lower() in ["k","a"]:
            ## king and ace
            #player_object.start_marble()
        elif play_card[1:].lower() in ["k","a","j","7"]:
            # test new jack code
            await self.playcard_callback(interaction)
            return
        else:
            # This case for 2,3,5,6,8,9,10,
            # this 0 needs to be changed to the specific marble to move, forcing 0 now for simplicity
            player_object.move_marble_dist(0, card_to_int(play_card))
        
        await interaction.response.edit_message(content=interaction.message.content,delete_after=1,view=None)
        player_object.player_hand.remove(play_card)
        # TODO: consolodate this into one function too, probably
        if len(player_one.player_hand + player_two.player_hand + player_three.player_hand + player_four.player_hand) == 0:
            game_manager.next_round()
        else:
            game_manager.next_turn()
            
        await self.build_board_state()
        await self.update_board_visual()
        await send_turn_player_alert(game_manager.turn_player)
        #await interaction.response.send_message(return_content,view=returnview,ephemeral=True)
        
# -------------

class Start_Menu(discord.ui.View):
    def __init__(self, *, timeout=1800):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Claim P1",style=discord.ButtonStyle.blurple,emoji="\U0001F7E0")
    async def p1_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        return_content = assign_player(player_one, str(interaction.user.name), interaction.user.id)
        await interaction.response.edit_message(content=return_content)
        #await interaction.response.send_message("You're always the coolest to me", ephemeral=True)
        #print("-- data")
        #print(str(interaction.data))
        #print("-- channel") #maybe importnat? to get game to run only in one channel?
        #print(str(interaction.channel))
        #print("-- client")
        #print(str(interaction.client))
        #print("-- command")
        #print(str(interaction.command))
        #print("-- extras")
        #print(str(interaction.extras))
        #print("-- followup")
        #print(str(interaction.followup))
        #print("-- id")
        #print(str(interaction.id))
        #print("-- message")
        #print(str(interaction.message))
        #print("-- response")
        #print(str(interaction.response))
        #print("-- user") #important
        print(str(interaction.user))
        #await interaction.response.edit_message(content=f"{} claimed P1!".format(player_one))
        print(interaction.user.id)
        
        print(str(interaction.user))
        
    @discord.ui.button(label="Claim P2",style=discord.ButtonStyle.blurple,emoji="\U0001F535")
    async def p2_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        #await interaction.response.send_message("You're always the coolest to me", ephemeral=True)
        return_content = assign_player(player_two, str(interaction.user.name), interaction.user.id)
        await interaction.response.edit_message(content=return_content)
        
    @discord.ui.button(label="Claim P3",style=discord.ButtonStyle.red,emoji="\U0001F7E3")
    async def p3_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        #await interaction.response.send_message("You're always the coolest to me", ephemeral=True)
        return_content = assign_player(player_three, str(interaction.user.name), interaction.user.id)
        await interaction.response.edit_message(content=return_content)
        
    @discord.ui.button(label="Claim P4",style=discord.ButtonStyle.red,emoji="\U0001F7E2")
    async def p4_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        #await interaction.response.send_message("You're always the coolest to me", ephemeral=True)
        return_content = assign_player(player_four, str(interaction.user.name), interaction.user.id)
        await interaction.response.edit_message(content=return_content)
        
    @discord.ui.button(label="Start",style=discord.ButtonStyle.green)
    async def start_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        #await interaction.response.send_message("You're always the coolest to me", ephemeral=True)
        
        #initialize the things - init the game manager, run the board builder outside of init (so it works async properly)
        # then build the message containing the game
        channel = interaction.message.channel
        global game_manager
        game_manager = brandi_manager(channel,player_one,player_two,player_three,player_four)
        await game_manager.build_board_state()
        # --- TODO: What are these two lines for?
        #return_content = assign_player(None, interaction.user.name)
        #await interaction.response.edit_message(content=return_content)        
        # ---
        game_manager.game_state_message = await interaction.message.channel.send(game_manager.board_visual_text,view=Game_View())
        # TODO: This player needs to be randomly selected later


def num_to_emoji(num):
    num = str(num)
    if num == "1":
        return ":one:"
    elif num == "2":
        return ":two:"
    elif num == "3":
        return ":three:"
    elif num == "4":
        return ":four:"
    elif num == "5":
        return ":five:"
    elif num == "6":
        return ":six:"
    elif num == "7":
        return ":seven:"
    elif num == "8":
        return ":eight:"
    elif num == "9":
        return ":nine:"
    elif num == "10":
        return ":keycap_ten:"
    elif num == "A":
        return ":regional_indicator_a:"
    elif num == "J":
        return ":regional_indicator_j:"
    elif num == "Q":
        return ":regional_indicator_q:"
    elif num == "K":
        return ":regional_indicator_k:"

def card_to_int(card):
    card = str(card)
    if card[0] == "J":
        return 13
    card = card[1:]
    if card == "1":
        return 1
    elif card == "2":
        return 2
    elif card == "3":
        return 3
    elif card == "4":
        return 4
    elif card == "5":
        return 5
    elif card == "6":
        return 6
    elif card == "7":
        return 7
    elif card == "8":
        return 8
    elif card == "9":
        return 9
    elif card == "10":
        return 10
    elif card == "A":
        return 11
    elif card == "J":
        return 11
    elif card == "Q":
        return 12
    elif card == "K":
        return 13   

def emoji_hand(player_hand):
    # Spade = U+2660 U+FE0F
    # Club = U+2663 U+FE0F
    # Heart = U+2665 U+FE0F
    # Diamond = U+2666 U+FE0F
    # Joker = \U0001F0CF
    # A-  2-  3-  4-  5-  6-  7-  8-  9-  10-  J-  Q-  K-  
    # 1-U+31 U+FE0F U+20E3
    print("ran e_hand")
    if len(player_hand) == 0:
        return "Hand Empty"
    line_one = ""
    line_two = "\n"
    position_num = 1
    for each_card in player_hand:
        if each_card[0] == "J":
            line_one += "{}:black_joker:{}".format(square_b,square_b)
        elif each_card[0] == "S":
            line_one += ":spades:{}{}".format(num_to_emoji(each_card[1:]),square_b)
        elif each_card[0] == "C":
            line_one += ":clubs:{}{}".format(num_to_emoji(each_card[1:]),square_b)
        elif each_card[0] == "H":
            line_one += ":hearts:{}{}".format(num_to_emoji(each_card[1:]),square_b)
        elif each_card[0] == "D":
            line_one += ":diamonds:{}{}".format(num_to_emoji(each_card[1:]),square_b)
        line_two += "{}{}{}".format(num_to_emoji(position_num),square_b,square_b)
        position_num += 1
    #return str(player_hand)
    return line_one + line_two + "."

def button_card(player_card):
    return_suit = ""
    return_value = ""
    if player_card[0] == "J":
        return_suit = "\U0001F0CF"
    elif player_card[0] == "S":
        return_suit = "\U00002660"
        return_value = player_card[1:]
    elif player_card[0] == "C":
        return_suit = "\U00002663"
        return_value = player_card[1:]
    elif player_card[0] == "H":
        return_suit = "\U00002665"
        return_value = player_card[1:]
    elif player_card[0] == "D":
        return_suit = "\U00002666"
        return_value = player_card[1:]
    else:
        print("This shouldn't happen, you passed an unexpected value : {}".format(player_card))
    return return_suit, return_value
        

async def send_turn_player_alert(thisplayer):
    game_manager.tempmessage = await game_manager.hosting_channel.send("It is player {} <@{}> 's turn!".format(thisplayer.player_num, thisplayer.playerping),view=Game_View())
    #hopefully this saves the message


async def send_ephemeral_hand(thisplayer, interaction):
    return_content = emoji_hand(thisplayer.player_hand)
    thisplayer.player_hand_view = generate_player_hand_view(thisplayer)
    # channel.send returns the message object, but it cannot send ephemeral messages
    # response.sent_message returns whether the response succeeded or not? cannot store message obj
    # to do: find other differences between the two methods
    #thisplayer.player_hand_view = await interaction.message.channel.send(return_content,view=returnview,ephemeral=True)
    
    test = await interaction.response.send_message(return_content,view=thisplayer.player_hand_view,ephemeral=True)
    #test = await game_manager.hosting_channel.send_message(return_content,view=thisplayer.player_hand_view,ephemeral=True)    

class Game_View(discord.ui.View):
    def __init__(self, *, timeout=1800):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="View Hand",style=discord.ButtonStyle.blurple,emoji="\U0001F0CF")
    async def view_hand(self,interaction:discord.Interaction,button:discord.ui.Button):
        thisplayer = None
        for findplayer in [player_one, player_two, player_three, player_four]:
            if interaction.user.name == findplayer.player_name:
                thisplayer = findplayer
                print("foundplayer {} - {}".format(findplayer.player_num, findplayer.player_name))
        if thisplayer is None:
            return_content = "You aren't playing!"
            await interaction.response.send_message(return_content,view=Player_View(),ephemeral=True)
            return
        if game_manager.tempmessage and game_manager.turn_player == thisplayer:
            await game_manager.tempmessage.delete()
            game_manager.tempmessage = None
        # insert deletion of turn player message here
        print("calling player view here")
        await send_ephemeral_hand(thisplayer, interaction)
        
        # testing moving to function
        """
        return_content = emoji_hand(thisplayer.player_hand)
        thisplayer.player_hand_view = generate_player_hand_view(thisplayer)
        # channel.send returns the message object, but it cannot send ephemeral messages
        # response.sent_message returns whether the response succeeded or not? cannot store message obj
        # to do: find other differences between the two methods
        #thisplayer.player_hand_view = await interaction.message.channel.send(return_content,view=returnview,ephemeral=True)
        test = await interaction.response.send_message(return_content,view=thisplayer.player_hand_view,ephemeral=True)
        """


def move_predictor(player_obj, card_tuple, onlyone=None):
    # for each card:
    #     for each marble:
    #         does the card result in at least 1 valid move?
    #         yes: allow it to be played, deal with options later
    #         no: grey out button
    # if all options greyed out:
    #     discard hand, end round for player
    
    # do I build the whole tree of valid moves, and return them all to player?
    # do I only go one level deep, then the player selects a card and go the next level on that card?
    
    #def marble_advance_four():
    
    def marble_advance_seven(marble_loc, distance, locked=False):
        # the first time this is called, it is called on the space
        # that the marble is sitting on (distance 0)
        this_space = game_manager.label_to_space_array(marble_loc)
        if distance == 7:
            print("7 distance hit")
            return 7
        elif distance > 0 and this_space.marble and this_space.marble.marble_locked:
            # blocked path (distance must be >0 otherwise we likely detect the marble being moved)
            # relying on me properly storing/locking marbles            
            return distance-1
        else:
            best_dist = distance
            most_dis = 0
            next_spaces = this_space.next_space
            print("marble 7 alg - {} next to {}".format(marble_loc, next_spaces))
            for next_pos in next_spaces:
                if locked and isinstance(marble_loc, int) and isinstance(next_pos, str):
                    return 7
                    # if marble_loc is integer, it's on a normal space
                    # if it's on a normal space and it's locked, it is home beside goal
                    # this means going forward is always an option for the full distance
                    # the only thing that can stop 7 is a locked marble or the end of goal
                    # and we can guarentee neither of these are obstacles from this point
                elif next_pos is None:
                    # end of the goal road
                    # just return with how many steps it took
                    # because we aren't evaluating turns into the goal,
                    # this statement will only ever happen when a marble starts in the goal
                    # and there will not be a second option earlier
                    return distance
                else:
                    # it is not in a goal and it is not started
                    # mostly conerned with running into locked marbles 
                    most_dis = marble_advance_seven(next_pos, distance+1)
            return most_dis
        print("marble advance seven - end of tree hit?")
        return None #this should never hit
    
    def marble_seven_valid(player_obj):
        totaldist = 0
        for eachmarble in player_obj.player_marbles:
            if eachmarble.marble_home:
                continue
            totaldist += marble_advance_seven(eachmarble.marble_location, 0, eachmarble.marble_locked)
            if totaldist >= 7:
                return True
        #as long as any marbles can move a total of 7 spaces, it is valid
        #otherwise it is not
        return False

    def marble_advance_four(marble_loc, distance, locked=False):
        this_space = game_manager.label_to_space_array(marble_loc)
        if isinstance(marble_loc, str):
            # marble is in goal (or home), cannot reverse
            return []
        elif locked:
            #this next possibility is that the marble is on the start space
            #there is nothing that can stop it from stepping back 4
            new_loc = marble_loc - 4
            if new_loc < 0:
                new_loc += 64
            return [new_loc]
        elif distance == 0:
            return [this_space.space_num]
        else:
            # we check two things: 1. unobstructed space backwards
            #                      2. a turn into home
            if this_space.marble.marble_locked:
                #starting space should be handled by above case
                return []
            else:
                #one more step
                #mable_lock should be int at this point (or it gets caught at first if)
                prev_space = game_manager.label_to_space_array(marble_loc-1)
                check_for_goal = prev_space.next_space
                possibilities = []
                for eachspace in check_for_goal:
                    if eachspace.space_num == marble_loc:
                        #it's the normal path; so keep walking backward
                        possibilities += marble_advance_four(prev_space.space_num, distance-1)
                    else:
                        #the only way there's another path here is if it's the goal path
                        #check to see if it's the correct goal
                        if isinstance(next_pos, str):
                            # it's a goal space
                            if int(next_pos[1:2]) == game_manager.turn_player_num:
                                # it is the turn players goal - continue, but forwards
                                possibilities += marble_advance(next_pos, distance-1)
                            else:
                                # it is not the turn players goal - ignore it
                                pass
                        
        return
    
    # problem with marble_advance and current flaw in advance_sever
    # it is not detecting locked marbles blocking the path
    # need to add marble collision
    # and also on the todo list, stepping on marbles to send them home too
            
    def marble_advance(marble_loc, distance, locked=False):
        this_space = game_manager.label_to_space_array(marble_loc)
        if this_space.marble and this_space.marble.marble_locked:
            print("marble_advance - destination blocked - {} - {}".format(marble_loc, distance))
            return []
        if distance == 0:
            print("distance complete - destination is {}".format(this_space.space_num))
            return [this_space.space_num]
        elif distance > 0:
            possibilities = []
            #print(game_manager.label_to_space_array(marble_loc))
            next_spaces = game_manager.label_to_space_array(marble_loc).next_space
            print("{} next to {}".format(marble_loc, next_spaces))
            for next_pos in next_spaces:
                if locked and isinstance(marble_loc, int) and isinstance(next_pos, str):
                    print("marble is home and just started - cannot goal")
                    # if marble_loc is integer, it's on a normal space
                    # if it's on a normal space and it's locked, it is home beside goal
                    # if it's locked at home, it just started, do not go to goal
                    pass
                elif next_pos is None:
                    print("end of path with distance remaining, cannot complete")
                    # there is distance remaining but nowhere to go
                    # not a valid path
                    pass
                else:
                    #we're assuming move_predictor only gets called by turn player
                    if isinstance(next_pos, str):
                        # it's a goal space
                        if int(next_pos[1:2]) == game_manager.turn_player_num:
                            # it is the turn players goal - continue
                            possibilities += marble_advance(next_pos, distance-1)
                        else:
                            # it is not the turn players goal - ignore it
                            pass
                    else:
                        # it's not a goal space, it's a normal space
                        possibilities += marble_advance(next_pos, distance-1)
            return possibilities
        else:
            print("marble_advance - should never happen")
        return []
    
    print("move predictor start")
    card_var, move_set = card_tuple
    seven_check = False
    
    if len(card_var) > 1:
        card_val = card_var[1:]
    else:
        card_val = card_var
    # I'm sure this will fuck me up eventually, probably with jacks and jokers
    if card_val == "7":
        seven_check = marble_seven_valid(player_obj)    
    # TODO : need a different move predictor for each secondary function
    # fours, to count backward
    # sevens, to combine marbles
    # jack, swaps
    # king, ace, starts
    # assume joker is always playable?
    # -  -  4, -  -  7, -  -  -  Ja, -  K, A, Jo - special cases
    # 2, 3, 4, 5, 6, -  8, 9, 10, -  Q, K  A  -  - is always just distance forward
    card_distance = card_to_int(card_var)
    opp_marbles = None
    homelocked = False
    homelockcheck = False

    for eachmarble in player_obj.player_marbles:
        if onlyone and eachmarble.marble_id != onlyone:
            continue
        if card_var == "J":
            #jokers never invalid
            move_set.append([eachmarble.marble_id,["J"]])
        elif card_val == "J":
            # note that this one is card_val and not card_var. val strips the suit out
            if eachmarble.marble_locked:
                # a marble is locked if it is home, if it just started, or is on a goal space
                #nothing to swap
                move_set.append([eachmarble.marble_id,[]])
            else:
                if not opp_marbles:
                    player_marbles, opp_marbles = await game_manager.jack_marble_sorter(player_obj)
                if len(opp_marbles) > 0:
                    #valid opp to swap with
                    move_set.append([eachmarble.marble_id,[True]])
                else:
                    #nobody to swap with
                    move_set.append([eachmarble.marble_id,[]])
        elif eachmarble.marble_home and card_val not in ["A","K"]:
            #everybody is home and can't move, only starters+joker works
            move_set.append([eachmarble.marble_id,[]])
        elif eachmarble.marble_home and card_val in ["A","K"]:
            #marble is home, card is starter, exit is not blocked
            if not homelockcheck:
                homelockcheck = True #so we don't run this for each one
                for each2 in player_obj.player_marbles:
                    if each2.marble_locked and isinstance(each2.marble_location, int):
                        homelocked = True
            if not homelocked:
                move_set.append([eachmarble.marble_id,[True]])
            else:
                move_set.append([eachmarble.marble_id,[]])
        else:
            #marble is not home, card is not joker or jack 
            #check for 4 or 7, use a different marble_advance alg
            if card_val == "7":
                if seven_check:
                    move_set.append([eachmarble.marble_id, [True]])
                else:
                    move_set.append([eachmarble.marble_id,[]])
            elif card_val == "4":
                # this will need big bug testing
                set_to_append = [eachmarble.marble_id, marble_advance(eachmarble.marble_location,card_distance,eachmarble.marble_locked)]
                set_to_append[1].append(marble_advance_four(eachmarble.marble_location,card_distance,eachmarble.marble_locked))
                move_set.append(set_to_append)
            else:
                move_set.append([eachmarble.marble_id, marble_advance(eachmarble.marble_location,card_distance,eachmarble.marble_locked)])
    
    print(card_var)
    print(move_set)
    print("move predictor end")
    return card_var, move_set

testvar_deferred = None
testvar_interaction = None
def generate_player_hand_view(p_obj):
    # coroutine object has no attribute to_component
    # ^ I think because it was async at first, and the return from an async function is not the proper return
    # I probably had to use an await instead? Something like that
    print("generate_player_hand_view: {}".format(p_obj.player_hand))
    newview = discord.ui.View(timeout=None)
    splitrow = False
    buttonnum = 0
    if len(p_obj.player_hand) >= 6:
        splitrow = True
    
    atleastonevalid = False 
    for player_card in p_obj.player_hand:
        print()
        emoji_use, label_use = button_card(player_card)
        #To do: this tuple can store possible moves when turn starts
        # menu generation can pull from this without needing to recaculate mid-turn
        # but for now, I just want to test if the code works, so I make a fresh one every time
        print("hand generation: {}{}".format(emoji_use, label_use))
        temporary_tuple = (player_card, [])
        move_set = move_predictor(p_obj, temporary_tuple)
        #player_card_set[1] = move_set
        print(move_set)
        
        # this is where I should be generating possible moves and enabling/disabling a card in response?
        # then call this one when a players turn starts, and when a player wants to view their hand outside of their turn
        #      they can get a different view with all buttons disabled
        #move set is expected to contain: a tuple of (card, array of marbles). 
        #                                 array of marbles contains [id, array of options]
        #                                 array of options will have one item, False, if no valid moves
        if game_manager.swap_phase and p_obj.handswap is None:
            any_valid = True
        elif game_manager.swap_phase and p_obj.handswap:
            any_valid = False
        else:
            any_valid = move_set[1][0][1] + move_set[1][1][1] + move_set[1][2][1] + move_set[1][3][1]
        atleastonevalid = atleastonevalid or any_valid
        print("any valid for {} - {}".format(player_card, any_valid))
        print("testing {}".format(True if any_valid else False))
        buttontest = discord.ui.Button(
                row= 1 if (splitrow and buttonnum<3) else 2,
                id=int(buttonnum), # don't use a variable directly; it may take the variable at it's final state rather than at it's current state
                custom_id="{}.{}".format(p_obj.player_name, str(buttonnum)),
                emoji=str(emoji_use), 
                label=str(label_use), 
                style=discord.ButtonStyle.blurple, 
                disabled=not any_valid,
            )
        #print("button id:{}".format(buttontest.id))
        #buttontest.custom_id="{}.{}.{}".format(p_obj.player_name, str(buttonnum), str(buttontest.id))
        #print("button customid {}".format(buttontest.custom_id))
        async def se_callback(interaction):
            #this is a mess I gotta clean up
            print("callback number {}".format(int(buttonnum)))
            #print(interaction)
            #print(interaction.message.content)
            print(interaction.data)
            print(interaction.user.name) #same as below
            #print(p_obj.player_name) #same as above
            print(interaction.data["custom_id"])
            print(interaction.data["custom_id"].split("."))
            button_pname = interaction.data["custom_id"].split(".")[0]
            button_cardnum = int(interaction.data["custom_id"].split(".")[1])
            button_p_obj = find_player_obj(str(interaction.user.name))
            
            if game_manager.swap_phase:
                p_obj.handswap = p_obj.player_hand.pop(button_cardnum)
                await interaction.response.edit_message(content=interaction.message.content,delete_after=1,view=None)
                #I don't think I actually need that final variable, refactor later
                await game_manager.swapcard(interaction)
                return

            # TODO - Insert player turn check here once turn tracker is set up
            if game_manager.turn_player.player_name != button_p_obj.player_name:
                # it is not this players turn
                await interaction.response.send_message("It is not your turn. Please Wait",ephemeral=True) 
            elif str(button_p_obj.player_name) == str(button_pname):
                global testvar_interaction
                global testvar_deferred
                print("se_callback success")
                p_obj.player_hand_view.remove_item(button_cardnum)
                # removing the view works; editing the delete_after sometimes does or does not? failed in initial testing, worked eventually 
                # await interaction.response.edit_message(content=interaction.message.content,delete_after=1,view=None)
                await game_manager.playcard(interaction, button_p_obj, button_p_obj.player_hand[button_cardnum])                    
                    
                #test = interaction.message.components[0].children
                #print(test[0])
                #print(len(test))
                
                # these don't work
                # global testvar_ephem_message_delete
                #await interaction.delete_original_response()
                #anothertestvar = await interaction.channel.fetch_message(testvar_ephem_message_delete)
                #anothertestvar = await discord.abc.Messageable.fetch_message(testvar_ephem_message_delete)
                #await interaction.message.edit(delete_after=1,view=None) # can't find message. need to use response.edit_message
                #print(anothertestvar)
                #interaction.response.
                #await interaction.message.delete()
                #testvar_interaction = interaction
                #newinter = await interaction.response.defer()
                #print(newinter.resource)
                #testvar_deferred = newinter.resource
                
                #I think the goal here is to reply on the delete_after
                #get the turn order working, and just send a new ephemeral message to the turn player when their turn starts
                
                
                
                #await button_p_obj.player_hand_view.edit(content="testing editing weee")
                #if further action needed
                #returnview = generate_card_option_view(thisplayer)
                #await interaction.response.send_message(return_content,view=returnview,ephemeral=True)                
            else:
                print("se_callback fail")
                print("{} - {}".format(button_p_obj.player_name, len(button_p_obj.player_name)))
                print("{} - {}".format(button_pname, len(button_pname)))
                await interaction.response.edit_message(content="error has occurred")
    
        buttontest.callback = se_callback
        newview.add_item(buttontest)
        buttonnum += 1
        #newview.remove_item
        #newview.find_item
        #newview.clear_items
    
    
    ###
    # This is for testing purposes; remove later
    ###
    #buttontest = discord.ui.Button(
        #row= 1 if (splitrow and buttonnum<3) else 2,
        #id=int(buttonnum), # don't use a variable directly; it may take the variable at it's final state rather than at it's current state
        #custom_id="testbutton".format(p_obj.player_name, str(buttonnum)),
        #emoji="\U000020E3", # \U0001F0CF joker that I know works 
                            ## \U00000030 bad for 0, U0000FE0F bad
        #label=":one:", 
        #style=discord.ButtonStyle.blurple, 
        #disabled=not any_valid,
    #)    
    #newview.add_item(buttontest)
    ###
    # This is for testing purposes
    ###
    
    if not atleastonevalid and not game_manager.swap_phase:
        buttonnum += 1
        print("generate_player_hand none valid")
        buttontest = discord.ui.Button(
                row=2,
                id=int(buttonnum), # don't use a variable directly; it may take the variable at it's final state rather than at it's current state
                custom_id="{}.{}".format(p_obj.player_name, str(buttonnum)),
                emoji="😩", 
                label="No Valid Moves", 
                style=discord.ButtonStyle.blurple, 
                disabled=False,
            )
        async def se_callback(interaction):
            button_p_obj = find_player_obj(str(interaction.user.name))
            button_p_obj.player_hand = []
            await interaction.response.edit_message(content=interaction.message.content,delete_after=1,view=None)
            # TODO: consolodate this into one function too, probably
            if len(player_one.player_hand + player_two.player_hand + player_three.player_hand + player_four.player_hand) == 0:
                game_manager.next_round()
            else:
                game_manager.next_turn()
            await game_manager.build_board_state()
            await game_manager.update_board_visual()
        buttontest.callback = se_callback
        newview.add_item(buttontest)
    
    print("functiondone")
    return newview


def generate_card_option_view():
    # very under constructions
    buttontest = discord.ui.Button(
            row= 1 if (splitrow and buttonnum<3) else 2,
            custom_id="{}.{}".format(p_obj.player_name, str(buttonnum)),
            emoji=emoji_use,
            label=label_use, 
            style=discord.ButtonStyle.blurple, 
            disabled=False
        )    
    return

    
def find_player_obj(playername):
    for p_obj in [player_one, player_two, player_three, player_four]:
        if p_obj.player_name == playername:
            return p_obj

# this might not even be being used
# except to catch errors from people who aren't playing but are clicking buttons?
# see if this can get removed later
globaltestvar = "44"
class Player_View(discord.ui.View):
    testlabel_1 = "1"
    testlabel_2 = "2"
    testlabel_3 = "33"
    testlabel_4 = globaltestvar
    testlabel_5 = "5"
    testlabel_6 = "6"
    def __init__(self, buttonlabel1="1", timeout=1800):
        self.testlabel_1 = buttonlabel1
        self.testlabel_2 = "2_2_2"
        self.testlabel_3 = "3_3_3"
        self.testlabel_4 = "4_4_4"
        self.testlabel_5 = "5_5_5"
        self.testlabel_6 = "6_6_6"
        super().__init__(timeout=timeout)    

    @discord.ui.button(label=testlabel_1,style=discord.ButtonStyle.blurple)
    async def option_one(self,interaction:discord.Interaction,button:discord.ui.Button):
        p_obj = find_player_obj(interaction.user.name)
        if p_obj is not None:
            print("playing card 0 - from player {}".format(p_obj.player_num))
            await game_manager.playcard(interaction, p_obj, p_obj.player_hand[0])
        else:
            print("p_obj is none")
        return_content = emoji_hand(p_obj.player_hand)
        await interaction.response.edit_message(content=return_content)
       
    @discord.ui.button(label=testlabel_2,style=discord.ButtonStyle.blurple)
    async def option_two(self,interaction:discord.Interaction,button:discord.ui.Button):
        p_obj = find_player_obj(interaction.user.name)
        if p_obj is not None:
            print("playing card 1 - from player {}".format(p_obj.player_num))
            await game_manager.playcard(interaction, p_obj, p_obj.player_hand[1])
        else:
            print("p_obj is none")
        return_content = emoji_hand(p_obj.player_hand)
        await interaction.response.edit_message(content=return_content)
         
    @discord.ui.button(label=testlabel_3,style=discord.ButtonStyle.blurple)
    async def option_three(self,interaction:discord.Interaction,button:discord.ui.Button):
        p_obj = find_player_obj(interaction.user.name)
        if p_obj is not None:
            print("playing card 2 - from player {}".format(p_obj.player_num))
            await game_manager.playcard(interaction, p_obj, p_obj.player_hand[2])
        else:
            print("p_obj is none")
        return_content = emoji_hand(p_obj.player_hand)
        await interaction.response.edit_message(content=return_content)
          
    @discord.ui.button(label="4",row=2,style=discord.ButtonStyle.blurple)
    async def option_four(self,interaction:discord.Interaction,button:discord.ui.Button):
        p_obj = find_player_obj(interaction.user.name)
        if p_obj is not None:
            print("playing card 3 - from player {}".format(p_obj.player_num))
            await game_manager.playcard(interaction, p_obj, p_obj.player_hand[3])
        else:
            print("p_obj is none")
        return_content = emoji_hand(p_obj.player_hand)
        await interaction.response.edit_message(content=return_content)
          
    @discord.ui.button(label="5",row=2,style=discord.ButtonStyle.blurple)
    async def option_five(self,interaction:discord.Interaction,button:discord.ui.Button):
        p_obj = find_player_obj(interaction.user.name)
        if p_obj is not None:
            print("playing card 4 - from player {}".format(p_obj.player_num))
            await game_manager.playcard(interaction, p_obj, p_obj.player_hand[4])
        else:
            print("p_obj is none")
        return_content = emoji_hand(p_obj.player_hand)
        await interaction.response.edit_message(content=return_content)
           
    @discord.ui.button(label="6",row=2,style=discord.ButtonStyle.blurple)
    async def option_six(self,interaction:discord.Interaction,button:discord.ui.Button):
        p_obj = find_player_obj(interaction.user.name)
        if p_obj is not None:
            print("playing card 5 - from player {}".format(p_obj.player_num))
            await game_manager.playcard(interaction, p_obj, p_obj.player_hand[5])
        else:
            print("p_obj is none")
        return_content = emoji_hand(p_obj.player_hand)
        await interaction.response.edit_message(content=return_content)
               
@client.event
async def on_message(message):
    try:
        authname = str(message.author.name)
        if bot_username == authname:
            #ignore own name
            return
        #if admin_discord_handle != message.author.name:
            #uncomment to ignore everybody else
            #return

        need_save = False
        spoilertagged = False
        if "||" in message.content:
            spoilertagged = True
        commandsplit = message.content.replace("\n"," ").split(" ")

        #feature for fixing twitter links with bad thumbnails
        for msseg in commandsplit:
            #print("msseg - {}".format(msseg))
            if r"/twitter.com/" in msseg or r"/x.com/" in msseg or r".twitter.com/" in msseg or r".x.com/" in msseg:
                newmessage = msseg.replace("twitter", "vxtwitter")
                newmessage = newmessage.replace("x.com/", "vxtwitter.com/")
                if spoilertagged:
                    newmessage = newmessage.replace("||","")
                    newmessage = "{}{}{}".format("||",newmessage,"||")
                await message.channel.send(newmessage)        
    
        command = commandsplit[0].lower()    
        postcommand = " ".join(commandsplit[1:])
        if command == 'u!brandi':
            # eventually I'll support concurrent games
            if game_manager:
                await message.channel.send("Game in progress! Please wait!")
            else:
                await message.channel.send("Select a seat!",view=Start_Menu())
        elif command == 'u!setme':
            print("setme detected {} - {}".format(authname, type(authname)))
            if game_manager:
                print("p1 is {} - {}".format(player_one.player_name, type(player_one.player_name)))
                print("p2 is {} - {}".format(player_two.player_name, type(player_two.player_name)))
                print("p3 is {} - {}".format(player_three.player_name, type(player_three.player_name)))
                print("p4 is {} - {}".format(player_four.player_name, type(player_four.player_name)))
                if player_one and player_one.player_name == authname:
                    print("p1 setme {}".format(postcommand.replace(" ","")))
                    player_one.player_emoji = postcommand.replace(" ","")
                elif player_two and player_two.player_name == authname:
                    print("p2 setme {}".format(postcommand.replace(" ","")))
                    player_two.player_emoji = postcommand.replace(" ","")
                elif player_three and player_three.player_name == authname:
                    print("p3 setme {}".format(postcommand.replace(" ","")))
                    player_three.player_emoji = postcommand.replace(" ","")
                elif player_four and player_four.player_name == authname:
                    print("p4 setme {}".format(postcommand.replace(" ","")))
                    player_four.player_emoji = postcommand.replace(" ","")                  
        elif command == "u!emoji":
            # Spade = U+2660 U+FE0F
            # Club = U+2663 U+FE0F
            # Heart = U+2665 U+FE0F
            # Diamond = U+2666 U+FE0F
            # Joker = \U0001F0CF
            # A-  2-  3-  4-  5-  6-  7-  8-  9-  10-  J-  Q-  K-  
            # 1-U+31 U+FE0F U+20E3        
            await message.channel.send("\U00002666 \U00002665 \U00002663 \U00002660 :diamonds::one::two:")
        elif command == "u!repeat":
            print(str(postcommand))
            await message.channel.send(postcommand)
        elif command == 'u!time':
            discmessage = "(month) (day) hour minute AM/PM - use 3 letter month and only numbers for day/hour/minute"
            try:
                nowtime = datetime.datetime.now()
                timeyear = int(nowtime.year)
                timemonth = int(nowtime.month)
                timeday = int(nowtime.day)
                timehour = int(nowtime.hour)
                timeminute = int(nowtime.minute)
                timehalf = 'am'
                granular = 'day'
                zone = 'mst'
                if len(commandsplit) == 7:
                    # command month day hour minute AMPM zone
                    granular = 'year'
                    timemonth = commandsplit[1].lower()
                    if timemonth == 'jan':
                        timemonth = 1
                    elif timemonth == 'feb':
                        timemonth = 2
                    elif timemonth == 'mar':
                        timemonth = 3
                    elif timemonth == 'apr':
                        timemonth = 4
                    elif timemonth == 'may':
                        timemonth = 5
                    elif timemonth == 'jun':
                        timemonth = 6
                    elif timemonth == 'jul':
                        timemonth = 7
                    elif timemonth == 'aug':
                        timemonth = 8
                    elif timemonth == 'sep':
                        timemonth = 9
                    elif timemonth == 'oct':
                        timemonth = 10
                    elif timemonth == 'nov':
                        timemonth = 11
                    elif timemonth == 'dec':
                        timemonth = 12
                    #print(timemonth)
                    timeday = int(commandsplit[2])
                    timehour = int(commandsplit[3])
                    timeminute = int(commandsplit[4])
                    timehalf = commandsplit[5].lower()
                    zone = commandsplit[6].lower()
                elif len(commandsplit) == 6:
                    # command day hour minute AMPM
                    granular = 'month'
                    timeday = int(commandsplit[1])
                    timehour = int(commandsplit[2])
                    timeminute = int(commandsplit[3])
                    timehalf = commandsplit[4].lower()
                    zone = commandsplit[5].lower()
                elif len(commandsplit) == 5:
                    # command hour minute AMPM
                    timehour = int(commandsplit[1])
                    timeminute = int(commandsplit[2])
                    timehalf = commandsplit[3].lower()
                    zone = commandsplit[4].lower()
                else:
                    discmessage = "(month) (day) hour minute AM/PM - use 3 letter month and only numbers for day/hour/minute"
                    await message.channel.send(discmessage)
                    return
                if timehalf == 'pm' and timehour != 12:
                    timehour += 12
                elif timehalf == 'am' and timehour == 12:
                    timehour = 0
                date_time = datetime.datetime(timeyear, timemonth, timeday, timehour, timeminute, 0)
                if zone == 'pst':
                    date_time = date_time + datetime.timedelta(hours=1)
                elif zone == 'cst':
                    date_time = date_time - datetime.timedelta(hours=1)
                elif zone == 'est':
                    date_time = date_time - datetime.timedelta(hours=2)
                elif zone == 'gmt':
                    date_time = date_time - datetime.timedelta(hours=6)            
                if date_time < nowtime:
                    if granular == 'day':
                        date_time = date_time + datetime.timedelta(days=1)
                        date_time = datetime.datetime(timeyear, timemonth, timeday, timehour, timeminute, 0)
                    elif granular == 'month':
                        timemonth += 1
                        if timemonth == 13:
                            timemonth = 1
                            timeyear += 1
                        date_time = datetime.datetime(timeyear, timemonth, timeday, timehour, timeminute, 0)                    
                    elif granular == 'year':
                        timeyear += 1
                        date_time = datetime.datetime(timeyear, timemonth, timeday, timehour, timeminute, 0)                    
                unixstamp = int(time.mktime(date_time.timetuple()))
                discmessage = "<t:{}> - unix: {}".format(unixstamp, unixstamp)            
            except:
                traceback.print_exc()
                discmessage = "(month) (day) hour minute AM/PM timezone - use 3 letter month and only numbers for day/hour/minute - currently only supports PST, MST, CST, EST"
            await message.channel.send(discmessage)            
        elif admin_discord_handle == authname:
            if command == 'u!end':
                #print("Ending")
                await client.close()
            if command == 'u!btest':
                #admin test commands
                global testvar_interaction
                global testvar_deferred
                thisplayer = None
                for findplayer in [player_one, player_two, player_three, player_four]:
                    if testvar_interaction.user.name == findplayer.player_name:
                        thisplayer = findplayer
                        print("foundplayer {} - {}".format(findplayer.player_num, findplayer.player_name))
                if thisplayer is None:
                    return_content = "You aren't playing!"
                    await testvar_interaction.response.send_message(return_content,view=Player_View(),ephemeral=True)
                    return
                print("calling player view here")
                return_content = emoji_hand(thisplayer.player_hand)
                thisplayer.player_hand_view = generate_player_hand_view(thisplayer)
                # channel.send returns the message object, but it cannot send ephemeral messages
                # response.sent_message returns whether the response succeeded or not? cannot store message obj
                # to do: find other differences between the two methods
                #thisplayer.player_hand_view = await interaction.message.channel.send(return_content,view=returnview,ephemeral=True)
                test = await testvar_deferred.response.edit_message(content=return_content,view=thisplayer.player_hand_view)              
        #else:
            #print('no channel found')
    except Exception as e:
        await message.channel.send("Error occurred: {}".format(traceback.format_exc()))
    
    

#######################

def turnOff():
    client.close()
    sys.exit(0)

def turnOn():
    loop2 = asyncio.get_event_loop()
    asyncio.ensure_future(client.run(discotoken))
    loop2.run_forever()

window = tk.Tk()
#window.wm_attributes("-topmost", 1)
window.geometry("350x100")
frame_b = tk.Frame(bg="#330000", height=10)
endbutton = tk.Button(master=frame_b, text="Quit", command=turnOff)
startbutton = tk.Button(master=frame_b, text="Start", command=turnOn)
endbutton.pack(side=tk.RIGHT)
startbutton.pack(side=tk.RIGHT)
frame_b.pack(fill=tk.X)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
asyncio.ensure_future(window.mainloop())
loop.run_forever()
