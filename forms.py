from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectMultipleField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, DataRequired, EqualTo, Length
from Genre import Genre
from registerAndLogin import usernameIsOK, verifyCredentials
genres = [
    ('pop', Genre.POP), ('electronic',
                         Genre.ELECTRONIC), ('dance', Genre.DANCE), ('rap', Genre.RAP),
    ('hiphop', Genre.HIPHOP), ('rock', Genre.ROCK), ('metal',
                                                     Genre.METAL), ('soul', Genre.SOUL),
    ('jazz', Genre.JAZZ), ('disco', Genre.DISCO), ('funk',
                                                   Genre.FUNK), ('classical', Genre.CLASSICAL),
    ('soundtrack', Genre.SOUNDTRACK), ('world',
                                       Genre.WORLD), ('folk', Genre.FOLK), ('indie', Genre.INDIE),
    ('broadway', Genre.BROADWAY), ('theater', Genre.BROADWAY), ('musical',
                                                                Genre.MUSICAL), ('vintage', Genre.VINTAGE),
    ('ballad', Genre.BALLAD), ('meditation',
                               Genre.MEDITATION), ('faith', Genre.FAITH)
]


class RegisterForm(FlaskForm):
    firstName = StringField('Your First Name', validators=[DataRequired()])
    lastName = StringField('Your Last Name', validators=[DataRequired()])
    email = EmailField('Your Email', validators=[DataRequired(), Email()])
    dateOfBirth = DateField('Your Birthday', validators=[DataRequired()])

    location = StringField(
        'Your Location', validators=[DataRequired()])

    favoriteGenres = SelectMultipleField(
        'Your Favorite Genres', choices=genres)

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


class LogoutButton(FlaskForm):
    logout = SubmitField('Logout')


class RegisterButton(FlaskForm):
    register = SubmitField('Register')


class LoginButton(FlaskForm):
    login = SubmitField('Login to Existing Account')
