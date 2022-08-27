from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime
import bleach
import smtplib
from login import LoginForm
from pyzbar import pyzbar
import cv2
from barcode import Barcode

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['CKEDITOR_PKG_TYPE'] = 'full-all'
ckeditor = CKEditor(app)
Bootstrap(app)

#### DATABASE FOR STUDENTS ON SQLALCHEMY ####

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), unique=True, nullable=False)  # string
    last_name = db.Column(db.String(250), nullable=False)  # string
    grade = db.Column(db.String(500), nullable=False)  # string
    age = db.Column(db.Integer, nullable=True)  # integer
    level_assigned = db.Column(db.String(50), nullable=True)  # string
    img_url = db.Column(db.String(250), nullable=True)
    total_points = db.Column(db.Integer, nullable=True)
    badge = db.Column(db.String, nullable=True)
    no_of_writeups = db.Column(db.Integer, nullable=True)
    current_book = db.Column(db.String(2500), nullable=True)
    past_books = db.Column(db.String(2500), nullable=True)
    volunteer_email = db.Column(db.String(250), nullable=False)


# db.create_all()

# new_student = Students(
#     first_name="B.",
#     last_name="Kumar",
#     grade="4",
#     age=9,
#     level_assigned="B1",
#     img_url="static/images/kumar.jpg",
#     total_points=19,
#     badge="Signed Up Badge, Completion Badge",
#     no_of_writeups=2,
#     current_book="0936342795948",
#     past_books="1234657354694, 3432732465974",
#     volunteer_email="anushajain.bang@yahoo.com"
# )
# db.session.add(new_student)
# db.session.commit()

#### END OF DATABASE STUFF ####


@app.route('/', methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        if login_form.username.data == 'admin' and login_form.password.data == 'ab':
            return render_template('index.html')

    return render_template('login.html', form=login_form)


@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/generic')
def generic():
    return render_template("about.html")


@app.route('/elements')
def elements():
    return render_template("elements.html")


@app.route('/books')
def books():
    return render_template('books.html')


@app.route('/level1')
def level1():
    return render_template('level1.html')


@app.route('/level2')
def level2():
    return render_template('level2.html')


@app.route('/level3')
def level3():
    return render_template('level3.html')


@app.route('/view-students')
def view_students():
    all_students = Students.query.all()
    return render_template("view_students.html", all_students=all_students)


@app.route('/barcode-reader')
def barcode_reader():
    b = Barcode()
    b.initiate()


@app.route('/individual-student/<int:index>', methods=["GET", "POST"])
def individual_students(index):
    view_student = Students.query.get(index)
    if view_student:
        return render_template("individual_student.html", student=view_student)
    else:
        return redirect(url_for('view_students'))


if __name__ == "__main__":
    app.run(debug=True)
