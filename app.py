from flask import Flask, render_template
from csv import reader, writer
import sys
import os
from User import setLatestNumberOfUsersAndIDs, getUserCount
from Genre import Genre
from appLoading import loadAllUsers
app = Flask(__name__)

HOMEPAGE_ACCESS_COUNT = 0
ALL_USER_OBJECTS = []


def findUser(username, password):
    for user in ALL_USER_OBJECTS:
        if ((user.username == username) and (user.password == password)):
            return user
    return None


def updateAllUserObjects():
    global ALL_USER_OBJECTS
    ALL_USER_OBJECTS = loadAllUsers()


def updateHPACount():
    global HOMEPAGE_ACCESS_COUNT
    HOMEPAGE_ACCESS_COUNT = HOMEPAGE_ACCESS_COUNT + 1


@app.route('/', methods=['GET', 'POST'])
def main_page():

    updateHPACount()
    if (HOMEPAGE_ACCESS_COUNT == 1):
        updateAllUserObjects()

    setLatestNumberOfUsersAndIDs()

    return render_template("home.html", userCount=getUserCount())


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
