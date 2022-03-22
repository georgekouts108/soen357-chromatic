from flask import Flask, render_template
from csv import reader, writer
import sys
import os
from User import User, setLatestNumberOfUsers
from Genre import Genre

app = Flask(__name__)


@app.route('/')
def main_page():

    setLatestNumberOfUsers()

    myUser = User('George', 'Koutsaris', 23, 'mtl',
                  None, 'georgey', 'myPwd', False)
    myUser2 = User('Mike', 'Manou', 25, 'roc',
                   None, 'miko', 'myPwd3', False)

    myUser.writeGeneralInfoData()
    myUser.writeCredentialsData()
    myUser2.writeGeneralInfoData()
    myUser2.writeCredentialsData()

    myUser2.changePassword("MICHAELLLLLLLLL")
    return render_template("home.html")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
