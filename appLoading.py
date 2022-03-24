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

    for u in range(1, len(general_info_rows)):
        nextGeneralInfoArray = general_info_rows[u]
        nextFavGenresArray = genres_info_rows[u][1::]

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

        nextUser = User(firstname, lastname, email, birthMonth, birthDay, birthYear,
                        location, nextFavGenresArray, username, password, id, False, loggedIn)

        all_users.append(nextUser)

        with open(r"test_databases/TESTallUserLoad_GeneralInfo.csv", 'a') as user_records:
            csv_writer = writer(user_records)
            newRow = [nextUser.id, nextUser.firstname, nextUser.lastname, nextUser.email, nextUser.birthmonth, nextUser.birthday,
                      nextUser.birthyear, nextUser.age, nextUser.location, nextUser.loggedOn, nextUser.username, nextUser.password]
            csv_writer.writerow(newRow)

        with open(r"test_databases/TESTallUserLoad_GenreInfo.csv", 'a') as user_records2:
            csv_writer2 = writer(user_records2)
            newRow2 = [nextUser.id]
            for g in nextUser.favGenres:
                newRow2.append(g)
            csv_writer2.writerow(newRow2)

    return all_users
