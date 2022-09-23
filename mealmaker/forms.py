from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    IntegerField,
    FileField,
    SelectField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class NewMealForm(FlaskForm):
    name = StringField("Meal Name", validators=[DataRequired(), Length(min=1, max=200)])
    portion = IntegerField("No. Portions", validators=[DataRequired()])
    prep_time_hour = IntegerField(
        "Prep Time (Hours):", validators=[DataRequired(), NumberRange(min=0, max=24)]
    )
    prep_time_min = IntegerField(
        "Prep Time (Mins):", validators=[DataRequired(), NumberRange(min=0, max=60)]
    )
    cook_time_hour = IntegerField(
        "Cook Time (Hours):", validators=[DataRequired(), NumberRange(min=0, max=24)]
    )
    cook_time_min = IntegerField(
        "Cook Time (Mins):", validators=[DataRequired(), NumberRange(min=0, max=60)]
    )
    diet_type = SelectField(
        "Dietary Requirements:",
        choices=[(0,"None"), (1,"Vegetarian"), (2,"Vegan")],
        validators=[DataRequired()],
    )
    health_type = SelectField(
        "Healthy:", choices=[(0,"Low"), (1,"Medium"), (2,"High")], validators=[DataRequired()]
    )
    effort = SelectField(
        "Effort:", choices=[(0,"Low"), (1,"Medium"), (2,"High")], validators=[DataRequired()]
    )
    cost = SelectField(
        "Cost:", choices=[(0,"Low"), (1,"Medium"), (2,"High")], validators=[DataRequired()]
    )
    freezable = SelectField(
        "Freezable:", choices=[(0,"Yes"), (1,"No")], validators=[DataRequired()]
    )
    num_ingredient = IntegerField(
        "Number of Ingredients:", validators=[DataRequired(), NumberRange(min=0)]
    )
    time_to_go_off = IntegerField(
        "Time to go off: ", validators=[DataRequired(), NumberRange(min=0)]
    )
    recipe = StringField("Recipe:", validators=[DataRequired()])
    submit = SubmitField("Add Meal")
