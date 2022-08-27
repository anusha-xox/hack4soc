from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap
from flask_wtf.file import FileField, FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=2)])
    submit = SubmitField(label='Login')


class StudentForm(FlaskForm):
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField(label='Last Name', validators=[DataRequired()])
    grade=StringField(label='Grade' ,validators=[DataRequired()])
    age=StringField(label='Age', validators=[DataRequired()])
    level_assigned=StringField(label='Level', validators=[DataRequired()])
    img_url=StringField(label='Img Url', validators=[DataRequired()])
    total_points=StringField(label='Total Points', validators=[DataRequired()])
    badge=StringField(label='Badge', validators=[DataRequired()])
    no_of_writeups=StringField(label='No of Writeups', validators=[DataRequired()])
    current_book=StringField(label='Current Book Borrowed', validators=[DataRequired()])
    past_books=StringField(label='Past books', validators=[DataRequired()])
    volunteer_email=StringField(label='Volunteer Email', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class Question(FlaskForm):

    q1=StringField(label="Sample Question 1", validators=[DataRequired()])
    q2 = StringField(label="Sample Question 2", validators=[DataRequired()])
    q3 = StringField(label="Sample Question 3", validators=[DataRequired()])
    q4 = StringField(label="Sample Question 4", validators=[DataRequired()])
    q5 = StringField(label="Sample Question 5", validators=[DataRequired()])
    submit = SubmitField(label='Login')

class Evaluate(FlaskForm):
    name=StringField(label="What is your name?", validators=[DataRequired()])
    grade= StringField(label="Which grade are you in?", validators=[DataRequired()])
    level = StringField(label="Which level are you in?", validators=[DataRequired()])
    subject= StringField(label="Which subject do you want to take up the assessment for?", validators=[DataRequired()])

    submit = SubmitField(label='Login')

