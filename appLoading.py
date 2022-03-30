from csv import reader, writer
import csv
from operator import index
import sys
import os
from User import User
from Chat import Chat


def loadAllUsers():
    all_users = []

    # save all the existing general information about users
    general = open('databases/userGeneralInfo.csv', 'r')
    general_csv_reader = reader(general)
    general_info_rows = list(general_csv_reader)
    general.close()

    # save all the existing genre preferences of users
    genres = open('databases/userFavGenres.csv', 'r')
    genres_csv_reader = reader(genres)
    genres_info_rows = list(genres_csv_reader)
    genres.close()

    # [NEW] save all the existing friendships of users
    friendships = open('databases/userFriends.csv', 'r')
    friendships_csv_reader = reader(friendships)
    friendships_info_rows = list(friendships_csv_reader)
    friendships.close()

    # [NEW] save all the sent friend requests of users
    sent_friend_reqs = open('databases/userSentFriendRequests.csv', 'r')
    friendships_csv_reader2 = reader(sent_friend_reqs)
    sentReqs_info_rows = list(friendships_csv_reader2)
    sent_friend_reqs.close()

    # [NEW] save all the received friend requests of users
    rec_friend_reqs = open('databases/userReceivedFriendRequests.csv', 'r')
    friendships_csv_reader3 = reader(rec_friend_reqs)
    recReqs_info_rows = list(friendships_csv_reader3)
    rec_friend_reqs.close()

    for u in range(1, len(general_info_rows)):
        nextGeneralInfoArray = general_info_rows[u]
        nextFavGenresArray = genres_info_rows[u][1::]
        nextFriendshipArray = friendships_info_rows[u]
        nextSentFriendReqsArray = sentReqs_info_rows[u]
        nextReceivedFriendReqsArray = recReqs_info_rows[u]

        # GENERAL INFO PARAMETERS
        id = nextGeneralInfoArray[0]
        firstname = nextGeneralInfoArray[1]
        lastname = nextGeneralInfoArray[2]
        email = nextGeneralInfoArray[3]
        birthMonth = nextGeneralInfoArray[4]
        birthDay = nextGeneralInfoArray[5]
        birthYear = nextGeneralInfoArray[6]
        location = nextGeneralInfoArray[8]
        loggedIn = nextGeneralInfoArray[9]
        username = nextGeneralInfoArray[10]
        password = nextGeneralInfoArray[11]

        # FRIENDSHIP INFO PARAMETERS

        nextUser = User(firstname, lastname, email, birthMonth, birthDay, birthYear,
                        location, nextFavGenresArray, username, password, id, False, loggedIn, nextFriendshipArray, nextSentFriendReqsArray, nextReceivedFriendReqsArray)

        all_users.append(nextUser)

    return all_users


def setUpFriendshipFiles(latestUserCount):

    if (latestUserCount > 0):

        # 1
        friendships = open('databases/userFriends.csv', 'r')
        friendships_csv_reader = reader(friendships)
        friendships_info_rows = list(friendships_csv_reader)
        friendships.close()

        with open(r"databases/userFriends.csv", 'a') as user_records:
            csv_writer = writer(user_records)
            for i in range(1, latestUserCount+1):
                rowExists = False
                for fr in friendships_info_rows:
                    if (fr[0] == str(i)):
                        rowExists = True
                        break
                if not rowExists:
                    csv_writer.writerow([str(i)])
        user_records.close()
        # 1

        # 2
        sent_friend_reqs = open('databases/userSentFriendRequests.csv', 'r')
        friendships_csv_reader2 = reader(sent_friend_reqs)
        sentReqs_info_rows = list(friendships_csv_reader2)
        sent_friend_reqs.close()

        with open(r"databases/userSentFriendRequests.csv", 'a') as user_records2:
            csv_writer2 = writer(user_records2)
            for i in range(1, latestUserCount+1):

                rowExists = False
                for fr in sentReqs_info_rows:
                    if (fr[0] == str(i)):
                        rowExists = True
                        break
                if not rowExists:
                    csv_writer2.writerow([str(i)])
        user_records2.close()
        # 2

        # 3
        rec_friend_reqs = open('databases/userReceivedFriendRequests.csv', 'r')
        friendships_csv_reader3 = reader(rec_friend_reqs)
        recReqs_info_rows = list(friendships_csv_reader3)
        rec_friend_reqs.close()

        with open(r"databases/userReceivedFriendRequests.csv", 'a') as user_records3:
            csv_writer3 = writer(user_records3)
            for i in range(1, latestUserCount+1):

                rowExists = False
                for fr in recReqs_info_rows:
                    if (fr[0] == str(i)):
                        rowExists = True
                        break
                if not rowExists:
                    csv_writer3.writerow([str(i)])
        user_records3.close()
        # 3


def loadAllChats():
    all_chat_logs = []

    listOfChatFilenames = os.listdir("chats/")

    if listOfChatFilenames is None:
        print("NONE")
        return None
    print("NOT NONE")
    for filename in listOfChatFilenames:
        chat_log = open("chats/"+str(filename)+"", 'r')
        csv_reader = reader(chat_log)
        rows = list(csv_reader)
        chat_log.close()

        next_chat_log = rows[1::]
        next_member_set = []

        memberIDs = filename.split('_')

        general = open('databases/userGeneralInfo.csv', 'r')
        general_csv_reader = reader(general)
        general_info_rows = list(general_csv_reader)
        for index in range(1, len(memberIDs)-1):
            next_member = [str(memberIDs[index])]
            next_fullname = general_info_rows[int(
                memberIDs[index])][1]+" "+general_info_rows[int(memberIDs[index])][2]
            next_username = general_info_rows[int(memberIDs[index])][10]
            next_member.append(next_fullname)
            next_member.append(next_username)
            next_member_set.append(next_member)
        general.close()

        first_username = rows[1][1]
        first_fullname = rows[1][2]
        first_userID = rows[1][0]
        first_message = rows[1][3]
        chat_id = int(memberIDs[0][4::])
        next_chat_log = Chat(next_member_set, first_username,
                             first_userID, first_fullname, first_message, chat_id, False)
        all_chat_logs.append(next_chat_log)

    return all_chat_logs
