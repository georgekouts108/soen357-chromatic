from flask import Flask, render_template
from csv import reader, writer
import sys
import os
from User import User, setLatestNumberOfUsersAndIDs, getNextUserID, getUserCount
from Genre import Genre

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_page():

    setLatestNumberOfUsersAndIDs()

    myUser = User('George', 'Koutsaris', 5, 9, 1998,
                  23, 'mtl', None, 'georgey', 'myPwd')
    myUser2 = User('Mike', 'Manou', 4, 3, 1996, 25,
                   'roc', None, 'miko', 'myPwd3')

    # myUser.addGenre(Genre.CLASSICAL)
    # myUser.addGenre(Genre.JAZZ)
    # myUser.addGenre(Genre.ELECTRONIC)

    # myUser2.addGenre(Genre.HIPHOP)
    # myUser2.addGenre(Genre.MEDITATION)
    # myUser2.addGenre(Genre.FUNK)

    # myUser2.deleteGenre(Genre.MEDITATION)

    return render_template("home.html", userCount=getUserCount())


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
