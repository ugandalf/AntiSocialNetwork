#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, validators


class MessageForm(FlaskForm):
    message = TextAreaField('', [validators.DataRequired()])
    submit = SubmitField('Submit')
