import random
import sys, os
from turtle import update

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
    'survival': 0,                   # Boolean whether the user is playing endless mode or not
    }

defender_list = ['ARCHR', 'WALL', 'MINE', 'HEAL', 'CANON', "NUKE"]
monster_list = ['ZOMBI', 'WWOLF', 'SKELE', 'GOLEM']

defenders = {'ARCHR': {'name': 'Archer',
                       'maxHP': 5,
                       'min_damage': 1,
                       'max_damage': 4,
                       'price': 5,
                       'upgrade_cost': 8,
                       'level': 0
                       },
             
             'WALL': {'name': 'Wall',
                      'maxHP': 20,
                      'min_damage': 0,
                      'max_damage': 0,
                      'price': 3,
                      'upgrade_cost': 6,
                      'level': 0
                      },

             'MINE': {'name': 'Mine',
                      'maxHP': 10,
                      'min_damage': 10,
                      'max_damage': 10,
                      'price': 7,
                      'upgrade_cost': 10,
                      'level': 0
                      },

             'HEAL': {'name': 'Heal',
                      'min_damage': 5,
                      'max_damage': 5,
                      'price': 8,
                      'upgrade_cost': 12,
                      'level': 0                     
                     },
            
             'CANON': {'name': 'Cannon',
                      'maxHP': 8,
                      'min_damage': 3,
                      'max_damage': 5,
                      'price': 7,
                      'upgrade_cost': 8,
                      'level': 0                 
                     },

             'NUKE': {'name': 'Nuclear',
                      'min_damage': 15,
                      'max_damage': 15,
                      'price': 12,
                      'upgrade_cost': 15,
                      'level': 0   
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
                      },

            'SKELE': {'name': 'Skeleton',
                      'maxHP': 10,
                      'min_damage': 1,
                      'max_damage': 3,
                      'moves' : 1,
                      'reward': 3
                    },
            
            'GOLEM': {'name': 'Golem',
                      'maxHP': 30,
                      'min_damage': 1,
                      'max_damage': 2,
                      'moves' : 1,
                      'reward': 4
                    }
            }

levels =  {'ARCHR': 0,
           'WALL': 0,
           'MINE': 0,
           'HEAL': 0,
           'CANON': 0,
           'NUKE': 0                                           
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
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]                              # List of letters

    
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
    print("Turn {num:<}     Threat = [{threat:{width}}]     Danger level {danger:<}".format(num=game_vars["turn"], threat=str("-" * game_vars["threat"]), width= game_vars["max_threat"], danger=game_vars["danger_level"]))
    print("Gold = {}".format(game_vars["gold"]), end="   ")

    if game_vars["survival"] == False:
        print("Monsters killed = {}/{}".format(game_vars["monsters_killed"], game_vars["monster_kill_target"]))
    else:
        print("Monsters killed = {}".format(game_vars["monsters_killed"]))


#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu():
    print("1. Buy unit  2. Upgrade Unit   3. End turn")
    print("4. Save game 5. Quit")

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
        upgrade_defender()
    elif choice == 3:
        end_turn(field)
    elif choice == 4:
        save_game(field, game_vars)
    elif choice == 5:
        print("Thank you for playing")
        raise SystemExit()
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
    print("2. Start new Survival Mode")
    print("3. Load saved game")
    print("4. Game Options")
    print("5. Quit")

    try:
        choice = int(input("Your choice? "))
        assert 1 <= choice <= 5
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
        game_vars["survival"] = 1
        game_vars["monster_kill_target"] = -1
        new_game()
    elif option == 3:
        load_game()
    elif option == 4:
        game_options()
    elif option == 5:
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
    letter_columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]  
    position = input("Place where? (X to cancel) ")

    if position.lower() == "x":
        game_vars["gold"] += defenders[unit_name]["price"]
        buy_unit()
    
    else:
        try:
            # Asserts that user input is 2 in length, the first letter is in letter_columns and the second number is between 1 and 3
            assert len(position) == 2
            assert position[0].upper() in letter_columns
            assert 1 <= int(position[1]) <= 3


            # If player is putting down a heal
            if unit_name == "HEAL":
                heal_units(position=position)
            
            elif unit_name == "NUKE":
                nuke_units(position = position)


            # Ensures that player can only put unit in an empty position
            elif field[letter_columns.index(position[0].upper())][int(position[1]) - 1] == None:
                field[letter_columns.index(position[0].upper())][int(position[1]) - 1] = [unit_name, defenders[unit_name]["maxHP"], defenders[unit_name]["maxHP"]]


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
        print("{}. {} ({} gold)".format(i + 1, defenders[defender_list[i]]["name"], defenders[defender_list[i]]["price"]), end="")

        if defender_list[i] == "NUKE":
            print(" **DAMAGES ALLIES**")
            
        else:
            print("")
    
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

#-------------------------------------------------------------------
# upgrade_defender()
#
#   Prompts user for which defender he/she would like to upgrade
#---------------------------------------------------------------------
def upgrade_defender():
    for i in range(len(defender_list)):        
        print("{}. {} ({} gold)".format(i + 1, defenders[defender_list[i]]["name"], defenders[defender_list[i]]["upgrade_cost"]))
    
    print(f"{i + 2}. Don't buy")

    try:
        unit_choice = int(input("Your choice? "))
        assert 1 <= unit_choice <= (len(defender_list) + 1)

        # If user selects DONT BUY, returns to combat menu.
        if (unit_choice == len(defender_list) + 1):
             show_combat_menu()

        else:
            # Checks if user has sufficient gold for purchase
            if game_vars["gold"] >= defenders[defender_list[unit_choice - 1]]["upgrade_cost"]:
                game_vars["gold"] -= defenders[defender_list[unit_choice - 1]]["upgrade_cost"]
                defender_upgrade(unit_choice)
            else:
                print("Insufficient gold!")
                upgrade_defender()

    except (ValueError, AssertionError):
        print("Invalid Upgrade!")
        upgrade_defender()


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
                if field[row][unit][0] in defender_list and field[row][unit][0] != "MINE":
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
    if (game_vars["threat"] >= game_vars["max_threat"]):
            game_vars["threat"] -= game_vars["max_threat"]
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

                # Every other turn, cannon is unable to fire
                if game_vars["turn"] % 2 != 0 and unit == "CANON":
                    print("Charging Cannon...")
                    break


                # Skeletons take half damage from Archers
                if unit == "ARCHR" and field[row][element][0] == "SKELE":
                    damage = round(damage / 2)
                
                # Monster takes damage.
                field[row][element][1] -= damage


                # Prompt damage if unit is not wall.
                if unit != "WALL":
                    print("{} in lane {} shoots {} for {} damage!".format(defenders[unit]["name"], letter_columns[row].upper(), monsters[field[row][element][0]]["name"], damage))
                
                # If the monster dies after taking damage, 
                if field[row][element][1] <= 0:
                    # Make changes to game vars
                    game_vars["monsters_killed"] += 1
                    game_vars["num_monsters"] -= 1
                    game_vars["threat"] += monsters[field[row][element][0]]["reward"]
                    game_vars["gold"] += monsters[field[row][element][0]]["reward"]
                    
                    # print death and remove from board
                    print("{} dies!".format(monsters[field[row][element][0]]["name"]))
                    print("You gain {} gold as a reward.".format(monsters[field[row][element][0]]["reward"]))
                    field[row][element] = None

                    # If monsters_killed == 20, win game!
                    if game_vars["monsters_killed"] == game_vars["monster_kill_target"]:
                        win_game()
                    
                    break
                
                # If units a cannon, 50% chance for knockback
                if unit == "CANON":
                    chance = random.randint(0, 1)
                    if chance == 0 and element != len(field[0]) - 1:
                        if field[row][element + 1] == None:
                            print("Cannon pushes {} back!".format(monsters[field[row][element][0]]["name"]))
                            field[row][element + 1] = field[row][element]
                            field[row][element] = None    

                # Breaks loop after shooting at one monster, as monsters behind are unaffected.
                break

#----------------------------------------------------------
# heal_units()
#
#   Heals units within a 3 x 3 square
#----------------------------------------------------------
def heal_units(position):
    letter_columns = ["a", "b", "c", "d", "e"]
    row, column = letter_columns.index(position[0]), int(position[1]) - 1

    row_addition = 2
    if row == len(letter_columns) - 1:
        row_addition = 1

    for i in range(row - 1, row + row_addition):
        for j in range(column - 1, column + 2):
            if field[i][j] != None and field[i][j][0] in defender_list:
                if field[i][j][1] + defenders["HEAL"]["min_damage"]  > field[i][j][2]:
                    field[i][j][1] += (field[i][j][2] - field[i][j][1])
                else:
                    field[i][j][1] += defenders["HEAL"]["min_damage"] 

    print("Your defenders were healed!")

#------------------------------------------------------------
# nuke_units()
#
#   Nukes all units in a 3x3 square, including defenders
#------------------------------------------------------------
def nuke_units(position):
    letter_columns = ["a", "b", "c", "d", "e"]
    row, column = letter_columns.index(position[0]), int(position[1]) - 1

    row_addition = 2
    if row == len(letter_columns) - 1:
        row_addition = 1

    for i in range(row - 1, row + row_addition):
        for j in range(column - 1, column + 2):
            if field[i][j] != None:
                field[i][j][1] -= defenders["NUKE"]["max_damage"]

                if field[i][j][0] in defender_list:
                    print("Nuke damages {} for {} damage!".format(defenders[field[i][j][0]]["name"], defenders["NUKE"]["max_damage"]))
                elif field[i][j][0] in monster_list:
                    print("Nuke damages {} for {} damage!".format(monsters[field[i][j][0]]["name"], defenders["NUKE"]["max_damage"]))

                if field[i][j][1] < 1:
                    if field[i][j][0] in defender_list:
                        print("{} dies! ".format(defenders[field[i][j][0]]["name"]))
                    elif field[i][j][0] in monster_list:
                        print("{} dies! ".format(monsters[field[i][j][0]]["name"]))
                    
                    field[i][j] = None
            
                    

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
        
        # Golem Monster only attacks every other turn!
        if game_vars["turn"] % 2 == 0 and monster_name == "GOLEM":
            print("Golem readies itself...")
            break

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

            # If the monster steps on a mine
            if field[row][column - 1][0] == "MINE":
                
                # If mine is in Lane E, dont check for next row.
                row_addition = 2
                if row == 4:
                    row_addition = 1

                # Loops through 3 x 3 square (Depends on row)
                for i in range(row - 1, row + row_addition):
                    for j in range(column - 2, column + 1):
                        # If the unit is a monster
                        if field[i][j] != None and field[i][j][0] in monster_list:
                            field[i][j][1] -= defenders["MINE"]["min_damage"]
                            print("Mine in lane {} explodes and deals {} damage!".format(letter_columns[i],  defenders["MINE"]["min_damage"]))

                            # If monster dies
                            if field[i][j][1] <= 0:
                                print("{} dies! ".format(monsters[field[i][j][0]]["name"]))
                                field[i][j] = None

                # Monster advances if its still alive.
                field[row][column - 1] = field[row][column]
                field[row][column] = None

            # IF MONSTER COMES ACROSS REGULAR DEFENDER....
            else:
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
# defender_upgrade()
#   Increases the status of defenders min_damage, max_damage and HP by a certain cost
#--------------------------------------------------------------------
def defender_upgrade(choice):
    
    # If defender is an Archer, increase all stats by 1
    if defender_list[choice - 1] == "ARCHR":
        defenders[defender_list[choice - 1]]["maxHP"] += 1
        defenders[defender_list[choice - 1]]["min_damage"] += 1
        defenders[defender_list[choice - 1]]["max_damage"] += 1
        levels["ARCHR"] += 1

    # If wall, increase HP by 5
    elif defender_list[choice - 1] == "WALL":
        defenders[defender_list[choice - 1]]["maxHP"] += 5
        levels["WALL"] += 1
    
    elif defender_list[choice - 1] == "CANON":
        defenders[defender_list[choice - 1]]["maxHP"] += 1
        defenders[defender_list[choice - 1]]["max_damage"] += 2
        defenders[defender_list[choice - 1]]["min_damage"] += 2
        levels["CANON"] += 1

    else:
        defenders[defender_list[choice - 1]]["max_damage"] += 2
        defenders[defender_list[choice - 1]]["min_damage"] += 2

        levels[defender_list[choice - 1]] += 1
    

    # Increase defender costs incrementing by 2
    defenders[defender_list[choice - 1]]["upgrade_cost"] += 2

    print("{} upgraded!".format(defenders[defender_list[choice - 1]]["name"]))

    show_combat_menu()


#--------------------------------------------------------------------
# monster_upgrade()
#
#   Increases the stats of monsters min_damage, max_damage, and HP.
#---------------------------------------------------------------------
def monster_upgrade(monsters):

    print("The evil grows stronger!\n")

    game_vars["danger_level"] += 1

    for i in monsters:
        monsters[i]["maxHP"] += 1
        monsters[i]["min_damage"] += 1
        monsters[i]["max_damage"] += 1
        monsters[i]["reward"] += 1

#--------------------------------------------------------------------
# update_levels()
#
#   Updates the defenders and monsters levels after loading a saved game
#---------------------------------------------------------------------  
def update_levels(defender_levels, danger_level):
    for i in monsters:
        monsters[i]["maxHP"] += danger_level
        monsters[i]["min_damage"] += danger_level
        monsters[i]["max_damage"] += danger_level
        monsters[i]["reward"] += danger_level

    for i, key in enumerate(levels):
        levels[key] = defender_levels[i]

    for i in defenders:
        if i == "ARCHR":
            defenders[i]["maxHP"] += levels[i]
            defenders[i]["min_damage"] += levels[i]
            defenders[i]["max_damage"] += levels[i]

        elif i == "WALL":
            defenders[i]["maxHP"] += (levels[i] * 5)
        
        elif i == "CANON":
            defenders[i]["maxHP"] += levels[i]
            defenders[i]["min_damage"] += (levels[i] * 2)
            defenders[i]["max_damage"] += (levels[i] * 2)

        else:
            defenders[i]["min_damage"] += (levels[i] * 2)
            defenders[i]["max_damage"] += (levels[i] * 2) 

        defenders[i]["upgrade_cost"] += (levels[i] * 2)    



    

#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------
def spawn_monster(monster_list):

    if (game_vars["num_monsters"] < 5):

        random_row = random.randint(0, len(field) - 1)
        random_monster_num = random.randint(0, 1)

        random_row = random.randint(0, 4)                                   # Random integer for random row
        random_monster_num = random.randint(0, len(monster_list) - 1)       # Random integer for random monster

        monster = monster_list[random_monster_num]                          # Gets a monster between Zombies and Werewolves 
        monster_health = monsters[monster]['maxHP']                         # Saves the monster's starting health to a new variable
        monster_maxHP = monsters[monster]['maxHP']

        # If the space is empty, spawn a monster
        if field[random_row][-1] == None:  
            field[random_row][-1] = [monster, monster_health, monster_maxHP]    # Sets the value in the field as a list with [name, health]
            game_vars["num_monsters"] += 1
        # Else, redo the function until get an empty space (Ensures that monsters aren't replaced)
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

    if game_vars["survival"] == 1:
        print("You survived a total of {} turns and killed {} monsters!".format(game_vars["turn"], game_vars["monsters_killed"]))

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

        # Converts defender levels into a list of strings
        defender_levels = [str(x) for x in levels.values()]

        # Saves first line as game variables
        save_file.writelines(",".join(variables))
        
        save_file.write("\n")

        save_file.writelines(",".join(defender_levels))

        save_file.write("\n")

        # Loops through every row in field
        for row in field:
            # Saves every element of row as a list of strings
            elements = [str(x) for x in row]
            # Saves list of elements as a single string joined by a "-"
            save_file.writelines("-".join(elements))
            save_file.write("\n")

        save_file.close()
    
    show_combat_menu()
    
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

        if len(variables_and_field) != len(field) + 2:
            print("Failed to load save file...Returning to main menu")
            show_main_menu()
        else:
            # First line is game variables
            game_variables = variables_and_field[0].strip("\n").split(",")

            # Second line is defender levels, using list comprehension to convert back into integer
            defender_levels = [int(x) for x in variables_and_field[1].strip("\n").split(",")]

            # enumerate creates an index value pair, e.g., (0, turn), (1, maxHP)
            for i, j  in enumerate(game_vars):
                game_vars[j] = int(game_variables[i])
            
            # Updates monster and defender levels
            update_levels(defender_levels, game_vars["danger_level"])

            # For every row in field
            for row in range(len(field)):
                # Temp row is the second line onwards of the txt file split into a list.
                temp_row = variables_and_field[row + 2].strip("\n").split("-")

                # For every element in each row
                for column in range((len(field[0]))):
                    # If it is "None" in the txt file, the element becomes NoneType
                    if temp_row[column] == "None":
                        field[row][column] = None

                    # If it is not None, split the list into 3, then save the first (name), second (hp) and third (maxHP) values accordingly
                    else:
                        temp_info = temp_row[column].strip("]").strip("[").split(",")
                        field[row][column] = [temp_info[0].strip("'"), int(temp_info[1]), int(temp_info[2])]

            draw_field()

        save_file.close()
        
#-----------------------------------------
# game_options()
#
#    Allows user to specify threat levels, etc.
#-----------------------------------------
def game_options():
    print("\n---------------------SETTINGS---------------------")
    print("1. Threat Level")
    print("2. Monster Kill Target")

    print("3. Back to Main Menu")

    choice = int(input("Which setting would you like to change? "))

    try:
        assert 1 <= choice <= 3

        if choice == 1:
            threat_level = int(input("Enter the max threat: (The higher the easier, MAX 30)"))

            if threat_level < 5 or threat_level > 30:
                print("Invalid Threat Level! (Min 5, Max 30)")
                game_options()
            else:
                game_vars["max_threat"] = threat_level
                game_options()

        elif choice == 2:
            kill_target = int(input("Enter the monster kill target: (Min 5)"))

            if kill_target < 5:
                print("Invalid Monster Kill Target! (Min 5)")
                game_options()
            
            else:
                game_vars["monster_kill_target"] = kill_target
                game_options()
        
        elif choice == 3:
            show_main_menu()


    except (AssertionError, ValueError):
        print("Invalid input!")
        game_options()


    

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

show_main_menu()




# TO DO: ADD YOUR CODE FOR THE MAIN GAME HERE!
    
    
