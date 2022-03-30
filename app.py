from flask import Flask, render_template, url_for, request, redirect
from csv import reader, writer
import sys
import os

from User import User, setLatestNumberOfUsersAndIDs, getUserCount
from Genre import Genre
from appLoading import loadAllUsers, setUpFriendshipFiles, loadAllChats
from forms import GenreManageControls, HomeButton, HomePageButtons, LoginForm, RegisterForm, LoginButton, RegisterButton, GenreManageControls, MessagesPageButtons, NewChatForm, ChatViewForm
from registerAndLogin import verifyCredentials, usernameIsOK, emailIsOK, findActiveUser
from csvEditing import toggleUserLoginState, retrieveFavGenres
from Chat import Chat, setLatestNumberOfChatsAndIDs, getNextChatID, updateNextChatID, updateNumOfActiveChats, getChatCount
from messaging import getInfoForFriends, getYourUsername
from wtforms import SelectMultipleField

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key1234567890"

# NEW -- MARCH 29, 2022
ALL_CHAT_OBJECTS = []


def updateAllChatObjects():
    global ALL_CHAT_OBJECTS
    ALL_CHAT_OBJECTS = loadAllChats()


def getChatMemberBlueprint(username):

    targetUserID = int(findUserID(username))
    their_id = str(ALL_USER_OBJECTS[targetUserID - 1].id)
    their_full_name = str(ALL_USER_OBJECTS[targetUserID - 1].firstname) + " " + str(
        ALL_USER_OBJECTS[targetUserID - 1].lastname)

    return [their_id, their_full_name, username]
# NEW -- MARCH 29, 2022


HOMEPAGE_ACCESS_COUNT = 0
ALL_USER_OBJECTS = []


def updateAllUserObjects():
    global ALL_USER_OBJECTS
    ALL_USER_OBJECTS = loadAllUsers()


def findUserID(username):
    id = 0
    global ALL_USER_OBJECTS
    for a in ALL_USER_OBJECTS:
        if a.username == username:
            id = a.id
            break
    return id


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
                                          form.favoriteGenres.data, form.username.data, form.password.data, 0, True, False, None, None, None)
                    # may not need this
                    global ALL_USER_OBJECTS
                    ALL_USER_OBJECTS.append(registeredUser)
                    # may not need this
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
        return render_template("home.html", USERNAME=USERNAME, userCount=getUserCount(), form2=HomePageButtons())

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

    updateHPACount()
    if (HOMEPAGE_ACCESS_COUNT == 1):
        latestUserCount = setLatestNumberOfUsersAndIDs()
        setUpFriendshipFiles(latestUserCount)
        updateAllUserObjects()

        updateAllChatObjects()  # NEW - MARCH 29
    form2 = HomePageButtons()

    if getCURRENT_USER() is not None:
        toggleUserLoginState(CURRENT_USER, True)
        return render_template("home.html", USERNAME=CURRENT_USER, userCount=getUserCount(), form2=form2)

    return redirect(url_for('login'))


@app.route('/manage_genres')
def manageGenres():
    my_genres = retrieveFavGenres(CURRENT_USER)
    return render_template("genreManage.html", USERNAME=CURRENT_USER, GENRES=my_genres, form2=GenreManageControls())


@app.route('/addordelgenre', methods=['POST', 'GET'])
def add_or_del_genre():

    form2 = GenreManageControls()
    currentUserID = int(findUserID(CURRENT_USER))

    if request.method == 'POST':
        addOrDel = request.form['addordel']
        print("addOrDel == "+str(addOrDel))
        try:
            if (str(addOrDel) == 'add'):
                if form2.favoriteGenres.data is not None:
                    for i in form2.favoriteGenres.data:
                        ALL_USER_OBJECTS[currentUserID - 1].addGenre(i)
            elif (str(addOrDel) == 'del'):
                if form2.favoriteGenres.data is not None:
                    for i in form2.favoriteGenres.data:
                        ALL_USER_OBJECTS[currentUserID - 1].deleteGenre(i)
            else:
                raise Exception()
        except Exception():
            return redirect(url_for('manageGenres'))
    return redirect(url_for('manageGenres'))


@app.route('/connections', methods=['POST', 'GET'])
def connections():
    currentUserID = int(findUserID(CURRENT_USER))
    recommendations = ALL_USER_OBJECTS[currentUserID -
                                       1].getFriendRecommendations()
    myGenres = ALL_USER_OBJECTS[currentUserID -
                                1].favGenres

    # for listing all users besides the current user
    fullNames = []
    usernames = []
    ages = []
    locations = []

    usersCountToShow = 0
    for auo in ALL_USER_OBJECTS:
        if ((auo.username is not CURRENT_USER) and
                (not ALL_USER_OBJECTS[currentUserID - 1].userExistsInFriendsList(auo.username))):
            usersCountToShow = usersCountToShow + 1
            fullNames.append(auo.firstname + " " + auo.lastname)
            usernames.append(auo.username)
            ages.append(auo.age)
            locations.append(auo.location)

    return render_template("connections.html", USERNAME=CURRENT_USER, RECOMMENDATIONS=recommendations, GENRES=myGenres, homeButton=HomeButton(), usernames=usernames, fullnames=fullNames, ages=ages, locations=locations, userCount=usersCountToShow, currentUserID=currentUserID)


@app.route('/my_friends', methods=['POST', 'GET'])
def my_friends():
    currentUserID = int(findUserID(CURRENT_USER))

    myFriends = ALL_USER_OBJECTS[currentUserID - 1].friends
    return render_template("myFriends.html", USERNAME=CURRENT_USER, MY_FRIENDS=myFriends, homeButton=HomeButton())


@app.route('/friend', methods=['POST', 'GET'])
def friend():
    currentUserID = int(findUserID(CURRENT_USER))
    if request.method == 'POST':

        triggeredUsername = request.form.get("my_uname")
        actionToDo = request.form['friend']
        if (actionToDo == 'Add Friend'):
            ALL_USER_OBJECTS[currentUserID -
                             1].sendFriendRequest(triggeredUsername)
        elif (actionToDo == 'Cancel Friend Request'):
            ALL_USER_OBJECTS[currentUserID -
                             1].cancelFriendRequest(triggeredUsername)
        elif (actionToDo == 'Accept Friend Request'):
            ALL_USER_OBJECTS[currentUserID -
                             1].acceptFriendRequest(triggeredUsername)
        elif (actionToDo == 'Unfriend'):
            ALL_USER_OBJECTS[currentUserID -
                             1].unfriendUser(triggeredUsername)
    return redirect(url_for('connections'))


@app.route('/my_messages', methods=['POST', 'GET'])
def messages():
    return render_template("myMessages.html", USERNAME=CURRENT_USER, msgForm=MessagesPageButtons())


@app.route('/new_chat_creation', methods=['POST', 'GET'])
def createChat():
    return render_template("createChat.html", USERNAME=CURRENT_USER, newChatForm=NewChatForm())


@app.route('/chat_host_new_chat', methods=['POST', 'GET'])
def newChat():
    form = NewChatForm()
    if request.method == 'POST':
        recipients = form.recipientOptions.data  # list of recipients' usernames
        message = form.newMessage.data  # the written message

        currentUserID = int(findUserID(CURRENT_USER))
        full_name = str(ALL_USER_OBJECTS[currentUserID - 1].firstname) + \
            " " + str(ALL_USER_OBJECTS[currentUserID - 1].lastname)

        members = [[str(currentUserID), full_name, CURRENT_USER]]

        for r in recipients:
            members.append(getChatMemberBlueprint(r))

        newChat = Chat(members, CURRENT_USER, currentUserID,
                       full_name, message, 0, True)
        chat_log = newChat.retrieveChatLog()

        global ALL_CHAT_OBJECTS
        ALL_CHAT_OBJECTS.append(newChat)

    return render_template("chatHostPage.html", USERNAME=CURRENT_USER, MEMBERS=members, LOG=chat_log, homeButton=HomeButton(), ID=newChat.id, chatform=ChatViewForm())


@app.route('/chat_host', methods=['POST', 'GET'])
def viewChat():
    form = ChatViewForm()
    if request.method == 'POST':
        chat_id = request.form['chatID']
        new_message = form.newMessage.data
        currentUserID = int(findUserID(CURRENT_USER))
        firstname = str(ALL_USER_OBJECTS[currentUserID - 1].firstname)
        lastname = str(ALL_USER_OBJECTS[currentUserID - 1].lastname)
        full_name = firstname+" "+lastname

        ALL_CHAT_OBJECTS[int(chat_id) - 1].appendMessageToChat(
            currentUserID, CURRENT_USER, full_name, new_message)

        members = ALL_CHAT_OBJECTS[int(chat_id)-1].members
        chat_log = ALL_CHAT_OBJECTS[int(chat_id)-1].retrieveChatLog()

        return render_template("chatHostPage.html", USERNAME=CURRENT_USER, MEMBERS=members, LOG=chat_log, homeButton=HomeButton(), ID=ALL_CHAT_OBJECTS[int(chat_id)-1].id, chatform=ChatViewForm())
    return None


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
