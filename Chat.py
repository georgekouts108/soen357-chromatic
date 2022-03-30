from Genre import Genre
from csv import reader, writer
from csvEditing import updatePassword, updateGenres, getGenreDB, getGeneralInfoDB
import csv
import os
from datetime import datetime

NEXT_CHAT_ID = 1
NUM_OF_ACTIVE_CHATS = 0


def getChatCount():
    return NUM_OF_ACTIVE_CHATS


def setLatestNumberOfChatsAndIDs():

    listOfChatFiles = os.listdir("chats/")
    chatCount = len(listOfChatFiles)
    print("THE NUMBER OF ACTIVE CHATS == "+str(chatCount))

    global NUM_OF_ACTIVE_CHATS
    NUM_OF_ACTIVE_CHATS = int(chatCount)

    global NEXT_CHAT_ID
    NEXT_CHAT_ID = NUM_OF_ACTIVE_CHATS + 1

    return NUM_OF_ACTIVE_CHATS


def getNextChatID():
    return NEXT_CHAT_ID


def updateNextChatID():
    global NEXT_CHAT_ID
    NEXT_CHAT_ID = NEXT_CHAT_ID + 1


def updateNumOfActiveChats():
    global NUM_OF_ACTIVE_CHATS
    NUM_OF_ACTIVE_CHATS = NUM_OF_ACTIVE_CHATS + 1


class Chat:
    def __init__(self, members, firstUsername, firstUserID, firstFullName, firstMessage=None, manualChatID=0, isNewChat=True):

        self.firstusername = firstUsername
        self.firstuserID = firstUserID
        self.firstfullname = firstFullName

        # a list of the format: [member's user ID, member's full name, member's username]
        self.members = members

        # the first message that was sent whcih originally started the chat
        self.firstMessage = firstMessage

        if (isNewChat is True):
            self.id = getNextChatID()
            updateNextChatID()
            updateNumOfActiveChats()
            setLatestNumberOfChatsAndIDs()
        else:
            self.id = manualChatID

        participantIDs = []
        for m in members:
            participantIDs.append(str(m[0]))

        self.log_file_name = "chat" + \
            str(self.id)+"_"+'_'.join(participantIDs)+"_"
        self.createAndStartChatLogFile()

    def createAndStartChatLogFile(self):
        newChatLogWrite = open(
            'chats/' + str(self.log_file_name) + '.csv', 'w', newline='')
        csv_writer = writer(newChatLogWrite)
        # write the header row
        csv_writer.writerow(
            ["Sender ID", "Sender Username", "Sender Name", "Message"])

        csv_writer.writerow([str(self.firstuserID), str(self.firstusername), str(
            self.firstfullname), self.firstMessage])
        newChatLogWrite.close()
        return True

    def retrieveChatLog(self):
        ChatLogRead = open('chats/' + str(self.log_file_name) + '.csv', 'r')
        csv_reader = reader(ChatLogRead)
        log_rows = list(csv_reader)
        ChatLogRead.close()
        return log_rows[1::]

    def appendMessageToChat(self, senderUserID, senderUsername, senderName, message):
        ChatLogWrite = open('chats/' + str(self.log_file_name) +
                            '.csv', 'a', newline='')
        csv_writer = writer(ChatLogWrite)

        csv_writer.writerow([str(senderUserID), str(
            senderUsername), str(senderName), str(message)])
        ChatLogWrite.close()
        return True
