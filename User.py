from Genre import Genre
from csv import reader, writer
from csvEditing import updatePassword, updateGenres, getGenreDB, getGeneralInfoDB
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
    return NUM_OF_ACTIVE_USERS


def updateNextUserID():
    global NEXT_USER_ID
    NEXT_USER_ID = NEXT_USER_ID + 1


def updateNumOfActiveUsers():
    global NUM_OF_ACTIVE_USERS
    NUM_OF_ACTIVE_USERS = NUM_OF_ACTIVE_USERS + 1


class User:

    # initially, users have no friends and are not logged in once they create an account
    def __init__(self, firstname, lastname, email, birthMonth, birthDay, birthYear, location, favGenres, username, password, manualUserID, newUserID=True, loggedOn=False,
                 friends=None, sentFriendReqs=None, receivedFriendRequests=None):

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

        self.friends = friends
        self.sent_friend_requests = sentFriendReqs
        self.received_friend_requests = receivedFriendRequests

        if(newUserID is True):  # is a new user coming in?
            self.id = getNextUserID()
            updateNextUserID()
            self.writeGeneralInfoData()
            self.writeFavGenresData()
            self.writeFriendsData()
            self.writeSentFriendRequestsData()
            self.writeRecievedFriendRequestsData()

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

    def writeFriendsData(self):
        with open(r"databases/userFriends.csv", 'a') as user_records:
            csv_writer = writer(user_records)

            if (self.friends is not None):
                FRIENDS = [self.id]
                for req in self.friends:
                    FRIENDS.append(req)
                csv_writer.writerow(FRIENDS)
            else:
                csv_writer.writerow([self.id])
        return True

    def writeSentFriendRequestsData(self):
        with open(r"databases/userSentFriendRequests.csv", 'a') as user_records:
            csv_writer = writer(user_records)

            if (self.sent_friend_requests is not None):
                sentRequests = [self.id]
                for req in self.sent_friend_requests:
                    sentRequests.append(req)
                csv_writer.writerow(sentRequests)
            else:
                csv_writer.writerow([self.id])
        return True

    def writeRecievedFriendRequestsData(self):
        with open(r"databases/userReceivedFriendRequests.csv", 'a') as user_records:
            csv_writer = writer(user_records)

            if (self.received_friend_requests is not None):
                receivedRequests = [self.id]
                for req in self.received_friend_requests:
                    receivedRequests.append(req)
                csv_writer.writerow(receivedRequests)
            else:
                csv_writer.writerow([self.id])
        return True

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

    def isGenreInList(self, genre, array):
        yes = False
        for a in array:
            if a == genre:
                yes = True
                break
        return yes

    # this should NOT include existing friends
    def getFriendRecommendations(self):

        oneGenreMatches = []
        twoGenreMatches = []
        threeGenreMatches = []
        fourGenreMatches = []
        fivePlusGenreMatches = []

        for row in getGenreDB()[1::]:
            if ((row[0] != self.id) and (not self.userExistsInFriendsList(row[0]))):
                matchCount = 0
                genresInCommon = []
                theirUsername = getGeneralInfoDB()[int(row[0])][10]
                theirGenres = row[1::]

                # how many genres are matched?
                for myGenre in self.favGenres:
                    if self.isGenreInList(myGenre, theirGenres):
                        matchCount = matchCount + 1
                        genresInCommon.append(myGenre)

                if (matchCount == 1):
                    oneGenreMatches.append([theirUsername, genresInCommon])
                elif (matchCount == 2):
                    twoGenreMatches.append([theirUsername, genresInCommon])
                elif (matchCount == 3):
                    threeGenreMatches.append([theirUsername, genresInCommon])
                elif (matchCount == 4):
                    fourGenreMatches.append([theirUsername, genresInCommon])
                elif (matchCount >= 5):
                    fivePlusGenreMatches.append(
                        [theirUsername, genresInCommon])

        return [oneGenreMatches, twoGenreMatches, threeGenreMatches, fourGenreMatches, fivePlusGenreMatches]

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

    def sendFriendRequest(self, recipient):
        try:
            cond1 = not self.userExistsInFriendsList(recipient)
            cond2 = not self.userExistsInSentRequestsList(recipient)
            cond3 = not self.userExistsInReceivedRequests(recipient)
            if (not (cond1 and cond2 and cond3)):
                raise Exception()

            # when you send a friend request:
            # 1) that person's username gets added to your SENT csv
            # 2) your own username will get added to their RECEIVED csv

            # (1)
            f = open('databases/userSentFriendRequests.csv', 'r')
            csv_reader1 = reader(f)
            sentFriendRequestRows = list(csv_reader1)
            f.close()
            sentFriendRequestRows[int(self.id)].append(recipient)

            newList1 = open('databases/userSentFriendRequests.csv',
                            'w', newline='')
            csv_writer1 = writer(newList1)
            csv_writer1.writerows(sentFriendRequestRows)
            newList1.close()

            # (2)

            h = open('databases/userGeneralInfo.csv', 'r')
            csv_reader3 = reader(h)
            user_rows = list(csv_reader3)
            h.close()

            recipientID = 1
            for row in user_rows[1::]:
                if (str(row[10]) == str(recipient)):
                    recipientID = int(row[0])
                    break

            g = open('databases/userReceivedFriendRequests.csv', 'r')
            csv_reader2 = reader(g)
            receivedFriendRequestRows = list(csv_reader2)
            g.close()
            receivedFriendRequestRows[recipientID].append(self.username)

            newList2 = open(
                'databases/userReceivedFriendRequests.csv', 'w', newline='')
            csv_writer2 = writer(newList2)
            csv_writer2.writerows(receivedFriendRequestRows)
            newList2.close()

        except Exception:
            return

    def cancelFriendRequest(self, recipient):

        try:
            cond1 = not self.userExistsInFriendsList(recipient)
            cond2 = self.userExistsInSentRequestsList(recipient)
            if (not (cond1 and cond2)):
                raise Exception()

            # when you cancel a friend request:
            # 1) that person's username gets removed from your SENT csv
            # 2) your own username will get removed from their RECEIVED csv

            # (1)
            f = open('databases/userSentFriendRequests.csv', 'r')
            csv_reader1 = reader(f)
            sendFriendRequestRows = list(csv_reader1)
            f.close()

            poppedIndex = 1
            for requested_uname in sendFriendRequestRows[int(self.id)][1::]:
                if (requested_uname == recipient):
                    sendFriendRequestRows[int(self.id)].pop(poppedIndex)
                    break
                else:
                    poppedIndex = poppedIndex + 1

            newList1 = open('databases/userSentFriendRequests.csv',
                            'w', newline='')
            csv_writer1 = writer(newList1)
            csv_writer1.writerows(sendFriendRequestRows)
            newList1.close()

            h = open('databases/userGeneralInfo.csv', 'r')
            csv_reader3 = reader(h)
            user_rows = list(csv_reader3)
            h.close()

            # (2)
            recipientID = 0
            for row in user_rows[1::]:
                if (row[10] == recipient):
                    recipientID = int(row[0])
                    break

            g = open('databases/userReceivedFriendRequests.csv', 'r')
            csv_reader2 = reader(g)
            receivedFriendRequestRows = list(csv_reader2)
            g.close()

            poppedIndex = 1
            for requested_uname in receivedFriendRequestRows[recipientID][1::]:
                if (requested_uname == self.username):
                    receivedFriendRequestRows[recipientID].pop(poppedIndex)
                    break
                else:
                    poppedIndex = poppedIndex + 1

            newList2 = open(
                'databases/userReceivedFriendRequests.csv', 'w', newline='')
            csv_writer2 = writer(newList2)
            csv_writer2.writerows(receivedFriendRequestRows)
            newList2.close()

        except Exception:
            return

    def acceptFriendRequest(self, acceptee):

        try:
            cond1 = not self.userExistsInFriendsList(acceptee)
            cond2 = not self.userExistsInSentRequestsList(acceptee)
            cond3 = self.userExistsInReceivedRequests(acceptee)
            if (not (cond1 and cond2 and cond3)):
                raise Exception()

            # when you accept a friend request:
            # 1) the acceptee's username will be appended to your own list of friends
            # 2) your own username will be appended to the acceptee's list of friends
            # 3) your own username gets removed from the acceptee's SENT list
            # 4) the acceptee's username gets removed from the accepter's RECEIVED list

            # (1)
            g = open('databases/userFriends.csv', 'r')
            csv_reader2 = reader(g)
            friendsLists = list(csv_reader2)
            g.close()

            friendsLists[int(self.id)].append(acceptee)

            # (2)
            h = open('databases/userGeneralInfo.csv', 'r')
            csv_reader3 = reader(h)
            user_rows = list(csv_reader3)
            h.close()

            accepteeID = 0
            for row in user_rows[1::]:
                if (row[10] == acceptee):
                    accepteeID = int(row[0])
                    break

            friendsLists[accepteeID].append(self.username)

            newList2 = open(
                'databases/userFriends.csv', 'w', newline='')
            csv_writer2 = writer(newList2)
            csv_writer2.writerows(friendsLists)
            newList2.close()

            # (3)
            f = open('databases/userSentFriendRequests.csv', 'r')
            csv_reader1 = reader(f)
            sendFriendRequestRows = list(csv_reader1)
            f.close()

            poppedIndex = 1
            for accepted_uname in sendFriendRequestRows[int(accepteeID)][1::]:
                if (accepted_uname == self.username):
                    sendFriendRequestRows[int(accepteeID)].pop(poppedIndex)
                    break
                else:
                    poppedIndex = poppedIndex + 1

            newList1 = open('databases/userSentFriendRequests.csv',
                            'w', newline='')
            csv_writer1 = writer(newList1)
            csv_writer1.writerows(sendFriendRequestRows)
            newList1.close()

            # (4)
            g = open('databases/userReceivedFriendRequests.csv', 'r')
            csv_reader3 = reader(g)
            receivedFriendRequestRows = list(csv_reader3)
            g.close()

            poppedIndex = 1
            for acceptee_uname in receivedFriendRequestRows[int(self.id)][1::]:
                if (acceptee_uname == acceptee):
                    receivedFriendRequestRows[int(self.id)].pop(poppedIndex)
                    break
                else:
                    poppedIndex = poppedIndex + 1

            newList3 = open(
                'databases/userReceivedFriendRequests.csv', 'w', newline='')
            csv_writer3 = writer(newList3)
            csv_writer3.writerows(receivedFriendRequestRows)
            newList3.close()

            self.friends.append(acceptee)
        except Exception:
            return

    def unfriendUser(self, unfriendee):

        try:
            if not self.userExistsInFriendsList(unfriendee):
                raise Exception()

            g = open('databases/userFriends.csv', 'r')
            csv_reader = reader(g)
            friendsLists = list(csv_reader)
            g.close()

            h = open('databases/userGeneralInfo.csv', 'r')
            csv_reader3 = reader(h)
            user_rows = list(csv_reader3)
            h.close()

            unfriendeeID = 1
            for row in user_rows[1::]:
                if (row[10] == unfriendee):
                    unfriendeeID = int(row[0])
                    break

            poppedIndex = 1
            for uname in friendsLists[unfriendeeID][1::]:
                if (uname == self.username):
                    friendsLists[unfriendeeID].pop(poppedIndex)
                    break
                else:
                    poppedIndex = poppedIndex + 1

            poppedIndex2 = 1
            for uname in friendsLists[int(self.id)][1::]:
                if (uname == unfriendee):
                    friendsLists[int(self.id)].pop(poppedIndex2)
                    break
                else:
                    poppedIndex2 = poppedIndex2 + 1

            newList2 = open(
                'databases/userFriends.csv', 'w', newline='')
            csv_writer2 = writer(newList2)
            csv_writer2.writerows(friendsLists)
            newList2.close()

        except Exception:
            return

    # friendship precondition methods

    def userExistsInFriendsList(self, targetUser):
        exists = False
        g = open('databases/userFriends.csv', 'r')
        csv_reader2 = reader(g)
        friendsLists = list(csv_reader2)
        g.close()
        for user in friendsLists[int(self.id)]:
            if (user == targetUser):
                exists = True
                break
        return exists

    def userExistsInSentRequestsList(self, targetUser):
        exists = False
        g = open('databases/userSentFriendRequests.csv', 'r')
        csv_reader2 = reader(g)
        sentRequestsList = list(csv_reader2)
        g.close()
        for user in sentRequestsList[int(self.id)]:
            if (user == targetUser):
                exists = True
                break
        return exists

    def userExistsInReceivedRequests(self, targetUser):
        exists = False
        g = open('databases/userReceivedFriendRequests.csv', 'r')
        csv_reader2 = reader(g)
        receivedRequestsList = list(csv_reader2)
        g.close()
        for user in receivedRequestsList[int(self.id)]:
            if (user == targetUser):
                exists = True
                break
        return exists
