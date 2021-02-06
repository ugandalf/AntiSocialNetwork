#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class TagForm(FlaskForm):
    tag = StringField('Tag Name', [validators.DataRequired()])
    submit = SubmitField('Add Tag')
