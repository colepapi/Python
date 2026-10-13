# python constructor

class Person:
      def __init__(self, firstname, lastname, age, country, city):
          self.firstname = firstname
          self.lastname = lastname
          self.age = age
          self.country = country
          self.city = city


p = Person('Kawhi', 'Leonard', 25, 'Canada', 'Toronto')
print(f"{p.firstname} {p.lastname} {p.age} {p.country} {p.city}")


# object methods
class Person:
      def __init__(self, firstname, lastname, age, country, city):
          self.firstname = firstname
          self.lastname = lastname
          self.age = age
          self.country = country
          self.city = city
      def person_info(self):
        print(f'{self.firstname} {self.lastname} is {self.age} years old. He lives in {self.city}, {self.country}')

p = Person('Kawhi', 'Leonard', 25, 'Finland', 'Helsinki')
p.person_info()

# object default methods
class Person:
      def __init__(self, firstname='Kawhi', lastname='Leonard', age=25, country='Finland', city='Helsinki'):
          self.firstname = firstname
          self.lastname = lastname
          self.age = age
          self.country = country
          self.city = city

      def person_info(self):
        return f'{self.firstname} {self.lastname} is {self.age} years old. He lives in {self.city}, {self.country}.'

p1 = Person()
print(p1.person_info())
p2 = Person('Dennis', 'Schroder', 30, 'Nomanland', 'Noman city')
print(p2.person_info())


# method to modify class default values
class Person:
      def __init__(self, firstname='Kawhi', lastname='Leonard', age=25, country='Finland', city='Helsinki'):
          self.firstname = firstname
          self.lastname = lastname
          self.age = age
          self.country = country
          self.city = city
          self.skills = []

      def person_info(self):
        print(f'{self.firstname} {self.lastname} is {self.age} years old. He lives in {self.city}, {self.country}.')

      def add_skill(self, skill):
          self.skills.append(skill)

p1 = Person()
p1.person_info()

p1.add_skill('HTML')
p1.add_skill('CSS')
p1.add_skill('JavaScript')

print(p1.skills)

p2 = Person('Dennis', 'Schroder', 30, 'Nomanland', 'Noman city')

p2.person_info()


# Inheritance
class Student(Person):
    pass


s1 = Student('Ibanez', 'Garcia', 30, 'Finland', 'Helsinki')
s2 = Student('Henry', 'Teklemariam', 28, 'Finland', 'Espoo')
print(s1.person_info())
s1.add_skill('JavaScript')
s1.add_skill('React')
s1.add_skill('Python')
print(s1.skills)

print(s2.person_info())
s2.add_skill('Organizing')
s2.add_skill('Marketing')
s2.add_skill('Digital Marketing')
print(s2.skills)

print('\n')

# override parent method
class Student(Person):
    def __init__ (self, firstname='Kawhi', lastname='Leonard',age=25, country='Finland', city='Helsinki', gender='male'):
        self.gender = gender
        super().__init__(firstname, lastname,age, country, city)
    def person_info(self):
        gender = 'He' if self.gender =='male' else 'She'
        return f'{self.firstname} {self.lastname} is {self.age} years old. {gender} lives in {self.city}, {self.country}.'

s1 = Student('Dennis', 'Schroder', 30, 'Finland', 'Helsinki','male')
s2 = Student('Stephanie', 'Thompson', 28, 'Finland', 'Espoo', 'female')
print(s1.person_info())
s1.add_skill('JavaScript')
s1.add_skill('React')
s1.add_skill('Python')
print(s1.skills)

print(s2.person_info())
s2.add_skill('Organizing')
s2.add_skill('Marketing')
s2.add_skill('Digital Marketing')
print(s2.skills)


# Object Oriented Programming

# Encapsulation
class Waiter:
    def __init__(self):
        self.tables = []

    def add_table(self, table_no):
        self.tables.append(table_no)

Kassandra = Waiter()
Peter = Waiter()

Kassandra.tables.add_table(3)
Peter.tables.add_table(4)

print(Kassandra.tables)
print(Peter.tables)


# Inheritance - represents a relationship (is a relationship)
class staff:
    def __init__(self, name, shift):
        self.name = name
        self.shift = shift

    def start_work(self):
        print(f"I think {self.name} starts work on {self.shift} shift")

class waiter(staff):
    def take_order(self):
        print(f"{self.name} alternates with another waiter for the {self.shift} shift")

class chef(staff):
    def cook_food(self):
        print(f"{self.name} prepares meals for the customers while waiting for another chef to come during the {self.shift} shift")

class cleaner(staff):
    def clean_floors(self):
        print(f"{self.name} cleans the restaurant before the {self.shift} shift")

Naomi = waiter("Naomi", "night")
Erick = chef("Erick", "night")
Kanani = cleaner("Kanani", "day")

Erick.start_work()

Naomi.take_order()
Erick.cook_food()
Kanani.clean_floors()


# Polymorphism - same instruction many forms of behaviour
class restaurant:
    def __init__(self, staff, clients):
        self.staff = staff
        self.clients = clients

    def responsibility(self):
        print(f"The {self.staff} needs to give {self.clients} a good experience at the restaurant")

class managers(restaurant):
    def assign_role(self):
        print(f"The {self.staff} need to ensure everyone is comfortably performing their roles and that the {self.clients} give positive feedback")

    def responsibility(self):
        self.assign_role()

class chefs(restaurant):
    def cook_food(self):
        print(f"The {self.staff} prepares food for {self.clients}")

    def responsibility(self):
        self.cook_food()

class waiters(restaurant):
    def serve_food(self):
        print(f"The {self.staff} serves food to the {self.clients}")
    
    def responsibility(self):
        self.serve_food()

manager = managers("manager", "customers")
chef = chefs("chef", "customers")
waiter = waiters("waiter", "customers")

manager.responsibility()
chef.responsibility()
waiter.responsibility()


# Abstraction - setting rules before allowing someone to be a part of the system
from abc import ABC, abstractmethod

class staff(ABC):
    def __init__(self, name, shift):
        self.name = name
        self.shift = shift

    def start_work(self):
        print(f"I think {self.name} starts work on {self.shift} shift")
    
    @abstractmethod
    def experience(self):
        pass

class waiter(staff):
    def take_order(self):
        print(f"{self.name} takes order from the customers. He works on the {self.shift} shift")

    def experience(self):
        print(f"{self.name} has 3 years of hospitality experience")

Liam = waiter("Liam", "day")

Liam.start_work()
Liam.experience()


# Composition - an object has a relationship with another object
class chef:
    def cook_food(self, dish):
        print(f"The chef prepares the customer's food based on their order which is {dish}")

class waiter:
    def __init__(self, name, chef):
        self.name = name
        self.chef = chef

    def take_order(self, dish):
        print(f"{self.name} takes the order which is {dish} from the customer then relays it to the chef who prepares it")
    
    def serve_food(self, dish):
        print(f"Once the food is ready the chef informs {self.name} to serve the {dish} to the hungry customer")

Ombachi = chef()
waiters = waiter("Anne", Ombachi)

Ombachi.cook_food("Ugali and Fish")
waiters.take_order("Ugali and Fish")
waiters.serve_food("Ugali and Fish")