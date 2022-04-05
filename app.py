from flask import Flask, render_template, url_for, request, redirect
from csv import reader
import sys
import os
from datetime import datetime
from Genre import getListOfGenres
from User import User, setLatestNumberOfUsersAndIDs, getUserCount
from appLoading import loadAllUsers, setUpFriendshipFiles, loadAllChats
from forms import GenreManageControls, HomeButton, HomePageButtons, LoginForm, RegisterForm, LoginButton, RegisterButton, GenreManageControls, MessagesPageButtons, NewChatForm, ChatViewForm, ForgotPasswordForm
from registerAndLogin import verifyCredentials, usernameIsOK, emailIsOK, findActiveUser, verifyUsernameOrEmail
from csvEditing import getGeneralInfoDB, toggleUserLoginState, retrieveFavGenres, updatePassword, retrieveGeneralInfo
from Chat import Chat
from messaging import getInfoForFriends, removeEmptyChatFiles


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key1234567890"

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


HOMEPAGE_ACCESS_COUNT = 0
ALL_USER_OBJECTS = []


def updateAllUserAges():
    global ALL_USER_OBJECTS
    if (ALL_USER_OBJECTS is not None):
        for i in range(len(ALL_USER_OBJECTS)):
            ALL_USER_OBJECTS[i].updateUserAge()


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
    updateAllUserAges()

    form = RegisterForm()
    form2 = LoginButton()

    all_genres = getListOfGenres()
    for a in range(len(all_genres)):
        all_genres[a] = all_genres[a][6::]

    return render_template("register.html", form=form, form2=form2, GENRES=all_genres)


@app.route('/createuser', methods=['POST', 'GET'])
def createNewUser():
    updateAllUserAges()

    error_code = 0
    form = RegisterForm()
    if request.method == 'POST':

        birthday = request.form['birth_day']
        birth_year = birthday[0:4]
        birth_month = birthday[5:7]
        birth_day = birthday[8:]

        age = 0
        presentTime = datetime.now()
        presentDay = presentTime.strftime("%d")
        presentMonth = presentTime.strftime("%m")
        presentYear = presentTime.strftime("%Y")

        if (presentDay[0] == '0'):  # single digit day? 01-09?
            presentDay = presentDay[1]
        if (presentMonth[0] == '0'):  # single digit month? 01-09?
            presentMonth = presentMonth[1]

        birthDay = 0
        birthMonth = 0

        if (birth_day[0] == '0'):  # single digit birth day? 01-09?
            birthDay = int(birth_day[1])

        if (birth_month[0] == '0'):  # single digit birth month? 01-09?
            birthMonth = int(birth_month[1])

        isBirthdayToday = ((birthMonth == int(presentMonth))
                           and (birthDay == int(presentDay)))

        if (isBirthdayToday):
            age = (int(presentYear) - int(birth_year))
        else:
            age = (int(presentYear) - int(birth_year) - 1)

        if form.validate_on_submit:

            try:
                listofgenres = request.form.getlist('genre')

                genderIsChosen = False
                chosen_gender = request.form['gender']
                if (str(chosen_gender) == 'Male'):
                    genderIsChosen = True
                elif (str(chosen_gender) == 'Female'):
                    genderIsChosen = True
                elif (str(chosen_gender) == 'Unspecified'):
                    genderIsChosen = True

                pronounIsChosen = False
                chosen_pronoun = request.form['pronoun']

                if (str(chosen_pronoun) == 'He/Him'):
                    pronounIsChosen = True
                elif (str(chosen_pronoun) == 'She/Her'):
                    pronounIsChosen = True
                elif (str(chosen_pronoun) == 'They/Them'):
                    pronounIsChosen = True

                # implement later...
                chosen_picture = request.form['photo']
                print("DEBUGGING OVER HERE: chosen_picture== "+str(chosen_picture))
                # implement later...

                passwordsMatch = (form.password.data == form.confirm_pwd.data)
                usernameIsNew = usernameIsOK(form.username.data)
                email_is_ok = emailIsOK(form.email.data)
                if (email_is_ok and usernameIsNew and passwordsMatch and (age >= 13) and genderIsChosen):
                    registeredUser = User(form.firstName.data, form.lastName.data, form.email.data, birth_month, birth_day,
                                          birth_year, form.location.data, listofgenres, form.username.data, form.password.data, chosen_gender, chosen_pronoun, 0)

                    global ALL_USER_OBJECTS
                    ALL_USER_OBJECTS.append(registeredUser)
                else:
                    if not usernameIsNew:
                        error_code = 100
                    elif not email_is_ok:
                        error_code = 200
                    elif not passwordsMatch:
                        error_code = 300
                    elif not (age >= 13):
                        error_code = 400
                    elif not genderIsChosen:
                        error_code = 500
                    elif not pronounIsChosen:
                        error_code = 600

                    raise Exception()
            except Exception:
                return render_template("errorReport.html", ERRCODE=error_code)

    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    updateAllUserAges()

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
    updateAllUserAges()

    if getCURRENT_USER() is not None:
        toggleUserLoginState(CURRENT_USER, False)
        setCURRENT_USER(None)
    return redirect(url_for('login'))


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    updateAllUserAges()

    return render_template("forgotPassword.html", form=ForgotPasswordForm())


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    updateAllUserAges()

    form = ForgotPasswordForm()
    if request.method == 'POST':
        identity = form.identity.data
        new_pwd = form.new_password.data

        if verifyUsernameOrEmail(identity) != 'n':
            targetUserID = 0
            f = open('databases/userGeneralInfo.csv', 'r')
            csv_reader = reader(f)
            user_rows = list(csv_reader)
            f.close()
            # did the user give their email?
            if (verifyUsernameOrEmail(identity) == 'e'):
                for r in user_rows[1::]:
                    if (r[3] == identity):
                        targetUserID = int(r[0])
                        break
            # did the user give their username?
            elif (verifyUsernameOrEmail(identity) == 'u'):
                for r in user_rows[1::]:
                    if (r[10] == identity):
                        targetUserID = int(r[0])
                        break
            updatePassword(targetUserID, new_pwd)
            return redirect(url_for('login'))
    return redirect(url_for('forgot_password'))


@app.route('/', methods=['GET', 'POST'])
def main_page():

    removeEmptyChatFiles()

    updateHPACount()
    if (HOMEPAGE_ACCESS_COUNT == 1):
        latestUserCount = setLatestNumberOfUsersAndIDs()
        print('LATEST USER COUNT == '+str(latestUserCount))
        setUpFriendshipFiles(latestUserCount)
        updateAllUserObjects()
        updateAllChatObjects()
        updateAllUserAges()
    form2 = HomePageButtons()

    updateAllUserAges()

    if getCURRENT_USER() is not None:
        toggleUserLoginState(CURRENT_USER, True)
        return render_template("home.html", USERNAME=CURRENT_USER, userCount=getUserCount(), form2=form2)

    return redirect(url_for('login'))


@app.route('/manage_genres')
def manageGenres():
    updateAllUserAges()

    my_genres = retrieveFavGenres(CURRENT_USER)

    all_genres = getListOfGenres()
    for a in range(len(all_genres)):
        all_genres[a] = all_genres[a][6::]
    return render_template("genreManage.html", USERNAME=CURRENT_USER, GENRES=my_genres, ALL_GENRES=all_genres, form2=GenreManageControls())


@app.route('/addordelgenre', methods=['POST', 'GET'])
def add_or_del_genre():
    updateAllUserAges()

    form2 = GenreManageControls()
    currentUserID = int(findUserID(CURRENT_USER))

    if request.method == 'POST':
        addOrDel = request.form['addordel']
        if (str(addOrDel) is None):
            raise Exception()
        print("addOrDel == "+str(addOrDel))
        try:
            if (str(addOrDel) == 'add'):
                if request.form.getlist('genre') is not None:
                    for i in request.form.getlist('genre'):
                        ALL_USER_OBJECTS[currentUserID - 1].addGenre(i)
            elif (str(addOrDel) == 'del'):
                if request.form.getlist('genre') is not None:
                    for i in request.form.getlist('genre'):
                        ALL_USER_OBJECTS[currentUserID - 1].deleteGenre(i)
            else:
                raise Exception()
        except Exception():
            return redirect(url_for('manageGenres'))
    return redirect(url_for('manageGenres'))


@app.route('/connections', methods=['POST', 'GET'])
def connections():
    updateAllUserAges()

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
        if ((auo.username is not CURRENT_USER)
            and (
            (int(auo.age) >= 18 and int(
                ALL_USER_OBJECTS[currentUserID - 1].age) >= 18)
                or (int(auo.age) < 18 and int(ALL_USER_OBJECTS[currentUserID - 1].age) < 18))):
            usersCountToShow = usersCountToShow + 1
            fullNames.append(auo.firstname + " " + auo.lastname)
            ages.append(auo.age)
            locations.append(auo.location)

            isFriend = ALL_USER_OBJECTS[currentUserID -
                                        1].userExistsInFriendsList(auo.username)
            isReqSent = ALL_USER_OBJECTS[currentUserID -
                                         1].userExistsInSentRequestsList(auo.username)
            isReqReceived = ALL_USER_OBJECTS[currentUserID -
                                             1].userExistsInReceivedRequests(auo.username)

            username_info = [auo.username, isFriend, isReqSent, isReqReceived]
            usernames.append(username_info)

    return render_template("connections.html", USERNAME=CURRENT_USER, RECOMMENDATIONS=recommendations, GENRES=myGenres, homeButton=HomeButton(), usernames=usernames, fullnames=fullNames, ages=ages, locations=locations, userCount=usersCountToShow, currentUserID=currentUserID, GENERAL_INFO_DB=getGeneralInfoDB())


@app.route('/find_friends', methods=['GET', 'POST'])
def find_friends():
    updateAllUserAges()

    currentUserID = int(findUserID(CURRENT_USER))
    if request.method == 'POST':
        updateAllUserAges()
        query = str(request.form.get('search'))

        general_info_db = getGeneralInfoDB()[1::]
        filtered_db = []
        for gen in general_info_db:
            is_not_me = (int(gen[0]) != currentUserID)
            is_potential_fullname = (
                query.lower() in (gen[1]+" "+gen[2]).lower())
            is_potential_username = (query.lower() in gen[10].lower())
            is_age_appropriate = (
                (int(str(gen[7])) >= 18 and int(
                    ALL_USER_OBJECTS[currentUserID - 1].age) >= 18)
                or (int(str(gen[7])) < 18 and int(ALL_USER_OBJECTS[currentUserID - 1].age) < 18)
            )
            if (is_age_appropriate and is_not_me and (is_potential_fullname or is_potential_username)):

                isFriend = ALL_USER_OBJECTS[currentUserID -
                                            1].userExistsInFriendsList(gen[10])
                isReqSent = ALL_USER_OBJECTS[currentUserID -
                                             1].userExistsInSentRequestsList(gen[10])
                isReqReceived = ALL_USER_OBJECTS[currentUserID -
                                                 1].userExistsInReceivedRequests(gen[10])

                filtered_db.append([gen, isFriend, isReqSent, isReqReceived])

            print("filtered db="+str(filtered_db))
    return render_template("findFriends.html", USERNAME=CURRENT_USER, FILTER=filtered_db, homeButton=HomeButton())


@app.route('/my_friends', methods=['POST', 'GET'])
def my_friends():
    updateAllUserAges()

    currentUserID = int(findUserID(CURRENT_USER))
    myFriends = ALL_USER_OBJECTS[currentUserID - 1].friends[1::]
    print("myFriends = "+str(myFriends))
    return render_template("myFriends.html", USERNAME=CURRENT_USER, MY_FRIENDS=myFriends, homeButton=HomeButton())


@app.route('/friend', methods=['POST', 'GET'])
def friend():
    updateAllUserAges()

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
        elif (actionToDo == 'View Profile'):

            their_general_info = retrieveGeneralInfo(triggeredUsername)

            their_full_name = their_general_info[1]+" "+their_general_info[2]
            their_birthday = ALL_USER_OBJECTS[int(
                findUserID(triggeredUsername)) - 1].getBirthdayString()
            their_age = their_general_info[7]
            their_location = their_general_info[8]
            their_status = their_general_info[9]
            their_genres = retrieveFavGenres(triggeredUsername)

            mutual_genres = []
            your_genres = retrieveFavGenres(CURRENT_USER)
            for tg in their_genres:
                for yg in your_genres:
                    if (yg == tg):
                        mutual_genres.append(tg)
                        break

            their_friends = ALL_USER_OBJECTS[int(
                findUserID(triggeredUsername)) - 1].friends

            mutual_friends = []
            your_friends = ALL_USER_OBJECTS[int(
                findUserID(CURRENT_USER)) - 1].friends
            if your_friends is not None and their_friends is not None:
                for tf in their_friends:
                    for yf in your_friends:
                        if (yf == tf):
                            mutual_friends.append(tf)
                            break

            isFriend = ALL_USER_OBJECTS[currentUserID -
                                        1].userExistsInFriendsList(triggeredUsername)
            isReqSent = ALL_USER_OBJECTS[currentUserID -
                                         1].userExistsInSentRequestsList(triggeredUsername)
            isReqReceived = ALL_USER_OBJECTS[currentUserID -
                                             1].userExistsInReceivedRequests(triggeredUsername)

            friendship_status_info = [
                triggeredUsername, isFriend, isReqSent, isReqReceived]

            their_gender = ALL_USER_OBJECTS[int(
                findUserID(triggeredUsername)) - 1].gender

            their_pronoun = ALL_USER_OBJECTS[int(
                findUserID(triggeredUsername)) - 1].pronoun

            return render_template("userProfile.html", FULLNAME=their_full_name, USERNAME=triggeredUsername, BIRTHDAY=their_birthday, AGE=their_age, LOCATION=their_location, STATUS=their_status, ALL_GENRES=their_genres, MUT_GENRES=mutual_genres, ALL_FRIENDS=their_friends, MUT_FRIENDS=mutual_friends, FRIEND_STATUS_INFO=friendship_status_info, GENDER=their_gender, PRONOUN=their_pronoun)
    return redirect(url_for('connections'))


@app.route('/my_messages', methods=['POST', 'GET'])
def messages():
    updateAllUserAges()

    chatIDs = []
    listOfChatFiles = os.listdir("chats/")
    for filename in listOfChatFiles:
        splitted = filename.split('_')
        for s in splitted[1:len(splitted)-1]:
            if (str(s) == str(findUserID(CURRENT_USER))):
                chatIDs.append(str(splitted[0][4::]))
                break

    currentUserID = int(findUserID(CURRENT_USER))

    numberOfFriends = 0
    print("DEBUGGING HERE: ALL_USER_OBJECTS[currentUserID - 1].friends == "+str(
        ALL_USER_OBJECTS[currentUserID - 1].friends))

    if ALL_USER_OBJECTS[currentUserID - 1].friends is not None:
        numberOfFriends = len(ALL_USER_OBJECTS[currentUserID - 1].friends[1::])
    print("numberOfFriends == "+str(numberOfFriends))
    return render_template("myMessages.html", USERNAME=CURRENT_USER, msgForm=MessagesPageButtons(), CHAT_IDS=chatIDs, FRIEND_COUNT=numberOfFriends)


@app.route('/new_chat_creation', methods=['POST', 'GET'])
def createChat():
    updateAllUserAges()

    yourFriends = getInfoForFriends(CURRENT_USER)
    return render_template("createChat.html", USERNAME=CURRENT_USER, YOUR_FRIENDS=yourFriends, newChatForm=NewChatForm())


@app.route('/direct_message', methods=['POST', 'GET'])
def directMessage():
    updateAllUserAges()

    if request.method == 'POST':
        currentUserID = int(findUserID(CURRENT_USER))

        full_name = str(ALL_USER_OBJECTS[currentUserID - 1].firstname) + \
            " " + str(ALL_USER_OBJECTS[currentUserID - 1].lastname)

        members = [[str(currentUserID), full_name, CURRENT_USER]]
        recipient_gen_info = retrieveGeneralInfo(request.form.get("dm"))

        recipient_user_id = recipient_gen_info[0]
        recipient_full_name = recipient_gen_info[1]+" "+recipient_gen_info[2]
        members.append(
            [recipient_user_id, recipient_full_name, request.form.get("dm")])

        chatID = 0
        listOfChatFilenames = os.listdir("chats/")
        existing_chat_found = False
        for filename in listOfChatFilenames:

            memberIDs = filename.split('_')
            id_count = 0
            for m_id in memberIDs[1:len(memberIDs)-1]:
                for mem in members:
                    if (str(mem[0]) == str(m_id)):
                        id_count = id_count + 1
                        break

            if (id_count == len(memberIDs[1:len(memberIDs)-1])) and (id_count == 2):
                chatID = int(filename.split('_')[0][4::])
                existing_chat_found = True
                break

        global ALL_CHAT_OBJECTS
        if not existing_chat_found:

            newChat = Chat(members, CURRENT_USER, currentUserID,
                           full_name, None, 0, True)

            ALL_CHAT_OBJECTS.append(newChat)

        chat_log = ALL_CHAT_OBJECTS[int(chatID) - 1].retrieveChatLog()

    return render_template("chatHostPage.html", USERNAME=CURRENT_USER, MEMBERS=members, LOG=chat_log, homeButton=HomeButton(), ID=chatID, chatform=ChatViewForm())


@app.route('/chat_host_new_chat', methods=['POST', 'GET'])
def newChat():
    updateAllUserAges()

    form = NewChatForm()
    if request.method == 'POST':

        currentUserID = int(findUserID(CURRENT_USER))

        full_name = str(ALL_USER_OBJECTS[currentUserID - 1].firstname) + \
            " " + str(ALL_USER_OBJECTS[currentUserID - 1].lastname)
        message = str(form.newMessage.data)

        members = [[str(currentUserID), full_name, CURRENT_USER]]
        invitees = request.form.getlist('invitee')
        for i in invitees:
            members.append(getChatMemberBlueprint(i))

        chatID = 0
        listOfChatFilenames = os.listdir("chats/")
        existing_chat_found = False
        for filename in listOfChatFilenames:

            memberIDs = filename.split('_')
            id_count = 0
            for m_id in memberIDs[1:len(memberIDs)-1]:
                for mem in members:
                    if (str(mem[0]) == str(m_id)):
                        id_count = id_count + 1
                        break

            if (id_count == len(memberIDs[1:len(memberIDs)-1])) and (id_count == (len(invitees)+1)):
                chatID = int(filename.split('_')[0][4::])
                existing_chat_found = True
                break

        global ALL_CHAT_OBJECTS
        if existing_chat_found is True:

            ALL_CHAT_OBJECTS[int(chatID) - 1].appendMessageToChat(
                currentUserID, CURRENT_USER, full_name, message)
        else:
            newChat = Chat(members, CURRENT_USER, currentUserID,
                           full_name, message, 0, True)

            ALL_CHAT_OBJECTS.append(newChat)

        chat_log = ALL_CHAT_OBJECTS[int(chatID) - 1].retrieveChatLog()

    return render_template("chatHostPage.html", USERNAME=CURRENT_USER, MEMBERS=members, LOG=chat_log, homeButton=HomeButton(), ID=chatID, chatform=ChatViewForm())

# below is the route where you append a new message to a chat


@app.route('/chat_host', methods=['POST', 'GET'])
def viewChat():
    updateAllUserAges()

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


@app.route('/prev_chat_host', methods=['POST', 'GET'])
def prevChat():
    updateAllUserAges()

    if request.method == 'POST':
        visited_chat_id = int(request.form['chat'][6::])
        members = ALL_CHAT_OBJECTS[int(visited_chat_id) - 1].members
        chat_log = ALL_CHAT_OBJECTS[int(visited_chat_id)-1].retrieveChatLog()

    return render_template("chatHostPage.html", USERNAME=CURRENT_USER, chatform=ChatViewForm(), homeButton=HomeButton(), ID=visited_chat_id, MEMBERS=members, LOG=chat_log)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
