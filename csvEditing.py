from csv import reader, writer
import csv
from operator import index
import sys
import os

# credentials edits


def updateGenres(userID, newGenreArray):
    f = open('databases/userFavGenres.csv', 'r')
    csv_reader = reader(f)
    favorite_genres_rows = list(csv_reader)
    f.close()
    favorite_genres_rows[userID][1] = ','.join(
        str(genre) for genre in newGenreArray)
    newList = open('databases/userFavGenres.csv', 'w', newline='')
    csv_writer = writer(newList)
    csv_writer.writerows(favorite_genres_rows)
    newList.close()
    return True


def updatePassword(userID, newPassword):
    f = open('databases/userCredentials.csv', 'r')
    csv_reader = reader(f)
    credential_rows = list(csv_reader)
    f.close()
    credential_rows[userID][2] = newPassword
    newList = open('databases/userCredentials.csv', 'w', newline='')
    csv_writer = writer(newList)
    csv_writer.writerows(credential_rows)
    newList.close()
