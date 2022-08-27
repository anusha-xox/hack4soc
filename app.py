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
from form_data import LoginForm, StudentForm, Evaluate
from pyzbar import pyzbar
import cv2
from sqlalchemy import Column, Integer, String
from nlp import solve

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


class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    grade = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String, nullable=False)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'{self.id}'

    def add_new(self, student_id, name, grade, level, subject, question, answer):
        new_eval = Evaluation(student_id=student_id, name=name, grade=grade,
                              level=level, subject=subject, question=question, answer=answer)

        db.session.add(new_eval)
        db.session.commit()


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
        student_answer = evaluate_form.answer.data
        global ret
        ret = solve(student_answer, "Hardcoded text")
        name = evaluate_form.name.data
        grade = evaluate_form.grade.data
        level = evaluate_form.level.data
        student_id = evaluate_form.student_id.data
        question = evaluate_form.question.data
        answer = evaluate_form.answer.data
        subject = evaluate_form.subject.data

        e = Evaluation()
        e.add_new(student_id, name, grade, level, subject, question, answer)

        return render_template('test_result.html', result=ret)

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


@app.route('/add_student', methods=["GET", "POST"])
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        new_student = Students(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            grade=form.grade.data,
            age=form.age.data,
            level_assigned=form.level_assigned.data,
            img_url=form.img_url.data,
            total_points=form.total_points.data,
            badge=form.badge.data,
            no_of_writeups=form.no_of_writeups.data,
            current_book=form.current_book.data,
            past_books=form.past_books.data,
            volunteer_email=form.volunteer_email.data
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('view_students'))
    return render_template('add_student.html', heading="Add Student", form=form)


@app.route('/edit-student/<int:index>', methods=["GET", "POST"])
def edit_student(index):
    student_found = Students.query.get(index)
    if student_found:
        edit_form = StudentForm(
            first_name=student_found.first_name,
            last_name=student_found.last_name,
            grade=student_found.grade,
            age=student_found.age,
            level_assigned=student_found.level_assigned,
            img_url=student_found.img_url,
            total_points=student_found.total_points,
            badge=student_found.badge,
            no_of_writeups=student_found.no_of_writeups,
            current_book=student_found.current_book,
            past_books=student_found.past_books,
            volunteer_email=student_found.volunteer_email
        )
        if edit_form.validate_on_submit():
            student_found.first_name = edit_form.first_name.data
            student_found.last_name = edit_form.last_name.data
            student_found.grade = edit_form.grade.data
            student_found.age = edit_form.age.data
            student_found.level_assigned = edit_form.level_assigned.data
            student_found.img_url = edit_form.img_url.data
            student_found.total_points = edit_form.total_points.data
            student_found.badge = edit_form.badge.data
            student_found.no_of_writeups = edit_form.no_of_writeups.data
            student_found.current_book = edit_form.current_book.data
            student_found.past_books = edit_form.past_books.data
            student_found.volunteer_email = edit_form.volunteer_email.data
            db.session.commit()
            return redirect(url_for('view_students'))
        return render_template('add_student.html', heading="Edit Student", form=edit_form)


@app.route('/individual-student/<int:index>', methods=["GET", "POST"])
def individual_students(index):
    view_student = Students.query.get(index)
    if view_student:
        return render_template("individual_student.html", student=view_student)
    else:
        return redirect(url_for('view_students'))


if __name__ == "__main__":
    app.run(debug=True)

