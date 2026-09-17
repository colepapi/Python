# without parameters
def generate_full_name ():
    first_name = input("first_name: ")
    last_name = input("last_name: ")
    space = ' '
    full_name = first_name + space + last_name
    return full_name
print(generate_full_name())


def add_two_numbers ():
    num_one = int(input("num_one: "))
    num_two = int(input("num_two: "))
    total = num_one + num_two
    return total
print(add_two_numbers())


# return a string
def that_name(firstname):
    return firstname
print(that_name('Kawhi')) 

def full_name(firstname, lastname):
    space = ' '
    full_name = firstname  + space + lastname
    return full_name
print(full_name(firstname='Kawhi', lastname='Leonard')) 

# return a number
def add_two_numbers (num1, num2):
    total = num1 + num2
    return total
print(add_two_numbers(296, 354))

'''def add_two_numbers (num1, num2):
    print(num1 + num2)
add_two_numbers(5000, 3000) '''

def calculate_age (current_year, birth_year):
    age = current_year - birth_year
    return age
print('Age: ', calculate_age(2027, int(input("Enter birth_year: "))))

# return a boolean
def is_even (n):
    if n % 2 == 0:
        return True   
    return False
print(is_even(10))
print(is_even(7)) 

# return a list
def find_even_numbers(n):
    evens = []
    for i in range(n + 1):
        if i % 2 == 0:
            evens.append(i)
    return evens
print(find_even_numbers(88))


# with parameters
def greetings (name):
    message = 'Welcome to the NBA ' + name
    return message

print(greetings('Kawhi Leonard'))

def add_ten(num):
    ten = 10
    return num + ten
print(add_ten(90))

def square_number(x):
    return x * x
print(square_number(36))

'''def square_number(x):
    print(x * x)
square_number(int(input("Enter number: "))) '''

def area_of_circle (r):
    PI = 3.14
    area = PI * r ** 2
    return area
print(area_of_circle(280))

def sum_of_numbers(n):
    total = 0
    for i in range(n+1):
        total+=i
    return total
print(sum_of_numbers(10)) 
print(sum_of_numbers(100)) 


def generate_full_name (first_name, last_name):
    space = ' '
    full_name = first_name + space + last_name
    return full_name
print('Full Name: ', generate_full_name('Kawhi','Leonard'))

def sum_two_numbers (num_one, num_two):
    sum = num_one + num_two
    return sum
print('Sum of two numbers: ', sum_two_numbers(568, 932))

def calculate_age (current_year, birth_year):
    age = current_year - birth_year
    return age 
print('Age: ', calculate_age(2027, 1978))

def weight_of_object (mass, gravity):
    weight = str(mass * gravity)+ 'N' 
    return weight
print('Weight of an object: ', weight_of_object(100, 9.81))


# pass arguments with value and key
def print_fullname(firstname, lastname):
    space = ' '
    full_name = firstname  + space + lastname
    print(full_name)
print_fullname(firstname = 'Kawhi', lastname = 'Leonard')

def add_two_numbers (num1, num2):
    total = num1 + num2
    return total
print(add_two_numbers(num2 = 568, num1 = 942))


# default parameters
def greetings (name = 'Peter'):
    message = 'Welcome to our company ' + name
    return message
print(greetings())
print(greetings('Ashley Williams'))

def generate_full_name (first_name = 'Kawhi', last_name = 'Leonard'):
    space = ' '
    full_name = first_name + space + last_name
    return full_name

print(generate_full_name())
print(generate_full_name('David','Smith'))

def calculate_age (birth_year,current_year = 2027):
    age = current_year - birth_year
    return age 
print('Age: ', calculate_age(1997))

def weight_of_object (mass, gravity = 9.81):
    weight = str(mass * gravity)+ 'N' 
    return weight
print('Weight of an object: ', weight_of_object(100)) 
print('Weight of an object: ', weight_of_object(100, 1.62)) 


# arbitrary number of arguments
def sum_all_nums(*nums):
    total = 0
    for num in nums:
        total += num  
    return total
print(sum_all_nums(2, 3, 5))

def generate_groups (team,*args):
    print(team)
    for i in args:
        print(i) 
generate_groups('Team-1','Leonard','Brooks','Edwards','Tina')


# dictionary unpacking
def greet(name, location):    
    print("Hi there", name, "how is the weather in", location) 
my_dict = {"name": "Alice", "location": "New York"}
greet(**my_dict)  


# functions that take other functions as arguments
def square_number (n):
    return n ** n
def do_something(f, x):
    return f(x)
print(do_something(square_number, 3))  


def sum_numbers(nums): 
    return sum(nums)    

def higher_order_function(f, lst): 
    summation = f(lst)
    return summation
result = higher_order_function(sum_numbers, [1, 2, 3, 4, 5])
print(result)     


# function as a return value
def square(x):          
    return x ** 2

def cube(x):            
    return x ** 3

def absolute(x):        
    if x >= 0:
        return x
    else:
        return -(x)

def higher_order_function(type): 
    if type == 'square':
        return square
    elif type == 'cube':
        return cube
    elif type == 'absolute':
        return absolute

result = higher_order_function('square')
print(result(69))      
result = higher_order_function('cube')
print(result(48))       
result = higher_order_function('absolute')
print(result(-3))     


# python closures
def add_ten():
    ten = 110
    def add(num):
        return num + ten
    return add

closure_result = add_ten()
print(closure_result(990))  
print(closure_result(1890))  


# create decorators
def uppercase_decorator(function):
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase
    return wrapper
@uppercase_decorator
def greeting():
    return 'Welcome to Python'
print(greeting()) 

# apply multiple decorators to a single function
def uppercase_decorator(function):
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase
    return wrapper

def split_string_decorator(function):
    def wrapper():
        func = function()
        splitted_string = func.split()
        return splitted_string
    return wrapper

@split_string_decorator
@uppercase_decorator   
def greeting():
    return 'Welcome to Python'
print(greeting())

# decorator that accepts parameters
def decorator_with_parameters(function):
    def wrapper_accepting_parameters(para1, para2, para3):
        function(para1, para2, para3)
        print("I live in {}".format(para3))
    return wrapper_accepting_parameters

@decorator_with_parameters
def print_full_name(first_name, last_name, country):
    print("I am {} {}. I love to play basketball.".format(
        first_name, last_name))

print_full_name("Kawhi", "Leonard",'Los Angeles')


# map() - takes a function and iterable as parameters
numbers = [52, 69, 37, 88, 40] 
def square(x):
    return x ** 2
numbers_squared = map(square, numbers)
print(list(numbers_squared))

numbers_squared = map(lambda x : x ** 2, numbers)
print((numbers_squared)) 

numbers_str = ['1', '2', '3', '4', '5']  
numbers_int = map(int, numbers_str)
print(list(numbers_int))    

names = ['Kawhi', 'Lidiya', 'Ermias', 'Abraham'] 
def change_to_upper(name):
    return name.upper()
names_upper_cased = map(change_to_upper, names)
print(list(names_upper_cased))   

names_upper_cased = map(lambda name: name.upper(), names)
print(list(names_upper_cased))    


# filter
numbers = [52, 69, 37, 88, 40]  
def is_even(num):
    if num % 2 == 0:
        return True
    return False
even_numbers = filter(is_even, numbers)
print(list(even_numbers))     

numbers = [52, 69, 37, 88, 40]  
def is_odd(num):
    if num % 2 != 0:
        return True
    return False
odd_numbers = filter(is_odd, numbers)
print(list(odd_numbers)) 

# Filter long name
names = ['Jeniffer', 'Lidiya', 'Ermias', 'Abraham']  
def is_name_long(name):
    if len(name) > 7:
        return True
    return False
long_names = filter(is_name_long, names)
print(list(long_names)) 


# reduce
from functools import reduce

numbers_str = ['185', '245', '362', '484', '578'] 
def add_two_nums(x, y):
    return int(x) + int(y)
total = reduce(add_two_nums, numbers_str)
print(total)   


# spreading
lst_one = [1, 2, 3]
lst_two = [4, 5, 6, 7]
lst = [0, *lst_one, *lst_two]
print(lst)          

country_lst_one = ['Finland', 'Sweden', 'Norway']
country_lst_two = ['Denmark', 'Iceland']
nordic_countries = [*country_lst_one, *country_lst_two]
print(nordic_countries)  


# enumerate
for index, item in enumerate([20, 30, 40]):
    print(index, item)

countries = ['Finland', 'Sweden', 'Norway', 'Denmark', 'Iceland']
for index, i in enumerate(countries):
    if i == 'Finland':
        print(f'{i} : {index}')


# zip
fruits = ['banana', 'orange', 'mango', 'lemon', 'lime']                    
vegetables = ['Tomato', 'Potato', 'Cabbage','Onion', 'Carrot']
fruits_and_veges = []
for f, v in zip(fruits, vegetables):
    fruits_and_veges.append({'fruit':f, 'veg':v})
print(fruits_and_veges)