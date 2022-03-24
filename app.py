from flask import Flask, render_template, url_for, request, redirect
from csv import reader, writer
import sys
import os
from User import User, setLatestNumberOfUsersAndIDs, getUserCount
from Genre import Genre
from appLoading import loadAllUsers
from forms import LoginForm, RegisterForm, LogoutButton, LoginButton, RegisterButton
from registerAndLogin import verifyCredentials, usernameIsOK, emailIsOK, findActiveUser
from csvEditing import toggleUserLoginState


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


CURRENT_USER = None  # no one is logged in yet


def getCURRENT_USER():
    return CURRENT_USER


def setCURRENT_USER(new_current_user):
    global CURRENT_USER
    CURRENT_USER = new_current_user


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    form2 = LoginButton()
    return render_template("register.html", form=form, form2=form2)


@app.route('/createuser', methods=['POST', 'GET'])
def createNewUser():
    # args of User() need to be tweaked later...
    form = RegisterForm()
    if request.method == 'POST':

        # must parse the birthday fields and compute age
        birthday = request.form['birth_day']
        birth_year = birthday[0:4]
        birth_month = birthday[5:7]
        birth_day = birthday[8:]
        if form.validate_on_submit:
            try:
                passwordsMatch = (form.password.data == form.confirm_pwd.data)
                usernameIsNew = usernameIsOK(form.username.data)
                email_is_ok = emailIsOK(form.email.data)
                if (email_is_ok and usernameIsNew and passwordsMatch):
                    registeredUser = User(form.firstName.data, form.lastName.data, form.email.data, birth_month, birth_day, birth_year, form.location.data,
                                          form.favoriteGenres.data, form.username.data, form.password.data, 0, True, False)
                else:
                    raise Exception()
            except Exception:
                return redirect(url_for('register'))

    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    USERNAME = None

    activeUser = findActiveUser()
    if activeUser is not None:
        setCURRENT_USER(activeUser)

    if getCURRENT_USER() is not None:
        USERNAME = CURRENT_USER
        return render_template("home.html", USERNAME=USERNAME, userCount=getUserCount(), form2=LogoutButton())

    form = LoginForm()
    form2 = RegisterButton()

    if request.method == 'POST':
        if verifyCredentials(form.username.data, form.password.data):
            setCURRENT_USER(form.username.data)
            return redirect(url_for('main_page'))
    return render_template("login.html", form=form, form2=form2)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if getCURRENT_USER() is not None:
        toggleUserLoginState(CURRENT_USER, False)
        setCURRENT_USER(None)
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def main_page():

    updateAllUserObjects()
    setLatestNumberOfUsersAndIDs()

    form2 = LogoutButton()

    if getCURRENT_USER() is not None:
        toggleUserLoginState(CURRENT_USER, True)
        return render_template("home.html", USERNAME=CURRENT_USER, userCount=getUserCount(), form2=form2)

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
