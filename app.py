from flask import Flask, render_template, redirect, url_for, request, Response
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime
from flask_sqlalchemy import SQLAlchemy
import bleach
import smtplib
from login import LoginForm, StudentForm,  Evaluate
from pyzbar import pyzbar
import cv2
from sqlalchemy import Column, Integer, String


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['CKEDITOR_PKG_TYPE'] = 'full-all'
ckeditor = CKEditor(app)
Bootstrap(app)
global type_barcode
global data_barcode




def draw_barcode(decoded, image):
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top),
                          (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                          color=(0, 255, 0),
                          thickness=5)
    return image


def gen():
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            decoded_objects = pyzbar.decode(frame)
            for obj in decoded_objects:
                # draw the barcode
                print("detected barcode:", obj)
                image = draw_barcode(obj, frame)
                global data_barcode
                global type_barcode
                type_barcode = obj.type
                data_barcode = obj.data

                # print barcode type & data
                print("Type:", obj.type)
                print("Data:", obj.data)
                print()

            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


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

#
# class Progress(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(250), unique=True, nullable=False)  # string
#     last_name = db.Column(db.String(250), nullable=False)  # string



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

    # books=
    return render_template('books.html', )


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


@app.route('/barcode_reader')
def barcode_reader():
    return render_template('barcode.html')


@app.route('/evaluate', methods=["GET", "POST"])
def evaluate():
    evaluate_form = Evaluate()

    if evaluate_form.validate_on_submit():
        global student_answer
        student_answer= evaluate_form.answer.data
        return render_template('index.html')

    return render_template('evaluate.html', form=evaluate_form)


# @app.route('/questions', methods=["GET", "POST"])
# def questions():
#     question_form = Question()
#
#     if question_form.validate_on_submit():
#         global student_answer
#         student_answer= question_form.answer.data
#         return render_template('index.html')
#
#     return render_template('questions.html', form=question_form)


@app.route('/display_barcode')
def display_barcode():
    return render_template('display_barcode.html', type1=type_barcode, data1=data_barcode)


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/add_student')
def add_student():
    return render_template('add_student.html')


@app.route('/individual-student/<int:index>', methods=["GET", "POST"])
def individual_students(index):
    view_student = Students.query.get(index)
    if view_student:
        return render_template("individual_student.html", student=view_student)
    else:
        return redirect(url_for('view_students'))


if __name__ == "__main__":
    app.run(debug=True)


