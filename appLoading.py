from csv import reader, writer
import csv
from operator import index
import sys
import os
from User import User


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
