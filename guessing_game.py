# a) use import random
# b) use randint to generate random no. between 1 & 100
# c) we need to guess the correct no.:-
#    but also the range between being too close or far from the correct guessed no.
# d) use if...elif...else to:- diff the letters from the no.
#    and check if that range is considered too low or high? --> learn more on try & except statements
# e) is a loop needed? yes a while loop

import random

expected_match = random.randint(1, 100)

while True:
    try:
        guessed_no = int(input("Guess the number between 1 and 100: "))

        if guessed_no > expected_match:
            print("Too high!")
        elif guessed_no < expected_match:
            print("Too low!")
        else:
            print("Congratulations! You guessed the number.")
            break 
    except:
        print("Please enter a valid number")