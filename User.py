from Genre import Genre
from csv import reader, writer
import csv
import os


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

    def editFavGenresData(self):
        return -1

    def writeGeneralInfoData(self):
        return -1

    def writeFavGenresData(self):
        return -1

    def writeCredentialsData(self):
        username_found = False
        with open("databases/userCredentials.csv", 'r') as csvr:
            csv_reader = reader(csvr)
            credential_rows = list(csv_reader)
            if len(credential_rows) == 0:
                username_found = False
            else:
                count = 0
                for row in credential_rows:
                    if (count is not 0):
                        if (row[1] == self.username):
                            username_found = True
                            break
                    count = count + 1
        if not username_found:
            with open("databases/userCredentials.csv", 'a') as user_records:
                csv_writer = writer(user_records)
                csv_writer.writerow([self.id, self.username, self.password])
        return True

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
