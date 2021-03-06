from random import randint
from Genre import Genre
from csv import reader, writer
from csvEditing import updatePassword, updateGenres, getGenreDB, getGeneralInfoDB, updateAge
import csv
import os
from datetime import datetime, date
import math
from messaging import getInfoForFriends, getYourUsername, updateUnreadMessageCountForSpecificChat, updateTotalUnreadMessageCount
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
    def __init__(self, firstname, lastname, email, birthMonth, birthDay, birthYear, location, favGenres, username, password, gender, pronoun, manualUserID, newUserID=True, loggedOn=False,
                 friends=None, sentFriendReqs=None, receivedFriendRequests=None):

        # all parameters are assumed to be valid

        self.firstname = firstname
        self.lastname = lastname
        self.fullname = self.firstname + " " + self.lastname
        self.email = str(email)
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

        self.gender = gender
        self.pronoun = pronoun

        if(newUserID is True):  # is a new user coming in?
            self.id = getNextUserID()
            updateNextUserID()
            self.writeGeneralInfoData()
            self.writeFavGenresData()
            self.writeFriendsData()
            self.writeSentFriendRequestsData()
            self.writeRecievedFriendRequestsData()
            self.joinUnreadMessagesRecords()
            updateNumOfActiveUsers()
            setLatestNumberOfUsersAndIDs()

        else:  # or is an existing user coming in?
            self.id = manualUserID
        self.updateUserAge()

    def getNumberOfIncomingReqs(self):
        count = 0
        rec_friend_reqs = open('databases/userReceivedFriendRequests.csv', 'r')
        friendships_csv_reader3 = reader(rec_friend_reqs)
        recReqs_info_rows = list(friendships_csv_reader3)
        rec_friend_reqs.close()

        for r in recReqs_info_rows[1::]:
            if r[0] == str(self.id):
                count = len(r[1::])
                break
        return count

    def updateAllUnreadMessages(self):
        total_unread_msgs_count = 0
        listOfChatFiles = os.listdir("chats/")

        for filename in listOfChatFiles:
            indiv_unread_msgs_count = 0
            my_id_found = False
            for u_id in filename.split('_')[1:(len(filename.split('_')))]:
                if u_id == self.id:
                    my_id_found = True
                    break
            if not my_id_found:
                continue

            CSVFile = open('chats/'+filename, 'r')
            csv_reader = reader(CSVFile)
            chat_log = list(csv_reader)
            for msg in chat_log[1::]:
                i_saw_it = False
                for viewer in msg[5::]:
                    if viewer == self.username:
                        i_saw_it = True
                        break
                if not i_saw_it:
                    indiv_unread_msgs_count = indiv_unread_msgs_count+1
            CSVFile.close()

            updateUnreadMessageCountForSpecificChat(
                int(filename.split('_')[0][4::]), int(self.id), indiv_unread_msgs_count)

            total_unread_msgs_count = total_unread_msgs_count + indiv_unread_msgs_count

        updateTotalUnreadMessageCount(self.id, total_unread_msgs_count)
        return True

    def joinUnreadMessagesRecords(self):
        with open(r'databases/unreadMessages.csv', 'a') as CSVFile:
            csv_writer = writer(CSVFile)
            # write the new row for a user
            csv_writer.writerow([self.id, 0])
            CSVFile.close()
        return True

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
                      self.birthyear, self.age, self.location, self.loggedOn, self.username, self.password, self.gender, self.pronoun]
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

    def getFriendRecommendations(self):

        oneGenreMatches = []
        twoGenreMatches = []
        threeGenreMatches = []
        fourGenreMatches = []
        fivePlusGenreMatches = []

        for row in getGenreDB()[1::]:
            their_age = int(getGeneralInfoDB()[int(row[0])][7])
            if ((row[0] != self.id) and (not self.userExistsInFriendsList(row[0]))
                    and (((their_age < 18) and (int(self.age) < 18)) or ((their_age >= 18) and (int(self.age) >= 18)))):
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

        limited = [[], [], [], [], []]
        matcharray = [oneGenreMatches, twoGenreMatches,
                      threeGenreMatches, fourGenreMatches, fivePlusGenreMatches]

        for i in range(len(matcharray)):
            temp_array = matcharray[i]
            if (len(temp_array) <= 5):
                limited[i] = temp_array
            else:
                count = 5
                while (count >= 1):
                    random_index = randint(0, len(temp_array) - 1)
                    exists = False
                    if limited[i] is not None:
                        for j in limited[i]:
                            if j == temp_array[random_index]:
                                exists = True
                                break
                    if not exists:
                        limited[i].append(temp_array[random_index])
                        count = count - 1
        return limited

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

        elif (len(self.birthday) == 1 or len(self.birthday) == 2):
            birth_day = int(self.birthday)

        if (self.birthmonth[0] == '0'):  # single digit birth month? 01-09?
            birth_month = int(self.birthmonth[1])

        elif (len(self.birthmonth) == 1 or len(self.birthmonth) == 2):
            birth_month = int(self.birthmonth)

        birth = date(int(self.birthyear), birth_month, birth_day)
        present = date(int(presentYear), int(presentMonth), int(presentDay))
        days_passed = present - birth

        return math.floor(days_passed.days / 365)

    def updateUserAge(self):
        self.age = self.getCurrentAge()
        updateAge(self.id, self.age)
        return True

    def getBirthdayString(self):
        month = None
        day = None

        if (self.birthmonth == '01' or self.birthmonth == '1'):
            month = 'January'
        elif (self.birthmonth == '02' or self.birthmonth == '2'):
            month = 'February'
        elif (self.birthmonth == '03' or self.birthmonth == '3'):
            month = 'March'
        elif (self.birthmonth == '04' or self.birthmonth == '4'):
            month = 'April'
        elif (self.birthmonth == '05' or self.birthmonth == '5'):
            month = 'May'
        elif (self.birthmonth == '06' or self.birthmonth == '6'):
            month = 'June'
        elif (self.birthmonth == '07' or self.birthmonth == '7'):
            month = 'July'
        elif (self.birthmonth == '08' or self.birthmonth == '8'):
            month = 'August'
        elif (self.birthmonth == '09' or self.birthmonth == '9'):
            month = 'September'
        elif (self.birthmonth == '10'):
            month = 'October'
        elif (self.birthmonth == '11'):
            month = 'November'
        elif (self.birthmonth == '12'):
            month = 'December'

        if (self.birthday[0] == '0'):
            day = self.birthday[1::]
        else:
            day = self.birthday

        return str(month)+" "+str(day)+", "+str(self.birthyear)

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
            self.sent_friend_requests.remove(recipient)  # new - issue 29
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
            self.received_friend_requests.remove(acceptee)  # new - issue 29
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

            self.friends.pop(unfriendeeID - 1)

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
