import re

txt = 'I love to teach python and javaScript'
# It returns an object with span, and match
match = re.match('I love to teach', txt, re.I)
print(match) 

# We can get the starting and ending position of the match as tuple using span
span = match.span()
print(span)     

# Lets find the start and stop position from the span
start, end = span
print(start, end)  
substring = txt[start:end]
print(substring)    


txt = '''Python is the most beautiful language that a human being has ever created.
I recommend python for a first programming language'''

# It returns an object with span and match
match = re.search('first', txt, re.I)
print(match)  
# We can get the starting and ending position of the match as tuple using span
span = match.span()
print(span)     
# Lets find the start and stop position from the span
start, end = span
print(start, end)  
substring = txt[start:end]
print(substring)       

print('\n')

# findall()
txt = '''Python is the most beautiful language that a human being has ever created.
I recommend python for a first programming language'''
matches = re.findall('language', txt, re.I)
matches2 = re.findall('python', txt, re.I)
print(matches)
print(matches2)

print('\n')

# replace a substring
match_replaced = re.sub('[Pp]ython', 'JavaScript', txt, re.I)
print(match_replaced)  

print('\n')

txt = '''%I a%m te%%a%%che%r% a%n%d %% I l%o%ve te%ach%ing.
T%he%re i%s n%o%th%ing as r%ewarding a%s e%duc%at%i%ng a%n%d e%m%p%ow%er%ing p%e%o%ple.
I fo%und te%a%ching m%ore i%n%t%er%%es%ting t%h%an any other %jobs.
D%o%es thi%s m%ot%iv%a%te %y%o%u to b%e a t%e%a%cher?'''

matches = re.sub('%', '', txt)
print(matches)

print('\n')


# splitting text using RegEx split
txt = '''I am teacher and  I love teaching.
There is nothing as rewarding as educating and empowering people.
I found teaching more interesting than any other jobs.
Does this motivate you to be a teacher?'''
print(re.split('\n', txt))

print('\n')

# writing RegEx patterns
regex_pattern = r'apple'
txt = 'Apple and banana are fruits. An old cliche says an apple a day a doctor way has been replaced by a banana a day keeps the doctor far far away. '
matches = re.findall(regex_pattern, txt, re.I)
print(matches)

regex_pattern = r'\d+' 
txt = 'This regular expression example was made on December 6,  2019 and revised on July 8, 2021'
matches = re.findall(regex_pattern, txt)
print(matches) 

txt = 'This regular expression example was made on December 6,  2019 and revised on July 8, 2021'
regex_pattern = r'\d{1,4}'
matches = re.findall(regex_pattern, txt)
print(matches) 

txt = 'This regular expression example was made on December 6,  2019 and revised on July 8, 2021'
regex_pattern = r'^This' 
matches = re.findall(regex_pattern, txt)
print(matches)