import random

from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms.validators import Length, Optional


class CharacterForm(FlaskForm):
    game_system = SelectField(
        "Game system",
        validators=[],
        choices=[
            ("Pathfinder 2e"),
        ],
        default="Pathfinder 2e",
        render_kw={"disabled": ""},
    )
    hints = TextAreaField(
        "Hints",
        validators=[Optional(), Length(max=200)],
        description=(
            "Character's personality traits, ideals, bonds, and flaws. "
            "These are used to generate the character's background and name."
        ),
    )
    alignment_id = SelectField(
        "Alignment",
        validators=[],
    )
    template_id = SelectField(
        "Template",
        validators=[Optional()],
        description=(
            "Template determines the character's level and stats "
            "distribution, as well as the items and skills they have."
        ),
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
