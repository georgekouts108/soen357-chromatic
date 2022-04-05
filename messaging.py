from csv import reader
import os


def getYourUsername():
    uname = None
    h = open('databases/userGeneralInfo.csv', 'r')
    csv_reader3 = reader(h)
    user_rows = list(csv_reader3)
    h.close()
    for row in user_rows[1::]:
        if (str(row[9]) == str(True)):
            uname = row[10]
            break
    print("uname == "+str(uname))
    return uname


def getInfoForFriends(yourUsername):
    yourFriendsInfo = []
    h = open('databases/userGeneralInfo.csv', 'r')
    csv_reader3 = reader(h)
    user_rows = list(csv_reader3)
    h.close()

    yourID = 0
    for row in user_rows[1::]:
        if (row[10] == yourUsername):
            yourID = int(row[0])
            break

    i = open('databases/userFriends.csv', 'r')
    csv_reader4 = reader(i)
    user_rows2 = list(csv_reader4)
    i.close()
    # a list of your friends' usernames

    if (len(user_rows2) > 1):
        friendsUsernames = user_rows2[yourID][1::]
        for username in friendsUsernames:
            for u in user_rows[1::]:
                if (u[10] == username):
                    newInfoEntry = [str(u[0]), str(
                        u[1])+" "+str(u[2]), str(u[10])]
                    yourFriendsInfo.append(newInfoEntry)
                    break
    print("yourFriendsInfo == "+str(yourFriendsInfo))
    return yourFriendsInfo


def removeEmptyChatFiles():
    listOfChatFiles = os.listdir("chats/")
    for filename in listOfChatFiles:
        ChatLogRead = open('chats/' + filename, 'r')
        csv_reader = reader(ChatLogRead)
        log_rows = list(csv_reader)
        ChatLogRead.close()
        if len(log_rows) == 1:
            os.remove("chats/"+filename)
