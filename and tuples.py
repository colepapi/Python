empty_list = list()  
print(len(empty_list))  


fruits = ['banana', 'orange', 'mango', 'lemon']
vegetables = ['Tomato', 'Potato', 'Cabbage',
              'Onion', 'Carrot']     
animal_products = ['milk', 'meat', 'butter',
                   'yoghurt']             
web_techs = ['HTML', 'CSS', 'JS', 'React', 'Redux',
             'Node', 'MongDB'] 
countries = ['Finland', 'Estonia', 'Denmark', 'Sweden', 'Norway']


print('Fruits:', fruits)
print('Number of fruits:', len(fruits))
print('Vegetables:', vegetables)
print('Number of vegetables:', len(vegetables))
print('Animal products:', animal_products)
print('Number of animal products:', len(animal_products))
print('Web technologies:', web_techs)
print('Number of web technologies:', len(web_techs))
print('Number of countries:', len(countries))


# Replace
fruits = ['banana', 'orange', 'mango', 'lemon']
fruits[0] = 'Avocado'
fruits[1] = 'apple'
print(fruits) 

fruits = ['banana', 'orange', 'mango', 'lemon']
does_exist = 'banana' in fruits
print(does_exist)
does_exist = 'lime' in fruits
print(does_exist)


# Append - adding to the list
fruits = ['banana', 'orange', 'mango', 'lemon']
fruits.append('apple')          
fruits.append('lime')
print(fruits)


# insert
fruits = ['banana', 'orange', 'mango', 'lemon']
fruits.insert(2, 'apple')  
print(fruits)           
fruits.insert(3, 'lime')
print(fruits)


# remove
fruits = ['banana', 'orange', 'mango', 'lemon']
fruits.remove('banana')
print(fruits)  
fruits.remove('lemon')
print(fruits)  

# pop - removes the last item on the list
fruits = ['banana', 'orange', 'mango', 'lemon']
fruits.pop()
print(fruits)


# del
fruits = ['banana', 'orange', 'mango', 'lemon']
del fruits[0]
print(fruits)
del fruits[1]
print(fruits)


# clear
fruits = ['banana', 'orange', 'mango', 'lemon']
fruits.clear()
print(fruits)


# copy
fruits = ['banana', 'orange', 'mango', 'lemon']
fruits_copy = fruits.copy()
print(fruits_copy)


# join
positive_numbers = [1, 2, 3, 4, 5]
zero = [0]
negative_numbers = [-5, -4, -3, -2, -1]
integers = negative_numbers + zero + positive_numbers
print(integers)
fruits = ['banana', 'orange', 'mango', 'lemon']
vegetables = ['Tomato', 'Potato', 'Cabbage', 'Onion', 'Carrot']
fruits_and_vegetables = fruits + vegetables
print(fruits_and_vegetables)


# join with extend
num1 = [0, 1, 2, 3]
num2 = [4, 5, 6]
num1.extend(num2)
print('Numbers:', num1)

negative_numbers = [-5, -4, -3, -2, -1]
positive_numbers = [1, 2, 3, 4, 5]
zero = [0]
negative_numbers.extend(zero)
negative_numbers.extend(positive_numbers)
print('Integers:', negative_numbers)

fruits = ['banana', 'orange', 'mango', 'lemon']
vegetables = ['Tomato', 'Potato', 'Cabbage', 'Onion', 'Carrot']
fruits.extend(vegetables)
print('Fruits and vegetables:', fruits)


# count
fruits = ['banana', 'orange', 'mango', 'lemon']
print(fruits.count('orange')) 

ages = [22, 19, 24, 25, 26, 24, 25, 24]
print(ages.count(24))          


# index
fruits = ['banana', 'orange', 'mango', 'lemon']
print(fruits.index('orange'))  

ages = [22, 19, 24, 25, 26, 24, 25, 24]
print(ages.index(24))


# Reverse
fruits = ['banana', 'orange', 'mango', 'lemon']
fruits.reverse()
print(fruits)

ages = [22, 19, 24, 25, 26, 24, 25, 24]
ages.reverse()
print(ages)


# sort
fruits = ['banana', 'orange', 'mango', 'lemon']
fruits.sort()
print(fruits)

fruits.sort(reverse=True)
print(fruits)

ages = [22, 19, 24, 25, 26, 24, 25, 24]
ages.sort()
print(ages)

ages.sort(reverse=True)
print(ages)


# change tuples to lists and lists to tuples
fruits = ('banana', 'orange', 'mango', 'lemon')
fruits = list(fruits)
fruits[0] = 'apple'
print(fruits) 

fruits = tuple(fruits)
print(fruits)     

fruits = ('banana', 'orange', 'mango', 'lemon')
print('orange' in fruits) 
print('apple' in fruits)


fruits = ('banana', 'orange', 'mango', 'lemon')
vegetables = ('Tomato', 'Potato', 'Cabbage','Onion', 'Carrot')
fruits_and_vegetables = fruits + vegetables
print(fruits_and_vegetables)

# convert a list into a string
names = ["root", "auto", "admin"]
dnames = " ".join(names)
print(dnames)

# deletes the entire tuple since it is not possible to remove a single item in a tuple
del fruits


# unpacking lists or tuples
def sum_of_five_nums(a, b, c, d, e):
    return a + b + c + d + e
lst = [1, 2, 3, 4, 5]
print(sum_of_five_nums(*lst))  

countries = ['Finland', 'Sweden', 'Norway', 'Denmark', 'Iceland']
fin, sw, nor, *rest = countries
print(fin, sw, nor, rest)  

numbers = [1, 2, 3, 4, 5, 6, 7]
one, *middle, last = numbers
print(one, middle, last)     


# packing lists
def sum_all(*args):
    s = 0
    for i in args:
        s += i
    return s
print(sum_all(1, 2, 3))             
print(sum_all(1, 2, 3, 4, 5, 6, 7)) 