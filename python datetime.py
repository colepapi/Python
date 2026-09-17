# get datetime information
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
import time

now = datetime.now()                   
day = now.day                   
month = now.month               
year = now.year                 
hour = now.hour                 
minute = now.minute            
second = now.second
timestamp = now.timestamp()
print(day, month, year, hour, minute)
print('timestamp', timestamp)
print(f'{day}/{month}/{year}, {hour}:{minute}') 

# strftime
now = datetime.now()
t = now.strftime("%H:%M:%S")
print("time:", t)          

time_two = now.strftime("%d/%m/%Y, %H:%M:%S")
print("time two:", time_two)        

# strptime
date_string = "16 September, 2026"
date_object = datetime.strptime(date_string, "%d %B, %Y")
print("date_object: ", date_object)  

# using date from datetime
d = date(2026, 8, 26)
print(d)        
print('Current date: ', d.today())   

today = date.today()
print("Current year: ", today.year)   
print("Current month: ", today.month) 
print("Current day: ", today.day)   

# time objects to represent time
a = time()
print("a: ", a)
b = time(13, 35, 40)
print("b: ", b)

today = date(year=2026, month=8, day=26)
new_year = date(year=2027, month=1, day=1)
time_left_for_newyear = new_year - today
print('Time left for new year: ', time_left_for_newyear) 

t1 = datetime(year = 2026, month = 9, day = 16, hour = 17, minute = 15, second = 40)
t2 = datetime(year = 2027, month = 1, day = 1, hour = 0, minute = 0, second = 0)
diff = t2 - t1
print('Time left for new year:', diff) 


i=10
while i >= 1:
    print(i)
    i-=1
    time.sleep(1)