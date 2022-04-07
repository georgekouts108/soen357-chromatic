from csv import reader, writer
import os
from User import User
from Chat import Chat
from messaging import removeEmptyChatFiles


def loadAllUsers():
    all_users = []

    general = open('databases/userGeneralInfo.csv', 'r')
    general_csv_reader = reader(general)
    general_info_rows = list(general_csv_reader)
    general.close()

    genres = open('databases/userFavGenres.csv', 'r')
    genres_csv_reader = reader(genres)
    genres_info_rows = list(genres_csv_reader)
    genres.close()

    friendships = open('databases/userFriends.csv', 'r')
    friendships_csv_reader = reader(friendships)
    friendships_info_rows = list(friendships_csv_reader)
    friendships.close()

    sent_friend_reqs = open('databases/userSentFriendRequests.csv', 'r')
    friendships_csv_reader2 = reader(sent_friend_reqs)
    sentReqs_info_rows = list(friendships_csv_reader2)
    sent_friend_reqs.close()

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
        gender = nextGeneralInfoArray[12]
        pronoun = nextGeneralInfoArray[13]

        nextUser = User(firstname, lastname, email, birthMonth, birthDay, birthYear,
                        location, nextFavGenresArray, username, password, gender, pronoun, id, False, loggedIn, nextFriendshipArray, nextSentFriendReqsArray, nextReceivedFriendReqsArray)

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

        # 4
        genres = open('databases/userFavGenres.csv', 'r')
        genre_reader = reader(genres)
        fav_genres_rows = list(genre_reader)
        genres.close()

        with open(r"databases/userFavGenres.csv", 'a') as user_records4:
            csv_writer4 = writer(user_records4)
            for i in range(1, latestUserCount+1):

                rowExists = False
                for fr in fav_genres_rows:
                    if (fr[0] == str(i)):
                        rowExists = True
                        break
                if not rowExists:
                    csv_writer4.writerow([str(i)])
        user_records4.close()
        # 4


def loadAllChats():
    all_chats = []

    listOfChatFilenames = os.listdir("chats/")

    if listOfChatFilenames is None:
        return None

    for filename in listOfChatFilenames:
        chat_log = open("chats/"+str(filename)+"", 'r')
        csv_reader = reader(chat_log)
        rows = list(csv_reader)
        chat_log.close()

        removeEmptyChatFiles()

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
        next_chat = Chat(next_member_set, first_username,
                         first_userID, first_fullname, first_message, chat_id, next_chat_log, False)
        all_chats.append(next_chat)

    return all_chats
