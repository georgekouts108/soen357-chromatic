from csv import reader, writer
import csv
from operator import index
import sys
import os

# credentials edits


def updatePassword(userID, newPassword):
    f = open('databases/userCredentials.csv', 'r')
    csv_reader = reader(f)
    credential_rows = list(csv_reader)
    f.close()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$" +
          str(len(credential_rows)) + "== len of redentials row")
    indexToChange = 0
    for row in credential_rows:
        if ((row[0] == userID)):
            break
        else:
            indexToChange = indexToChange + 1
    print("#####################"+str(indexToChange) + "== index to change")
    credential_rows[indexToChange - 1][2] = newPassword

    newList = open('databases/userCredentials.csv', 'w', newline='')
    csv_writer = writer(newList)
    csv_writer.writerows(credential_rows)
    newList.close()
