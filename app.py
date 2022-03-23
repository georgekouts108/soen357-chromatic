from flask import Flask, render_template, url_for, request, redirect
from csv import reader, writer
import sys
import os
from User import User, setLatestNumberOfUsersAndIDs, getUserCount
from Genre import Genre
from appLoading import loadAllUsers
from forms import LoginForm
from registerAndLogin import verifyCredentials


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key1234567890"

HOMEPAGE_ACCESS_COUNT = 0
ALL_USER_OBJECTS = []


def updateAllUserObjects():
    global ALL_USER_OBJECTS
    ALL_USER_OBJECTS = loadAllUsers()


def updateHPACount():
    global HOMEPAGE_ACCESS_COUNT
    HOMEPAGE_ACCESS_COUNT = HOMEPAGE_ACCESS_COUNT + 1

####################################################################


@app.route('/', methods=['GET', 'POST'])
def main_page():

    updateHPACount()
    if (HOMEPAGE_ACCESS_COUNT == 1):
        updateAllUserObjects()

    setLatestNumberOfUsersAndIDs()

    return render_template("home.html", userCount=getUserCount())


####################################################################


@app.route('/login', methods=['GET', 'POST'])
def login_page():

    return render_template("login.html")


####################################################################
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
