#Ashwin Shrestha          12-4-2023
#Description - This is a working model of the popular game Candy Land. This game works until a player gets to the goal, in which case the 
#              game stops.

import random
import colorama
import copy
import sys
from colorama import Fore
colorama.init(autoreset=True)     # resets the color back to default after each line


def banner():   # banner
   print("\n###################################################\n")

def press_enter():  # useful so that my code has breaks, and user has control over the game.
   print()
   input("Press [enter] to continue....")
 
def rules():    # the rules
   print('''\nWelcome to Ashwin's Candy Realm!
         
            The Rules are simple:
         
            1) There are four players. The player itself will be human or AI depending on how many humans you choose.
            2) You can choose how many copies of a basic card to make from 1 to 5, and it will mutliply according to your choice.
            3) Your start card is always fixed, and will not change.
            4) Your cards can change if you wish so, just shuffle it
            5) The player will move to the next color on the game that you picked from your deck of cards.
            6) You win if you cross the last start card
            7) If your card isn't in start card don't worry, you have just won!!
            8) I tweaked the game such that if the card you draw is not present in the start, you basically went beyond the start card
               and won!
            9) Let the game begin!
         
            Side Note: I may have added a fun functionality to the game hehe''')
   

def user_choice():             # asks the user whether to play the game, to read the rules or quit the game
   print("[p]lay: to play the game, [r]ules: to read the rules, and [q]uit")
   while True:
       user_input = input("\nPlease enter either [p]lay, [r]ules or [q]uit: ")
       if user_input not in ["p","P","R","r","q","Q"]:
           print("Please enter either [p], [r], or [q]")
           continue
       if user_input == "p" or user_input == "P":
          return True
       if user_input == "r" or user_input == "R":
          rules()
       if user_input == "q" or user_input == "Q":
          print("Exiting...")
          sys.exit()

def define_card():         #defines the values of the card, and calls a function to essentially duplicate the card according to the user
   card = ["B","G","Y","R","M"]
   new_card = duplicate(card)
   return new_card

def duplicate(card):       # duplicates the cards according to the choice of the user
   while True:
        choice = input("How many copies of each card [1]- [5]?: ")
        try:
            choice = int(choice)
        except:
            print("Please enter an integer(1-5)")
            continue
        if choice not in [1,2,3,4,5]:
            print("Please enter an integer between 1 and 5")
            continue
        copy = card*choice
        return copy
   
def create_card(card):     #creates a start card which will not be changed for the entirety of a game
   new_card = copy.deepcopy(card)
   start_card = shuffle_card(new_card)
   return start_card

def print_Start(start_card):      # prints the start card to the terminal
    print(Fore.LIGHTYELLOW_EX + "START", end = "   ")
    print_with_color(start_card)
   
    print(Fore.LIGHTBLUE_EX + " GOAL!")

def print_Card(new_card):            # creates and prints the card which the user should have a choice to shuffle
    print(Fore.LIGHTYELLOW_EX+ "CARDS",end = "   ")
    print_with_color(new_card)
    print("\n\n")

   
def print_with_color(card):     # uses colorama to print both start_card and card with color
     for i in range(len(card)):
       if card[i] == "B":
         print(Fore.BLUE + card[i], end = "  ")
       if card[i] == "G":
         print(Fore.GREEN + card[i], end = "  ") 
       if card[i] == "R":
         print(Fore.RED + card[i], end = "  ")
       if card[i] == "Y":
         print(Fore.YELLOW + card[i], end = "  ")
       if card[i] == "M":
         print(Fore.MAGENTA + card[i], end = "  ")

def board_creation(card):     # creates a board for four players
  board = []
  for i in range(4):
     board.append([])
     for j in range(len(card)):
        board[i].append("")
  return board            # the board is the list

def shuffle_card(card):        # shuffles a deck of card given to it
   random.shuffle(card)
   return card


def card_drop_index(card, start_card, index):        #checks the location to drop the card by checking where the card matches the start-card in, and the index determines where to start the search from
   current_card = card[0]
   for i in range(index+1, len(start_card)):
      if start_card[i] == current_card:
         return i

def move_the_player(list,index,player_num):     # moves the player to the correct index. First removes any player, and then adds the player to the index location creating an illusion of moving
   position = current_position(list, player_num)
   for i in range(len(list[player_num-1])):
      if list[player_num-1][i] == player_num:
         list[player_num-1][i] = ""
         break
   try:
     list[player_num-1][index] = player_num
   except:
      print(f"\nPlayer {player_num} has moved {len(list[player_num-1])-position} spaces")
      print(Fore.LIGHTRED_EX+ f"\nPlayer {player_num} has won the game!!")
      print("\nThank you for playing!\n")
      sys.exit()

def print_player(list,player_num):    # prints the player to the screen
   print("        ", end = "")
   for i in list[player_num-1]:
      print(i, end = "   ")
   print()

def print_allplayer(list):      # prints all the players to the screen
   for i in list:
      print("        ", end = "")
      for j in i:
         print(j, end = "   ")
      print()

def get_updated_card(card):    # is used when one card is drawn, the drawn card goes to the end of the deck, and the second card becomes the first
   card.append(card[0])
   del card[0]
   return card

def space(player_num, step):   # displays number of steps a player moved after drawing a card
   if step == 1:
      print(f"Player {player_num} has moved {step} space")
   else:
      print(f"Player {player_num} has moved {step} spaces")
   press_enter()
   print("\n")

def current_position(list, player_num):       # gets current position of player in game
   for i in range(len(list[player_num-1])):
      if list[player_num-1][i] == player_num:
         return i 

def dev(player_num, list, start_card, cards):  # just a bit of fun..
   passw = "jojo"
   dev = input("enter the [s]ecret code: ")
   if dev != passw:
      print("Imposter!!!!")
   else:
      print("\n")
      print("DEV MODE ACTIVATED!")
      press_enter()
      print("\n")
      move_the_player(list,len(list[player_num])-1,player_num)
      print_allplayer(list)
      print_Start(start_card)
      print_Card(cards)
      print(f"Player {player_num} has won the game!\n")
      sys.exit()


def options(player_num, list, start_card, cards):   # options whether to draw a card, shuffle the deck or to quit, the quit option directly quits the game.
   while True: 
     choice = input("Would you like to draw a [m] card, [s]huffle the deck or [q]uit? ")
     if choice not in ["M","m","S","s","q","Q","d","D"]:
        print("Please enter either [m],[s] or [q]")
        continue
     if choice == "M" or choice == "m":
        print("\n"f"Player {player_num} (Human) has drawn a card")
        return True
     if choice == "S" or choice == "s":
        print(f"Player {player_num} has shuffled the deck")
        press_enter()
        print("\n")
        return False
     if choice == "Q" or choice == "q":
        print("Thank you for playing!")
        sys.exit()
     if choice == "d" or choice == "D":
        dev(player_num, list, start_card, cards)


   
def no_of_human_player():         #asks the user for the number of players, and also returns number of human and AI players
    while True: 
     num = input("\nEnter number of human players(1-4): ")
     try:
        num = int(num)
     except:
        print("Please enter an integer!")
        continue
     if num not in [1,2,3,4]:
        print("Please enter an integer(1-4)..")
        continue
     num_AI = 4-num
     return num,num_AI
    
def AI(start,card):    # AI logic
   if start[0] == card[0]:
        return False
   else:
      return True
   
   
        
   

def working_logos():   #this is where all the working logic resides 
   banner()
   print('Welcome to Candy Land\n')

   choice = user_choice()
   if choice == True:

      print("\nLet the game begin!")

      num_human,num_AI = no_of_human_player()    # gets no of human and AI player
      card = define_card()                       # gets the card specified by the user

      # creating the board and underlying logic
 
      global list                                # needed to be global so as to be accessible down later
      list = board_creation(card)                # creates a board essentially
      

      print("\n")

      #defining index of each player

      player1_index, player2_index, player3_index, player4_index = 0,0,0,0         # the index is just the position of each player in the list, and will change when a card is drawn and will be updated
      record = {1:player1_index, 2:player2_index, 3:player3_index, 4:player4_index}


     # the initial stage

      for i in range(1,5):             # this code keeps the initial player positions in their place, and everyone starts at the same place
         move_the_player(list,0,i)
         print_player(list,i)

      start_card = create_card(card)
      cards = create_card(card)
      print_Start(start_card)
      print_Card(cards)

      def bool_True(cards, start_card, j, list):    # this is the code behind the working of the player movement
         prev = copy.deepcopy(record[j])            # this is part of logic behind displaying how many steps the player moved
         index = card_drop_index(cards,start_card,record[j])   # finds where to drop the player to according to the start card and cards, and returns the index
         move_the_player(list, index, j)            # moves the player to the index we found
         diff = index - prev                        # value of how much the player moved
         space(j, diff)                             # displays number of step player moved on the screen/terminal
         print_allplayer(list)                      # prints the list, and the user is shown the new updated position of player
         record[j] = index                          # updating the current position/ index of the player, and is central to the functioning of the game.
         cards = get_updated_card(cards)            # makes necessary update to the cards
      


      while True:    
       
      # human

          for j in range(1,num_human+1):
          
              bool = options(j,list,start_card,cards)    #asks the user to either move the player, shuffle the card or to quit

              if bool == True:                           # if true the player asked to move the player

                  diff = bool_True(cards, start_card, j, list)

              if bool == False:                           # if false the player asked to shuffle the cards
                  
                  cards = shuffle_card(cards)
                  print_allplayer(list)
              
       
      # start and card for human

              print_Start(start_card)       # printing the start card and cards to the terminal
              print_Card(cards)


      # AI

          for i in range(5-num_AI,5):        # The part of AI 
               
               bool = AI(start_card, cards)
         
               if bool == True:
             
                   print(f"Player {i} (Computer) has drawn a card")
                   bool_True(cards, start_card, i, list)

               if bool == False:
             
                   print(f"Player {i} has shuffled the deck")
                   press_enter()
                   cards = shuffle_card(cards)
                   print_allplayer(list)

               print_Start(start_card)
               print_Card(cards)
      

         
         



def main():      # calling working_logos- the brain of this program
   working_logos()


if __name__ == "__main__":      # make sure its run on this program, and the logic to start this program
   main()

