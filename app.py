from flask import Flask, render_template, url_for, request, redirect
from csv import reader, writer
import sys
import os
from User import setLatestNumberOfUsersAndIDs, getUserCount
from Genre import Genre
from appLoading import loadAllUsers
from forms import LoginForm
from registerAndLogin import verifyCredentials


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key1234567890"

HOMEPAGE_ACCESS_COUNT = 0
ALL_USER_OBJECTS = []

######
CURRENT_USER = None  # no one is logged in yet


def getCURRENT_USER():
    return CURRENT_USER


def setCURRENT_USER(new_current_user):
    global CURRENT_USER
    CURRENT_USER = new_current_user
######


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

####################################################################


@app.route('/', methods=['GET', 'POST'])
def main_page():

    updateHPACount()
    if (HOMEPAGE_ACCESS_COUNT == 1):
        updateAllUserObjects()

    setLatestNumberOfUsersAndIDs()

    try:
        # comes from the html page 'login'
        requestedUsername = request.form['username']
        # comes from the html page 'login'
        requestesPassword = request.form['password']
        if not verifyCredentials(requestedUsername, requestesPassword):

            USERNAME = None
            if getCURRENT_USER() is not None:
                USERNAME = CURRENT_USER
                return render_template("home.html", userCount=getUserCount(), USERNAME=USERNAME)
            else:
                raise Exception
        else:
            setCURRENT_USER(requestedUsername)
            return render_template("home.html", userCount=getUserCount(), USERNAME=CURRENT_USER)

        # if not process_all_form_data(request.form['username'], request.form['password']):
        #     USERNAME = None
        #     if getCURRENT_USER() is not None:
        #         USERNAME = CURRENT_USER
        #         return render_template("home.html", userCount=getUserCount(), USERNAME=USERNAME)
        #     else:
        #         raise Exception
        # else:
        #     setCURRENT_USER(request.form['username'])
        #     return render_template("home.html", userCount=getUserCount(), USERNAME=CURRENT_USER)

    except Exception:
        return redirect(url_for('login_page'))


####################################################################


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    USERNAME = None
    if getCURRENT_USER() is not None:
        USERNAME = CURRENT_USER
        return render_template("home.html", USERNAME=USERNAME)

    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            return redirect(url_for('main_page'))
    return render_template("login.html", form=login_form)


####################################################################
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
