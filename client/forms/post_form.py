#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField, TextAreaField, validators

from flask_init import TagList

class PostForm(FlaskForm):
    title = StringField('Title', [validators.DataRequired()])
    contents = TextAreaField('Contents', [validators.DataRequired()])
    # can be improved using library "chosen" for jquery
    tags = SelectMultipleField('Tags (to select multiple use ctrl)', choices = [], coerce = int)
    submit = SubmitField('Create Post')

    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()

        # Update the choices for the agency field
        form.tags.choices = TagList.query.with_entities(TagList.tag_id, TagList.tag).order_by(TagList.tag).all()
        return form
