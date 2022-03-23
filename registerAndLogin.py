from csv import reader, writer
import csv
from operator import index
import sys
import os


def usernameIsOK(username):  # REGISTER -- check if a username is okay
    yes = True
    if (username is 'Username'):
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
