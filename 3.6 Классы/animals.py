class Animal:
    breathing = True
    pulse = True

    def eat(self):
        print('Eating')

    def sleep(self):
        print('Sleeping')

    def drink(self):
        print('Drinking')


class Artiodactyl(Animal):
    hooves = 4

    def run(self):
        print('Running')


class Bird(Animal):
    wings = 2
    beak = True

    def fly(self):
        print('Flying')

    def tear_down_an_egg(self):
        print('Egg')


class Duck(Bird):
    color = 'grey'


class Chicken(Bird):
    color = 'black'


class Goose(Bird):
    color = 'white'


class Cow(Artiodactyl):
    horns = 2

    def milk(self):
        print('Milk')


class Goat(Artiodactyl):
    horns = 2

    def butt(self):
        print('Butting')


class Sheep(Artiodactyl):
    horns = 2

    def shear(self):
        print('Wool')


class Pig(Artiodactyl):

    def dig(self):
        print('Digging')