import random
import sys, os

# Game variables
game_vars = {
    'turn': 0,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    'threat': 0,                    # Current threat metre level
    'max_threat': 10,               # Length of threat metre
    'danger_level': 1,              # Rate at which threat increases
    }

defender_list = ['ARCHR', 'WALL']
monster_list = ['ZOMBI', 'WWOLF']

defenders = {'ARCHR': {'name': 'Archer',
                       'maxHP': 5,
                       'min_damage': 1,
                       'max_damage': 4,
                       'price': 5,
                       },
             
             'WALL': {'name': 'Wall',
                      'maxHP': 20,
                      'min_damage': 0,
                      'max_damage': 0,
                      'price': 3,
                      }
             }

monsters = {'ZOMBI': {'name': 'Zombie',
                      'maxHP': 15,
                      'min_damage': 3,
                      'max_damage': 6,
                      'moves' : 1,
                      'reward': 2
                      },

            'WWOLF': {'name': 'Werewolf',
                      'maxHP': 10,
                      'min_damage': 1,
                      'max_damage': 4,
                      'moves' : 2,
                      'reward': 3
                      }
            }

field = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]


#----------------------------------------------------------------------
# draw_field()
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#      in the first 3 columns
#----------------------------------------------------------------------

def draw_field():
    letters = ["A", "B", "C", "D", "E"]                             # List of letters

    
    print(" {:^7}{:^6}{:^5}".format(1, 2, 3))                        # prints out the header numbers

    for i in range(len(field)):                                     # Loops through len of rows
        print(" +-----+-----+-----+-----+-----+-----+-----+")       # prints header every row

        print(letters[i], end="")                                   # Before printing field, prints letter
        for j in range(len(field[i])):         
            if field[i][j] != None:                     # loops through every element in each row, prints out name
                print("|{:<5}".format(field[i][j][0]), end="")
            else:
                print("|{:<5}".format(""), end="")

        print("|")      

        print(" ",end="")                                           # Extra space so field is even
        for h in range(len(field[i])):                              # Loops through ever element in each row and prints out health
            if field[i][h] != None:  
                if field[i][h][0] in monster_list:                   
                    print("|{:>2}/{:<2}".format(field[i][h][1], field[i][h][2]), end="")
                elif field[i][h][0] in defender_list:
                    print("|{:>2}/{:<2}".format(field[i][h][1], field[i][h][2]), end="")
            else:
                print("|{:<5}".format(""), end="")
            

        print("|")      
    
    print(" +-----+-----+-----+-----+-----+-----+-----+")

    show_game_vars()
    show_combat_menu()

#----------------------------
# show_game_vars()
#
#   Displays the game variables
#----------------------------
def show_game_vars():
    print("Turn {:<}     Threat = [{:<10}]     Danger level {:<}".format(game_vars["turn"], "-" * game_vars["threat"], game_vars["danger_level"]))
    print("Gold = {}   Monsters killed = {}/20".format(game_vars["gold"], game_vars["monsters_killed"]))


#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu():
    print("1. Buy unit     2. End turn")
    print("3. Save game    4. Quit")

    try:                                                    # Prompts user for choice, ensures no invalid inputs. 
        combat_choice = int(input("Your choice? "))
        check_combat_choice(combat_choice)

    except (ValueError):                                                 # Rerun the function if invalid
        print("Invalid input!")
        show_combat_menu()

#------------------------------------
# check_combat_choice(choice)
# 
#       Checks user's input for combat
#-------------------------------------
def check_combat_choice(choice):
    if choice == 1:
        buy_unit()
    elif choice == 2:
        end_turn(field)
    elif choice == 3:
        save_game(field, game_vars)
    elif choice == 4:
        print("Thank you for playing")
    else:
        print("Invalid input!")
        
        show_combat_menu()


#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Quit")

    try:
        choice = int(input("Your choice? "))
        assert 1 <= choice <= 3
        
        menu_check(choice)

    except (ValueError, AssertionError):

        print("Invalid choice!")
        show_main_menu()
   
#----------------------------
# menu_check(option)
#
#    Checks the users option in the main menu
#----------------------------
def menu_check(option):
    if option == 1:
        new_game()
    elif option == 2:
        load_game()
    elif option == 3:
        print("See you next time!")


#-----------------------------------------------------
# place_unit()
#
#    Places a unit at the given position
#    This function works for both defender and monster
#    Returns False if the position is invalid
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#    Returns True if placement is successful
#-----------------------------------------------------

def place_unit(unit_name, field):       
    letter_columns = ["a", "b", "c", "d", "e"]
    position = input("Place where? ")

    try:
        # Asserts that user input is 2 in length, the first letter is in letter_columns and the second number is between 1 and 3
        assert len(position) == 2
        assert position[0].lower() in letter_columns
        assert 1 <= int(position[1]) <= 3

        # Ensures that player can only put unit in an empty position
        if field[letter_columns.index(position[0])][int(position[1]) - 1] == None:
            field[letter_columns.index(position[0])][int(position[1]) - 1] = [unit_name, defenders[unit_name]["maxHP"], defenders[unit_name]["maxHP"]]
        
        # If there is already a unit there, warns the player and reruns the function.
        else:
            print("There is already a unit there!")
            place_unit(unit_name, field)

        end_turn(field)

    except (ValueError, AssertionError):                                                         
        print("Invalid position!")
        place_unit(unit_name, field)  

#-------------------------------------------------------------------
# buy_unit()
#
#    Allows player to buy a unit and place it using place_unit()
#-------------------------------------------------------------------
def buy_unit():                                    
    print("What unit do you wish to buy?")

    # Loops through defender list, prints out name and price of each defender
    for i in range(len(defender_list)):        
        print("{}. {} ({} gold)".format(i + 1, defenders[defender_list[i]]["name"], defenders[defender_list[i]]["price"]))
    
    print(f"{i + 2}. Don't buy")

    # Prompts user for unit they wish to purchase
    try:
        unit_choice = int(input("Your choice? "))
        assert 1 <= unit_choice <= (len(defender_list) + 1)

        # If user selects DONT BUY, returns to combat menu.
        if (unit_choice == len(defender_list) + 1):
             show_combat_menu()

        else:
            # Checks if user has sufficient gold for purchase
            if game_vars["gold"] >= defenders[defender_list[unit_choice - 1]]["price"]:
                game_vars["gold"] -= defenders[defender_list[unit_choice - 1]]["price"]
                place_unit(defender_list[unit_choice - 1], field)
            else:
                print("Insufficient gold!")
                buy_unit()

    except (ValueError, AssertionError):
        print("Invalid Unit!")
        buy_unit()

#--------------------------------------------------------------------
# end_turn()
#
#   Ends the turn and runs the necessary code.
#-------------------------------------------------------------------------
def end_turn(field):
    # Changes the game turn
    game_vars["turn"] += 1

    # Checks every unit in every row, if its a defender, defender_attack(), monster_attack() if its a monster, ignore if None
    for row in range(len(field)):
        for unit in range(len(field[row])):
            if field[row][unit] != None:
                if field[row][unit][0] in defender_list:
                    defender_attack(field[row][unit][0], field, row, unit)    
                elif field[row][unit][0] in monster_list:
                    monster_advance(field[row][unit][0], field, row, unit)
    
    # Every 12 turns, danger level increases
    if game_vars["turn"] % 12 == 0:
         monster_upgrade(monsters=monsters)

    # If no more mosters in field, spawn_monster
    if monster_check(field) == True:
        spawn_monster(monster_list)

    # Increase threat amount by random number between 1 and danger level
    game_vars["threat"] += random.randint(1, game_vars["danger_level"])
    
    # If threat level reaches 10, subtract by 10 and spawn a new monster.
    if (game_vars["threat"] >= 10):
            game_vars["threat"] -= 10
            spawn_monster(monster_list=monster_list)

    game_vars["gold"] += 1
    draw_field()

#-------------------------------------------------------------------------------------
# monster_check(field)
#                   Checks if there are monsters in the field, if not, spawn_monster()
#-------------------------------------------------------------------------------------
def monster_check(field):
    for i in field:
        for j in i:
            if j != None:
                # Returns False if there is a monster on the field.
                if j[0] in monster_list:
                    return False
    
    return True


#-----------------------------------------------------------
# defender_attack()
#
#    Defender unit attacks.
#    
#-----------------------------------------------------------
def defender_attack(unit, field, row, column):
    letter_columns = ["a", "b", "c", "d", "e"]

    max_dmg = defenders[unit]["max_damage"]
    min_dmg = defenders[unit]["min_damage"]

    # Loops through every unit to the right of the defender.
    for element in range(column, len(field[row])):
        # If its not none
        if field[row][element] != None:
            # If the unit is a monster:
            if field[row][element][0] in monster_list:
                damage = random.randint(min_dmg, max_dmg)
                field[row][element][1] -= damage

                # Prompt damage if unit is not wall.
                if unit != "WALL":
                    print("{} in lane {} shoots {} for {} damage!".format(defenders[unit]["name"], letter_columns[row].upper(), monsters[field[row][element][0]]["name"], damage))
                
                # If the monster dies after taking damage, 
                if field[row][element][1] <= 0:
                    # Make changes to game vars
                    game_vars["monsters_killed"] += 1
                    game_vars["threat"] += monsters[field[row][element][0]]["reward"]
                    game_vars["gold"] += monsters[field[row][element][0]]["reward"]
                    
                    # print death and remove from board
                    print("{} dies!".format(monsters[field[row][element][0]]["name"]))
                    print("You gain {} gold as a reward.".format(monsters[field[row][element][0]]["reward"]))
                    field[row][element] = None

                    # If monsters_killed == 20, win game!
                    if game_vars["monsters_killed"] == 20:
                        win_game()
                
                # Breaks loop after shooting at one monster, as monsters behind are unaffected.
                break
                    

#-----------------------------------------------------------
# monster_advance()
#
#    Monster unit advances.
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#-----------------------------------------------------------
def monster_advance(monster_name, field, row, column):

    letter_columns = ["A", "B", "C", "D", "E"]

    max_dmg = monsters[monster_name]["max_damage"]
    min_dmg = monsters[monster_name]["min_damage"]

    damage = random.randint(min_dmg, max_dmg)

    # Loops through the number of turns a monster has
    for i in range(monsters[monster_name]["moves"]):

        # If the next move passes the field, player loses.
        if column - 1 < 0:
            print("A {} has reached the city! All is lost!".format(monsters[monster_name]["name"]))
            lose_game() 

        # If there is nothing in front of the monster
        if field[row][column - 1] == None:
            field[row][column - 1] = field[row][column]
            field[row][column] = None

            print("{} in lane {} advances!".format(monsters[monster_name]["name"], letter_columns[row]))

            # column - 1 to change the position of the monster
            column -= 1
        
        # If there is a defender in front of the monster
        elif field[row][column - 1][0] in defender_list:
            field[row][column - 1][1] -= damage
            print("{} in lane {} hits {} for {} damange!".format(monsters[monster_name]["name"], letter_columns[row], defenders[field[row][column - 1][0]]["name"], damage))

            # If defender dies
            if field[row][column - 1][1] <= 0:
                print("{} dies! ".format(defenders[field[row][column - 1][0]]["name"]))
                field[row][column - 1] = field[row][column]
                field[row][column] = None
        
        # If there is a monster in front of the monster
        elif field[row][column - 1][0] in monster_list:
            print("{} in lane {} is blocked from advancing.".format(monsters[monster_name]["name"], letter_columns[row]))
        
        

            
#--------------------------------------------------------------------
# monster_upgrade()
#
#   Increases the stats of monsters min_damage, max_damage, and HP.
#---------------------------------------------------------------------
def monster_upgrade(monsters):

    print("The evil gros stronger!\n")

    game_vars["danger_level"] += 1

    for i in monsters:
        monsters[i]["maxHP"] += 1
        monsters[i]["min_damage"] += 1
        monsters[i]["max_damage"] += 1
        monsters[i]["reward"] += 1
        

    

#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------
def spawn_monster(monster_list):
    random_row = random.randint(0, 4)
    random_monster_num = random.randint(0, 1)

    random_row = random.randint(0, 4)                                   # Random integer for random row
    random_monster_num = random.randint(0, 1)                           # Random integer for random monster

    monster = monster_list[random_monster_num]                          # Gets a monster between Zombies and Werewolves 
    monster_health = monsters[monster]['maxHP']                         # Saves the monster's starting health to a new variable
    monster_maxHP = monsters[monster]['maxHP']

    if field[random_row][-1] == None:  
        field[random_row][-1] = [monster, monster_health, monster_maxHP]    # Sets the value in the field as a list with [name, health]
    else:
        spawn_monster(monster_list)
    
    
#-----------------------------------------
# win_game()
#-----------------------------------------
#   Prompts that the user has won the game.
#-----------------------------------------
def win_game():
    print("You have won the game!")
    raise SystemExit(0)

#-----------------------------------------
# lose_game()
#-----------------------------------------
#   Prompts that the user has lost the game.
#-----------------------------------------
def lose_game():
    print("You have lost the game!")
    raise SystemExit(0)

# save_game()
#
#    Saves the game in the file 'save.txt'
#-----------------------------------------
def save_game(field, game_vars):
    with open("save.txt", "w") as save_file:
        print("Game saved.")

        # Converts game_vars to list of strings
        variables = [str(x) for x in game_vars.values()]
        
        # Saves first line as game variables
        save_file.writelines(",".join(variables))
        
        save_file.write("\n")

        # Loops through every row in field
        for row in field:
            # Saves every element of row as a list of strings
            field_row = [str(x) for x in row]
            # Saves list of elements as a single string joined by a "-"
            save_file.writelines("-".join(field_row))
            save_file.write("\n")

        save_file.close()
    
#-----------------------------------------
# load_game()
#
#    Loads the game from 'save.txt'
#-----------------------------------------
def load_game():
    with open("save.txt", "r") as save_file:
        print("Loading saved game....")
        
        # List of lines
        variables_and_field = save_file.readlines()

        if len(variables_and_field) != 6:
            print("Failed to load save file...Returning to main menu")
            show_main_menu()
        
        # First line is game variables
        game_variables = variables_and_field[0].strip("\n").split(",")

        # enumerate creates an index value pair, e.g., (0, turn), (1, maxHP)
        for i, j  in enumerate(game_vars):
            game_vars[j] = int(game_variables[i])
        
        # For every row in field
        for row in range(len(field)):
            # Temp row is the second line onwards of the txt file split into a list.
            temp_row = variables_and_field[row + 1].strip("\n").split("-")
            
            # For every element in each row
            for column in range((len(field[0]))):
                # If it is "None" in the txt file, the element becomes NoneType
                if temp_row[column] == "None":
                    field[row][column] = None
                
                # If it is not None, split the list into 3, then save the first (name), second (hp) and third (maxHP) values accordingly
                else:
                    temp_info = temp_row[column].strip("]").strip("[").split(",")
                    field[row][column] = [temp_info[0].strip("'"), int(temp_info[1]), int(temp_info[2])]
        
        save_file.close()
        
    draw_field()


#-----------------------------------------
# new_game()
#
#    Initializes a new game
#-----------------------------------------
def new_game():
    initialize_game()
    spawn_monster(monster_list=monster_list)
    draw_field()

#-----------------------------------------------------
# initialize_game()
#
#    Initializes all the game variables for a new game
#-----------------------------------------------------
def initialize_game():
    game_vars['turn'] = 0
    game_vars['monster_kill_target'] = 20
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 10
    game_vars['threat'] = 0
    game_vars['danger_level'] = 1
    

#-----------------------------------------
#               MAIN GAME
#-----------------------------------------

print("Desperate Defenders")
print("-------------------")
print("Defend the city from undead monsters!")
print()

main_menu_choice = show_main_menu()




# TO DO: ADD YOUR CODE FOR THE MAIN GAME HERE!
    
    
