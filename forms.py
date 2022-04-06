from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectMultipleField, TextAreaField, HiddenField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, DataRequired, EqualTo, Length
from Genre import Genre
from registerAndLogin import usernameIsOK, verifyCredentials
from messaging import getInfoForFriends, getYourUsername

genres = [
    ('POP', Genre.POP), ('ELECTRONIC',
                         Genre.ELECTRONIC), ('DANCE', Genre.DANCE), ('RAP', Genre.RAP),
    ('HIPHOP', Genre.HIPHOP), ('ROCK', Genre.ROCK), ('METAL',
                                                     Genre.METAL), ('SOUL', Genre.SOUL),
    ('JAZZ', Genre.JAZZ), ('DISCO', Genre.DISCO), ('FUNK',
                                                   Genre.FUNK), ('CLASSICAL', Genre.CLASSICAL),
    ('SOUNDTRACK', Genre.SOUNDTRACK), ('WORLD',
                                       Genre.WORLD), ('FOLK', Genre.FOLK), ('INDIE', Genre.INDIE),
    ('BROADWAY', Genre.BROADWAY), ('THEATER', Genre.BROADWAY), ('MUSICAL',
                                                                Genre.MUSICAL), ('VINTAGE', Genre.VINTAGE),
    ('BALLAD', Genre.BALLAD), ('MEDITATION',
                               Genre.MEDITATION), ('FAITH', Genre.FAITH)
]


class RegisterForm(FlaskForm):
    firstName = StringField('Your First Name', validators=[DataRequired()])
    lastName = StringField('Your Last Name', validators=[DataRequired()])
    email = EmailField('Your Email', validators=[DataRequired(), Email()])
    dateOfBirth = DateField('Your Birthday', validators=[DataRequired()])

    location = StringField(
        'Your Location', validators=[DataRequired()])

    favoriteGenres = SelectMultipleField(
        'Select genres that you like (you can change your selection later if you wish)', choices=genres)

    username = StringField('Username', validators=[
                           DataRequired(), Length(min=8, max=15)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8, max=15)])
    confirm_pwd = PasswordField('Confirm Password', validators=[
                                DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Account', validators=[
                         usernameIsOK(username)])


class SettingsForm(FlaskForm):

    new_firstName = StringField(
        'If you want to change your display First name, enter a new one here:')
    new_lastName = StringField(
        'If you want to change your display Last name, enter a new one here:')

    new_username = StringField(
        'If you want to change your username, enter a new one here:', validators=[Length(min=8, max=15)])
    new_email = EmailField(
        'If you want to change your email, enter a new one here:')
    new_location = StringField(
        'If you want to change your location, enter a new one here:')

    # gender and pronoun setting will be written in HTML directly

    submit = SubmitField('Confirm Changes')


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8, max=15)])
    login = SubmitField('Login', validators=[
                        verifyCredentials(username, password)])

    forgotPwd = SubmitField('Forgot Password')


class ForgotPasswordForm(FlaskForm):
    identity = StringField('Username or Email', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(), Length(min=8, max=15)])
    confirm = SubmitField('Confirm')


class HomePageButtons(FlaskForm):
    genreManage = SubmitField('Manage Favorite Genres')
    findFriends = SubmitField('Find Friends')
    connections = SubmitField('See Friend Suggestions')
    myFriends = SubmitField('My Friends')
    myMessages = SubmitField('My Messages')
    logout = SubmitField('Logout')


class RegisterButton(FlaskForm):
    register = SubmitField('Register')


class LoginButton(FlaskForm):
    login = SubmitField('Login to Existing Account')


class HomeButton(FlaskForm):
    home = SubmitField('Home')


class GenreManageControls(FlaskForm):
    favoriteGenres = SelectMultipleField(
        'Select one or more genres, click on \"Add Genre(s)\" or \"Delete Genre(s)\", and then Confirm', choices=genres)
    home = SubmitField('Home')


class MessagesPageButtons(FlaskForm):
    startNewChat = SubmitField("Start New Chat")
    home = SubmitField('Home')


class NewChatForm(FlaskForm):

    friendsInfo = getInfoForFriends(getYourUsername())

    friends = []
    for f in friendsInfo:
        friends.append((f[2], f[1]))

    recipientOptions = SelectMultipleField(
        'Select one or more friends to create a chat with:', choices=friends)

    newMessage = TextAreaField(
        "Write something...", validators=[DataRequired()])
    send = SubmitField("Send Message")
    cancel = SubmitField('Cancel')


class ChatViewForm(FlaskForm):
    newMessage = TextAreaField(
        "Write something...", validators=[DataRequired()])
    send = SubmitField("Send")
