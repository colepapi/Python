#while loop
count = 0
while count < 5:
    print(count)
    count += 1


# break and continue
count = 0
while count < 5:
    print(count)
    count += 1
    if count == 3:
        break


count = 0
while count < 5:
    if count == 3:
        count += 1
        continue
    print(count)
    count += 1


numbers = (0,1,2,3,4,5)
for number in numbers:
    print(number)
    if number == 3:
        break


numbers = (0,1,2,3,4,5)
for number in numbers:
    print(number)
    if number == 3:
        continue
    print('Next number should be ', number + 1) if number != 5 else print("loop's end")


# for loop
numbers = [0, 1, 2, 3, 4, 5]
for number in numbers: 
    print(number)       # string

numbers = (0, 1, 2, 3, 4, 5)
for number in numbers: 
    print(number)          # tuple

it_companies = {'Facebook', 'Google', 'Microsoft', 'Apple', 'IBM', 'Oracle', 'Amazon'}
for company in it_companies:
    print(company)              # set

language = 'Python'
for letter in language:
    print(letter)

for i in range(len(language)):
    print(language[i])


# for loop with a dictionary
person = {
    'first_name':'Kawhi',
    'last_name':'Leonard',
    'age':25,
    'country':'Finland',
    'is_marred':True,
    'skills':['JavaScript', 'React', 'Node', 'MongoDB', 'Python'],
    'address':{
        'street':'Space street',
        'zipcode':'02210'
    }
}
for key in person:
    print(key)
print('\n')

for key, value in person.items():
    print(key, value) 
print('\n')

# nested for loop
for key in person:
    if key == 'skills':
        for skill in person['skills']:
            print(skill)

# range
lst = list(range(51))
print(lst) 

st = set(range(30, 51))  
print(st) 

lst = list(range(0,51,5))
print(lst) 

st = set(range(0,51,2))
print(st) 

lst = list(range(50,-5,-5))
print(lst) 


for number in range(11):
    print(number)   

# for else
for number in range(11):
    print(number)   
else:
    print('The loop stops at', number)


for number in range(6):
    pass