from csv import reader, writer
import csv
from operator import index
import sys
import os


def updateGenres(userID, newGenreArray):
    f = open('databases/userFavGenres.csv', 'r')
    csv_reader = reader(f)
    favorite_genres_rows = list(csv_reader)
    f.close()

    editedEntry = [userID]
    for genre in newGenreArray:
        editedEntry.append(genre)

    favorite_genres_rows[userID] = editedEntry

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
