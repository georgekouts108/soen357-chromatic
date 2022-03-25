from csv import reader, writer
import csv
from operator import index
import sys
import os


def getGeneralInfoDB():
    f = open('databases/userGeneralInfo.csv', 'r')
    csv_reader2 = reader(f)
    general_info_rows = list(csv_reader2)
    f.close()
    return general_info_rows


def getGenreDB():
    f = open('databases/userFavGenres.csv', 'r')
    csv_reader2 = reader(f)
    favorite_genres_rows = list(csv_reader2)
    f.close()
    return favorite_genres_rows  # including the header


def retrieveFavGenres(username):
    currentUserID = 0
    my_genres = []
    g = open('databases/userGeneralInfo.csv', 'r')
    csv_reader1 = reader(g)
    general_info_rows = list(csv_reader1)
    g.close()
    for general in general_info_rows:
        if (general[10] == username):
            currentUserID = general[0]
            break

    f = open('databases/userFavGenres.csv', 'r')
    csv_reader2 = reader(f)
    favorite_genres_rows = list(csv_reader2)
    f.close()

    for genre in favorite_genres_rows:
        if genre[0] == currentUserID:
            my_genres = genre[1::]
            break

    return my_genres


def updateGenres(userID, newGenreArray):
    f = open('databases/userFavGenres.csv', 'r')
    csv_reader = reader(f)
    favorite_genres_rows = list(csv_reader)
    f.close()

    editedEntry = [userID]
    for genre in newGenreArray:
        editedEntry.append(genre)

    favorite_genres_rows[int(userID)] = editedEntry

    newList = open('databases/userFavGenres.csv', 'w', newline='')
    csv_writer = writer(newList)
    csv_writer.writerows(favorite_genres_rows)
    newList.close()
    return True


def updatePassword(userID, newPassword):
    f = open('databases/userGeneralInfo.csv', 'r')
    csv_reader = reader(f)
    user_rows = list(csv_reader)
    f.close()
    user_rows[userID][11] = newPassword
    newList = open('databases/userGeneralInfo.csv', 'w', newline='')
    csv_writer = writer(newList)
    csv_writer.writerows(user_rows)
    newList.close()


def toggleUserLoginState(username, state):
    f = open('databases/userGeneralInfo.csv', 'r')
    csv_reader = reader(f)
    user_rows = list(csv_reader)
    f.close()

    indexToToggle = 0
    for row in user_rows:
        if (row[10] == username):
            break
        else:
            indexToToggle = indexToToggle + 1

    user_rows[indexToToggle][9] = state
    newList = open('databases/userGeneralInfo.csv', 'w', newline='')
    csv_writer = writer(newList)
    csv_writer.writerows(user_rows)
    newList.close()
