#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, SelectField, SubmitField, validators

class RegistrationForm(FlaskForm):
    email = StringField('Email Address', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    name = StringField('Name', [
        validators.DataRequired(),
        validators.Length(max=255)
    ])
    birthday = DateField('Birthday (in day/month/year format)', [validators.DataRequired()], format="%d/%m/%Y")
    gender = StringField('Gender', [
        validators.DataRequired(),
        validators.Length(max=32)
    ])
    country = SelectField('Country', choices=['Polska', 'Niemcy'])
    submit = SubmitField('Sign-Up')
