from csv import reader


def usernameIsOK(username):
    yes = True
    if (username == 'Username'):
        return False
    f = open('databases/userGeneralInfo.csv', 'r')
    csv_reader = reader(f)
    user_rows = list(csv_reader)
    f.close()
    for row in user_rows:
        if (row[10] == username):
            yes = False
            break
    return yes


def emailIsOK(email):
    yes = True
    if (email == 'Email'):
        return False
    f = open('databases/userGeneralInfo.csv', 'r')
    csv_reader = reader(f)
    user_rows = list(csv_reader)
    f.close()
    for row in user_rows:
        if (row[3] == email):
            yes = False
            break
    return yes


def verifyUsernameOrEmail(content):
    email_good = emailExists(str(content))
    uname_good = usernameExists(str(content))

    if (email_good):
        return 'e'
    elif (uname_good):
        return 'u'

    return 'n'


def usernameExists(username):
    yes = False
    f = open('databases/userGeneralInfo.csv', 'r')
    csv_reader = reader(f)
    user_rows = list(csv_reader)
    f.close()
    for row in user_rows:
        if (row[10] == username):
            yes = True
            break
    return yes


def emailExists(email):
    yes = False
    f = open('databases/userGeneralInfo.csv', 'r')
    csv_reader = reader(f)
    user_rows = list(csv_reader)
    f.close()
    for row in user_rows:
        if (row[3] == email):
            yes = True
            break
    return yes


def verifyCredentials(username, password):
    okay = False
    f = open('databases/userGeneralInfo.csv', 'r')
    csv_reader = reader(f)
    user_rows = list(csv_reader)
    f.close()
    for row in user_rows:
        if (row[10] == username and row[11] == password):
            okay = True
            break
    return okay


def findActiveUser():
    active_username = None

    f = open('databases/userGeneralInfo.csv', 'r')
    csv_reader = reader(f)
    user_rows = list(csv_reader)
    f.close()

    for row in user_rows:
        if (row[9] == str(True)):
            active_username = row[10]
            break
    return active_username
