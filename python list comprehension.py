# change string to a list of characters
language = 'Python'
lst = list(language) 
print(lst)         

lst = [i for i in language]
print(lst)  


numbers = [i for i in range(11)]  
print(numbers)                    

squares = [i * i for i in range(11)]
print(squares)                    

# make a list of tuples
numbers = [(i, i * i) for i in range(11)]
print(numbers)    

even_numbers = [i for i in range(21) if i % 2 == 0] 
print(even_numbers)                  

odd_numbers = [i for i in range(21) if i % 2 != 0]  
print(odd_numbers)

numbers = [-8, -7, -3, -1, 0, 1, 3, 4, 5, 7, 6, 8, 10]
positive_even_numbers = [i for i in numbers if i % 2 == 0 and i > 0]
print(positive_even_numbers)  


# Flattening a two dimensional array
list_of_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened_list = [ number for row in list_of_lists for number in row]
print(flattened_list)  


# lambda
add_two_nums = lambda a, b: a + b
print(add_two_nums(298,362))

# self invoke the lambda function
print((lambda a, b: a + b)(2000,3000))

square = lambda x : x ** 2
print(square(45))    
cube = lambda x : x ** 3
print(cube(45))

multiple_variable = lambda a, b, c: a ** 2 - 3 * b + 4 * c
print(multiple_variable(565, 565, 395))


# lambda function inside another function
def power(x):
    return lambda n : x ** n

cube = power(2)(3)
print(cube)          
two_power_of_five = power(2)(5) 
print(two_power_of_five)  