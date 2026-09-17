person = {
    'first_name':'Damian',
    'last_name':'Lillard',
    'age':25,
    'country':'Finland',
    'is_marred':True,
    'skills':['JavaScript', 'React', 'Node', 'MongoDB', 'Python'],
    'address':{
        'street':'Space street',
        'zipcode':'02210'
    }
    }


# accessing an item in a dictionary
print(person.get('first_name')) 
print(person.get('country'))  
print(person.get('skills')) 
print(person['skills'][0]) 
print(person['address']['street'])


# also use get() function
print(person.get('first_name')) 
print(person.get('country'))    
print(person.get('skills')) 
print(person.get('city'))


# add items into a dictionary
person['job_title'] = 'Instructor'
person['skills'].append('HTML')
print(person)


# modify items in a dictionary
person = {
    'first_name':'Damian',
    'last_name':'Lillard',
    'age':25,
    'country':'Finland',
    'is_marred':True,
    'skills':['JavaScript', 'React', 'Node', 'MongoDB', 'Python'],
    'address':{
        'street':'Space street',
        'zipcode':'02210'
    }
    }
person['first_name'] = 'Kyrie'
person['age'] = 22
print(person)
print('address' in person) # key exists in the dictionary


# removing key and value pairs in a dictionary
person.pop('last_name')        
person.popitem()                
del person['is_marred'] 
print(person)


# dictionary to a list of tuples
dct = {'key1':'value1', 'key2':'value2', 'key3':'value3', 'key4':'value4'}
print(dct.items()) 
print(dct.copy()) # copy a dictionary
print(dct.keys()) # gets keys as a list
print(dct.values()) # gets dictionary values as a list
print(dct.clear())
del dct


# unpacking dictionaries
def unpacking_person_info(name, country, city, age):
    return f'{name} lives in {city}, {country}. He is {age} years old.'
dct = {'name':'Kawhi', 'country':'Finland', 'city':'Helsinki', 'age':25}
print(unpacking_person_info(**dct))


# packing dictionaries
def packing_person_info(**kwargs):
    for key in kwargs:
        print(f"{key} = {kwargs[key]}")
    return kwargs
print(packing_person_info(name="Kawhi", country="Finland", city="Helsinki", age=25))


