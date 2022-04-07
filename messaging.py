from csv import reader, writer
from genericpath import exists
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
            removed_chat_id = int(filename.split('_')[0][4::])
            deleteChatFromURrecords(removed_chat_id)

## NEW - notifications


def initUnreadMessagesCSVFile(currentUserCount):

    if not exists('databases/unreadMessages.csv'):
        newCSVFile = open('databases/unreadMessages.csv', 'w', newline='')
        csv_writer = writer(newCSVFile)
        # write the header row
        csv_writer.writerow(["UserID", "TotalUnread"])
        for u in range(currentUserCount):
            csv_writer.writerow([u+1, 0])
        newCSVFile.close()
    else:
        csvfile = open('databases/unreadMessages.csv', 'r')
        csv_reader = reader(csvfile)
        rows = list(csv_reader)
        csvfile.close()

        #####
        listOfChatFiles = os.listdir("chats/")
        for filename in listOfChatFiles:
            next_chat_id = int(filename.split('_')[0][4::])
            id_exists = False
            for i in rows[0][2::]:
                if int(i[4::]) == next_chat_id:
                    id_exists = True
                    break
            if not id_exists:
                rows[0].append("Chat"+str(next_chat_id))
                for r in rows[1::]:
                    r.append(0)

        csvfileWrite = open('databases/unreadMessages.csv', 'w', newline='')
        csv_writer = writer(csvfileWrite)
        csv_writer.writerows(rows)
        csvfileWrite.close()
    return None


def deleteNonexistingChatsFromURrecords():
    csvfile = open('databases/unreadMessages.csv', 'r')
    csv_reader = reader(csvfile)
    rows = list(csv_reader)
    csvfile.close()

    for r in rows[0][2::]:
        temp_header = str(r)
        temp_chat_id = r[4::]
        listOfChatFiles = os.listdir("chats/")
        chat_id_exists = False

        for filename in listOfChatFiles:
            if "C"+filename.split('_')[0][1::] == temp_header:
                chat_id_exists = True
                break

        if not chat_id_exists:
            deleteChatFromURrecords(int(temp_chat_id))
    return True


def deleteChatFromURrecords(chatID):
    csvfile = open('databases/unreadMessages.csv', 'r')
    csv_reader = reader(csvfile)
    rows = list(csv_reader)
    csvfile.close()

    deleted_chat_index = 0
    for header in rows[0]:
        if header == 'Chat'+str(chatID):
            break
        else:
            deleted_chat_index = deleted_chat_index + 1

    updated_rows = []
    for r in rows:
        temp_new_row = []
        for i in range(len(r)):
            if (i != deleted_chat_index):
                temp_new_row.append(r[i])
        updated_rows.append(temp_new_row)
    csvfileWrite = open('databases/unreadMessages.csv', 'w', newline='')
    csv_writer = writer(csvfileWrite)
    csv_writer.writerows(updated_rows)
    csvfileWrite.close()
    return True


def updateUnreadMessageCountForSpecificChat(chatID, userID, new_ur_count):
    csvfile = open('databases/unreadMessages.csv', 'r')
    csv_reader = reader(csvfile)
    rows = list(csv_reader)
    csvfile.close()
    column_index = 0
    for header in rows[0]:
        if header == ('Chat'+str(chatID)):
            break
        else:
            column_index = column_index + 1
    for r in rows[1::]:
        if str(r[0]) == str(userID):
            r[column_index] = new_ur_count
            break
    csvfileWrite = open('databases/unreadMessages.csv', 'w', newline='')
    csv_writer = writer(csvfileWrite)
    csv_writer.writerows(rows)
    csvfileWrite.close()
    return True


def updateTotalUnreadMessageCount(userID, new_total_ur_count):
    csvfile = open('databases/unreadMessages.csv', 'r')
    csv_reader = reader(csvfile)
    rows = list(csv_reader)
    csvfile.close()
    for r in rows[1::]:
        if r[0] == str(userID):
            r[1] = new_total_ur_count
            break
    csvfileWrite = open('databases/unreadMessages.csv', 'w', newline='')
    csv_writer = writer(csvfileWrite)
    csv_writer.writerows(rows)
    csvfileWrite.close()
    return True


def retrieveUnreadMessageCountForSpecificChat(chatID, userID):
    unread_count = 0
    csvfile = open('databases/unreadMessages.csv', 'r')
    csv_reader = reader(csvfile)
    rows = list(csv_reader)
    csvfile.close()
    column_index = 0
    for header in rows[0]:
        if header == ('Chat'+str(chatID)):
            break
        else:
            column_index = column_index + 1
    for r in rows[1::]:
        if str(r[0]) == str(userID):
            unread_count = int(r[column_index])
            break
    return unread_count


def getIndividualChatUnreadMessageCountsForSpecificUser(userID):
    counts = []

    listOfChatFiles = os.listdir("chats/")
    for filename in listOfChatFiles:
        next_chat_id = int(filename.split('_')[0][4::])
        i_am_member = False

        for u_id in filename.split('_')[1:(len(filename.split('_'))-1)]:
            if u_id == str(userID):
                i_am_member = True
                break
        if i_am_member:
            x = retrieveUnreadMessageCountForSpecificChat(next_chat_id, userID)
            print("COUNTS == "+str(x))
            counts.append(x)
        else:
            counts.append(0)

    return counts


def retrieveTotalUnreadMessageCount(userID):
    total_count = 0
    csvfile = open('databases/unreadMessages.csv', 'r')
    csv_reader = reader(csvfile)
    rows = list(csv_reader)
    csvfile.close()
    for r in rows[1::]:
        if r[0] == str(userID):
            total_count = int(r[1])
            break
    return total_count
