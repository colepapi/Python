file=open("main.py", "r")
print(file.read())

for i in range(10):
    print(file.readline())

'''file=open("main.py", "w")
print(file.write(""))'''

file.close()