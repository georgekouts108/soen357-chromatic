

class User:

    # initially, users have no friends and are not logged in once they create an account
    def __init__(self, id, name, age, location, favGenres):
        self.id = id
        self.name = name
        self.age = age
        self.location = location
        self.favGenres = favGenres

    def printName(self):
        print("hello, my name is " + self.name)
