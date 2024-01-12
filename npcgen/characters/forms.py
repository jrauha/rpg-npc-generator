import random

from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms.validators import Optional


class CharacterForm(FlaskForm):
    hints = TextAreaField("Hints", validators=[Optional()])

    alignment_id = SelectField(
        "Alignment",
        validators=[],
    )
    template_id = SelectField(
        "Template",
        validators=[Optional()],
    )
    class_id = SelectField(
        "Class",
        validators=[Optional()],
    )
    race_id = SelectField(
        "Race",
        validators=[Optional()],
    )

    def get_choice_or_random(self, field):
        choices = field.choices[1:]  # Exclude the first element
        return field.data or random.choice(choices)[0]
