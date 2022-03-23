from csv import reader, writer
import csv
from operator import index
import sys
import os


def usernameIsOK(username):  # REGISTER -- check if a username is okay
    yes = True
    if (username == 'Username'):
        return False
    f = open('databases/userGeneralInfo.csv', 'r')
    csv_reader = reader(f)
    user_rows = list(csv_reader)
    f.close()
    for row in user_rows:
        if (row[9] is username):
            yes = False
            break
    return yes


# LOGGING IN -- check if credentials are valid
def verifyCredentials(username, password):
    okay = False
    f = open('databases/userGeneralInfo.csv', 'r')
    csv_reader = reader(f)
    user_rows = list(csv_reader)
    f.close()
    for row in user_rows:
        if (row[9] == username and row[10] == password):
            okay = True
            break
    return okay
