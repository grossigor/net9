class Animal:

    def __init__(self):
        self.breathing = True
        self.pulse = True

    def eat(self):
        print('Eating')

    def sleep(self):
        print('Sleeping')

    def drink(self):
        print('Drinking')


class Artiodactyl(Animal):

    def __init__(self):
        self.hooves = 4

    def run(self):
        print('Running')


class Bird(Animal):

    def __init__(self):
        self.wings = 2
        self.beak = True

    def fly(self):
        print('Flying')

    def tear_down_an_egg(self):
        print('Egg')


class Duck(Bird):

    def __init__(self):
        self.color = 'grey'


class Chicken(Bird):

    def __init__(self):
        self.color = 'black'


class Goose(Bird):

    def __init__(self):
        self.color = 'white'


class Cow(Artiodactyl):

    def __init__(self):
        self.horns = 2

    def milk(self):
        print('Milk')


class Goat(Artiodactyl):

    def __init__(self):
        self.horns = 2

    def butt(self):
        print('Butting')


class Sheep(Artiodactyl):

    def __init__(self):
        self.horns = 2

    def shear(self):
        print('Wool')


class Pig(Artiodactyl):

    def dig(self):
        print('Digging')


animal = Animal()
artiodactyl = Artiodactyl()
bird = Bird()
duck = Duck()
chicken = Chicken()
goose = Goose()
cow = Cow()
goat = Goat()
sheep = Sheep()
pig = Pig()

pig.drink()
goose.fly()
print(cow.horns)