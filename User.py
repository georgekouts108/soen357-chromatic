from Genre import Genre


class User:

    # initially, users have no friends and are not logged in once they create an account
    def __init__(self, id, name, age, location, favGenres, username, password, isLoggedOn):
        self.id = id
        self.name = name
        self.age = age
        self.location = location
        self.favGenres = favGenres
        self.username = username
        self.password = password
        self.loggedOn = isLoggedOn

        # later, implement friends and chats

    def addGenre(self, newGenre):
        if (self.favGenres is None):
            self.favGenres = [newGenre]
        else:
            alreadyExists = False
            for g in self.favGenres:
                if (self.favGenres[g] is newGenre):
                    alreadyExists = True
                    break
            if not alreadyExists:
                self.favGenres.append(newGenre)

    def deleteGenre(self, delGenre):
        try:
            if (self.favGenres is None):
                raise Exception()
            else:
                poppedIndex = 0
                for g in self.favGenres:
                    if (self.favGenres[g] is delGenre):
                        self.favGenres.pop(poppedIndex)
                        break
                    else:
                        poppedIndex = poppedIndex + 1

        except Exception:
            print("No genres to delete")
