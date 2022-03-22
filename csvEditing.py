from csv import reader, writer
import csv
import sys
import os

# credentials edits


# def updatePassword(userID, newPassword):
#     file = open('databases/userCredentials.csv', 'r')
#     csv_reader = reader(file)
#     credential_rows = list(csv_reader)
#     file.close()

#     indexToChange = 0
#     for row in credential_rows:
#         if ((row[0] is userID)):
#             break
#         else:
#             indexToChange = indexToChange + 1
#     credential_rows[indexToChange][2] = newPassword
#     newList = open('databases/userCredentials.csv', 'w', newline='')
#     csv_writer = writer(newList)
#     csv_writer.writerows(credential_rows)
#     newList.close()
#     return True
