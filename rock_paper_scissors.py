# a) user chooses between the 3 any other choice is invalid
# b) playing the game against the comp
# c) whether you win or lose the game gives one the option to continue or quit(y/n)
# d) in order to win:- rock beats scissors, scissors beats paper, paper beats rock
# e) is a loop or a function required? --> yes while true loop & function for refactoring of the code
# f) modularizing the function as follows: user enters their choice, see the users choice, what happens everytime the user enters the choice
#    in order to determine the winner of the game, continue/quit of the game
# g) are if...elif...else as well as try...except statements required? --> try...except statements not required

import random

rock = 'r'
paper = 'p'
scissors = 's'
games_emojis = {rock:'🪨', paper:'📃', scissors:'✂️'}
games_choices = tuple(games_emojis)

def entry_for_user():
    while True:
        user_choice = input('Rock, paper, or scissors? (r/p/s): ').lower()
        if user_choice in games_choices:
            return user_choice
        else:
            print('Invalid Choice!')

def show_choices():
    print(f'You chose {games_emojis[user_choice]}')
    print(f'Computer chose {games_emojis[comp_choice]}')

def decision_makers():
    if user_choice == comp_choice:
        print("Tied!")
    elif (
        (user_choice == rock and comp_choice == paper) or
        (user_choice == scissors and comp_choice == rock) or
        (user_choice == paper and comp_choice == scissors)):
        print("You Lose!")
    else:
        print('You Win!')

def game_on():
    while True: 
        user_choice = entry_for_user()

        comp_choice = random.choice(games_choices)

        show_choices()

        decision_makers()

        move_on = input('Continue? (y/n): ').lower()
        if move_on != 'y' or move_on == 'n':
            break