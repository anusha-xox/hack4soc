from flask import Flask, render_template, redirect, url_for, request, Response
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
        success, frame=camera.read()
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


            ret, buffer=cv2.imencode(".jpg", frame)
            frame=buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/', methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        if login_form.username.data == 'admin' and login_form.password.data == 'ab':
            return render_template('index1.html')

    return render_template('login.html', form=login_form)


@app.route('/home')
def home():
    return render_template("index1.html")


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
    return render_template("view_students.html")


@app.route('/barcode_reader')
def barcode_reader():

    return render_template('barcode.html')


@app.route('/display_barcode')
def display_barcode():
    return render_template('display_barcode.html', type1=type_barcode, data1=data_barcode)


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
