# import the module
import os
# Creating a directory
os.mkdir('directory_name')
# Changing the current directory
os.chdir('path')
# Getting current working directory
os.getcwd()
# Removing directory
os.rmdir()


import mymodule
print(mymodule.generate_full_name('Kawhi', 'Leonard')) 


from mymodule import generate_full_name, sum_two_nums, person, gravity
print(generate_full_name('Kawhi','Leonard'))
print(sum_two_nums(961,439))
print(person['firstname'])
mass = 100
weight = mass * gravity
print(weight)
