from Genre import Genre
from csv import reader, writer
from csvEditing import updatePassword
import csv
import os


NUM_OF_ACTIVE_USERS = 0
NEXT_USER_ID = 1


def setLatestNumberOfUsers():
    file = open('databases/userGeneralInfo.csv', 'r')
    csv_reader = reader(file)
    credential_rows = list(csv_reader)
    file.close()

    global NUM_OF_ACTIVE_USERS
    NUM_OF_ACTIVE_USERS = len(credential_rows) - 1

    global NEXT_USER_ID
    NEXT_USER_ID = len(credential_rows)


def updateNextUserID():
    global NEXT_USER_ID
    NEXT_USER_ID = NEXT_USER_ID + 1


def updateNumOfActiveUsers():
    global NUM_OF_ACTIVE_USERS
    NUM_OF_ACTIVE_USERS = NUM_OF_ACTIVE_USERS + 1


class User:

    # initially, users have no friends and are not logged in once they create an account
    def __init__(self, firstname, lastname, age, location, favGenres, username, password, isLoggedOn):

        self.id = NEXT_USER_ID
        updateNextUserID()

        self.firstname = firstname
        self.lastname = lastname
        self.fullname = self.firstname + " " + self.lastname
        self.age = age
        self.location = location
        self.favGenres = favGenres
        self.username = username
        self.password = password
        self.loggedOn = isLoggedOn

        # later, implement friends and chats
        updateNumOfActiveUsers()

    # READING FROM CSVs

    # EDITING CSVs
    # def changePassword(self, newPassword):

    #     updatePassword(self.id, newPassword)

    # WRITING TO CSVs

    def writeGeneralInfoData(self):
        with open(r"databases/userGeneralInfo.csv", 'a') as user_records:
            csv_writer = writer(user_records)
            newRow = [self.id, self.firstname, self.lastname, self.age,
                      self.location, self.loggedOn]
            csv_writer.writerow(newRow)
        return True

    def writeFavGenresData(self):
        with open(r"databases/userFavGenres.csv", 'a') as user_records:
            csv_writer = writer(user_records)
            try:
                if (self.favGenres is not None):
                    csv_writer.writerow(
                        [self.id, ','.join(str(genre) for genre in self.favGenres)])
                else:
                    raise Exception()
            except Exception:
                print("no genres")
        return True

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
            with open(r"databases/userCredentials.csv", 'a') as user_records:
                csv_writer = writer(user_records)
                csv_writer.writerow([self.id, self.username, self.password])
        return True

    def addGenre(self, newGenre):
        if (self.favGenres is None):
            self.favGenres = [newGenre]
        else:
            alreadyExists = False
            for g in range(len(self.favGenres)):
                if (self.favGenres[g] is newGenre):
                    alreadyExists = True
                    break
            if not alreadyExists:
                self.favGenres.append(newGenre)
        # TODO: update the CSV file for this user
        return True

    def deleteGenre(self, delGenre):
        try:
            if (self.favGenres is None):
                raise Exception()
            else:
                poppedIndex = 0
                for g in self.favGenres:
                    if (self.favGenres[g] is delGenre):
                        self.favGenres.pop(poppedIndex)
                        # TODO: update the CSV file for this user
                        break
                    else:
                        poppedIndex = poppedIndex + 1
                # TODO: update the CSV file for this user
        except Exception:
            print("No genres to delete")
