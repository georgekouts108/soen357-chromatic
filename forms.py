from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectMultipleField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, DataRequired, EqualTo, Length
from Genre import Genre
from registerAndLogin import usernameIsOK, verifyCredentials
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
        'Your Top Favorite Genre (you can add more later)', choices=genres)

    username = StringField('Username', validators=[
                           DataRequired(), Length(min=8, max=15)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8, max=15)])
    confirm_pwd = PasswordField('Confirm Password', validators=[
                                DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Account', validators=[
                         usernameIsOK(username)])


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8, max=15)])
    login = SubmitField('Login', validators=[
                        verifyCredentials(username, password)])


class HomePageButtons(FlaskForm):
    genreManage = SubmitField('Manage Favorite Genres')
    logout = SubmitField('Logout')


class RegisterButton(FlaskForm):
    register = SubmitField('Register')


class LoginButton(FlaskForm):
    login = SubmitField('Login to Existing Account')


class GenreManageControls(FlaskForm):
    favoriteGenres = SelectMultipleField(
        'Select one or more genres, click on \"Add Genre(s)\" or \"Delete Genre(s)\", and then Confirm', choices=genres)
    home = SubmitField('Home')
