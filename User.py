from Genre import Genre
from csv import reader, writer
from csvEditing import updatePassword, updateGenres
import csv
import os
from datetime import datetime
NUM_OF_ACTIVE_USERS = 0
NEXT_USER_ID = 1


def getUserCount():
    return NUM_OF_ACTIVE_USERS


def getNextUserID():
    return NEXT_USER_ID


def setLatestNumberOfUsersAndIDs():
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
    def __init__(self, firstname, lastname, email, birthMonth, birthDay, birthYear, location, favGenres, username, password, manualUserID, newUserID=True, loggedOn=False):

        # all parameters are assumed to be valid

        self.firstname = firstname
        self.lastname = lastname
        self.fullname = self.firstname + " " + self.lastname
        self.email = email
        self.birthmonth = birthMonth
        self.birthday = birthDay
        self.birthyear = birthYear
        self.age = self.getCurrentAge()
        self.location = location
        self.favGenres = favGenres
        self.username = username
        self.password = password
        self.loggedOn = loggedOn

        # later, implement friends and chats

        if(newUserID is True):  # is a new user coming in?
            self.id = getNextUserID()
            updateNextUserID()
            self.writeGeneralInfoData()
            self.writeFavGenresData()

            updateNumOfActiveUsers()
            setLatestNumberOfUsersAndIDs()

        else:  # or is an existing user coming in?
            self.id = manualUserID

    def updateGenreList(self):
        # this method assumes that self.favGenres has been updated
        updateGenres(self.id, self.favGenres)

    def changePassword(self, newPassword):
        self.password = newPassword
        updatePassword(self.id, newPassword)

    def writeGeneralInfoData(self):
        with open(r"databases/userGeneralInfo.csv", 'a') as user_records:
            csv_writer = writer(user_records)
            newRow = [self.id, self.firstname, self.lastname, self.email, self.birthmonth, self.birthday,
                      self.birthyear, self.age, self.location, self.loggedOn, self.username, self.password]
            csv_writer.writerow(newRow)
        return True

    def writeFavGenresData(self):
        with open(r"databases/userFavGenres.csv", 'a') as user_records:
            csv_writer = writer(user_records)

            if (self.favGenres is not None):
                genres = [self.id]
                for genre in self.favGenres:
                    genres.append(genre)
                csv_writer.writerow(genres)
            else:
                csv_writer.writerow([self.id, ''])
        return True

    def addGenre(self, newGenre):
        if (self.favGenres is None):
            self.favGenres = [newGenre]
        else:
            alreadyExists = False
            for g in range(len(self.favGenres)):
                if (self.favGenres[g] == newGenre):
                    alreadyExists = True
                    break
            if not alreadyExists:
                self.favGenres.append(newGenre)
                self.updateGenreList()

        return True

    def deleteGenre(self, delGenre):
        try:
            if (self.favGenres is None):
                raise Exception()
            else:
                poppedIndex = 0
                for g in self.favGenres:
                    if (g == delGenre):
                        self.favGenres.pop(poppedIndex)
                        self.updateGenreList()
                        break
                    else:
                        poppedIndex = poppedIndex + 1

        except Exception:
            print("No genres to delete")

    def getCurrentAge(self):
        presentTime = datetime.now()
        presentDay = presentTime.strftime("%d")
        presentMonth = presentTime.strftime("%m")
        presentYear = presentTime.strftime("%Y")

        if (presentDay[0] == '0'):  # single digit day? 01-09?
            presentDay = presentDay[1]
        if (presentMonth[0] == '0'):  # single digit month? 01-09?
            presentMonth = presentMonth[1]

        birth_day = 0
        birth_month = 0

        if (self.birthday[0] == '0'):  # single digit birth day? 01-09?
            birth_day = int(self.birthday[1])

        if (self.birthmonth[0] == '0'):  # single digit birth month? 01-09?
            birth_month = int(self.birthmonth[1])

        isBirthdayToday = ((birth_month == int(presentMonth))
                           and (birth_day == int(presentDay)))

        if (isBirthdayToday):
            return (int(presentYear) - int(self.birthyear))

        return (int(presentYear) - int(self.birthyear) - 1)
