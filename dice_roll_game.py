# a) if user selects yes continue, if no exits the game & if uses other letters apart from y/n consider it invalid choice
# b) include input where the user can make y/n choice
# c) use range since dice has 6 sides? --> & there needs to be 2 dices
# d) use random import
# e) use logical operator 'OR'? no there is a simpler way
# f) is a function needed? no

import random

while True:
    user_choice = input("Roll the dice? (y/n): ").lower()

    if user_choice == "y":
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)
        print(f"({die1}, {die2})")
    elif user_choice == "n":
        print("Thanks for playing the roll dice game")
        break
    else:
        print("Invalid choice!")
