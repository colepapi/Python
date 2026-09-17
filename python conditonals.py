a = 3
if a < 0:
    print('A is a negative number')
else:
    print('A is a positive number')


a = 0
if a > 0:
    print('A is a positive number')
elif a < 0:
    print('A is a negative number')
else:
    print('A is zero')


# logical operators
a = 0
if a > 0 and a % 2 == 0:
        print('A is an even and positive integer')
elif a > 0 and a % 2 !=  0:
     print('A is a positive integer')
elif a == 0:
    print('A is zero')
else:
    print('A is negative')
    

user = 'Odell'
access_level = 3
if user == 'admin' or access_level >= 5:
        print('Access granted!')
else:
    print('Access denied!')