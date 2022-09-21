from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class NewMealForm(FlaskForm):
    name = StringField('Meal Name',
                       validators=[DataRequired(), Length(min=1, max=200)])
    portion = IntegerField('No. Portions', validators=[DataRequired()])
    submit = SubmitField('Add Meal')
