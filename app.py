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

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['CKEDITOR_PKG_TYPE'] = 'full-all'
ckeditor = CKEditor(app)
Bootstrap(app)


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
    return render_template("generic.html")


@app.route('/elements')
def elements():
    return render_template("elements.html")

if __name__ == "__main__":
    app.run(debug=True)