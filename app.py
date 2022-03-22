from flask import Flask, render_template
from csv import reader, writer
import sys
import os
from User import User
from Genre import Genre

app = Flask(__name__)


@app.route('/')
def main_page():
    myUser = User(15, 'George', 'Koutsaris', 23, 'mtl',
                  None, 'myUserName12', 'myPwd', False)
    myUser.addGenre(Genre.JAZZ)
    myUser.addGenre(Genre.CLASSICAL)
    myUser.writeFavGenresData()

    myUser.writeGeneralInfoData()
    myUser.writeCredentialsData()

    return render_template("home.html")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
