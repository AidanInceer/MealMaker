from flask_wtf import FlaskForm
from wtforms.widgets import TextArea
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    IntegerField,
    FileField,
    SelectField,
    FieldList,
    FormField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class IngredientForm(FlaskForm):
    ingredient_name = StringField(validators=[DataRequired()])
    ingredient_amount = IntegerField(validators=[DataRequired()])
    ingredient_unit = SelectField(
        validators=[DataRequired()],
        choices=["g", "kg", "tbsp", "tsp", "item", "oz", "ml", "L"],
    )


class NewMealForm(FlaskForm):
    name = StringField("Meal Name", validators=[DataRequired(), Length(min=1, max=200)])
    portion = IntegerField("No. Portions", validators=[DataRequired()])
    prep_time_hour = IntegerField("Prep Time (Hours):", validators=[DataRequired()])
    prep_time_min = IntegerField("Prep Time (Mins):", validators=[DataRequired()])
    cook_time_hour = IntegerField("Cook Time (Hours):", validators=[DataRequired()])
    cook_time_min = IntegerField("Cook Time (Mins):", validators=[DataRequired()])
    diet_type = SelectField(
        "Dietary Requirements:",
        choices=["None", "Vegetarian", "Vegan"],
        validators=[DataRequired()],
    )
    health_type = SelectField(
        "Healthy:", choices=["Low", "Medium", "High"], validators=[DataRequired()]
    )
    effort = SelectField(
        "Effort:", choices=["Low", "Medium", "High"], validators=[DataRequired()]
    )
    cost = SelectField(
        "Cost:", choices=["Low", "Medium", "High"], validators=[DataRequired()]
    )
    freezable = SelectField(
        "Freezable:", choices=["Yes", "No"], validators=[DataRequired()]
    )
    num_ingredient = IntegerField(
        "Number of Ingredients:", validators=[DataRequired(), NumberRange(min=0)]
    )
    time_to_go_off = IntegerField(
        "Time to go off: ", validators=[DataRequired(), NumberRange(min=0)]
    )
    cal_per_portion = IntegerField(
        "Calories: ", validators=[DataRequired(), NumberRange(min=0)]
    )
    protein_per_portion = IntegerField(
        "Protein: ", validators=[DataRequired(), NumberRange(min=0)]
    )
    fat_per_portion = IntegerField(
        "Fat: ", validators=[DataRequired(), NumberRange(min=0)]
    )
    carb_per_portion = IntegerField(
        "Carbs: ", validators=[DataRequired(), NumberRange(min=0)]
    )
    recipe = StringField("Recipe: ", validators=[DataRequired()], widget=TextArea())
    ingredient = FieldList(FormField(IngredientForm), min_entries=1, max_entries=30)
    submit = SubmitField("Add Meal")


class UpdateMealForm(FlaskForm):
    name = StringField("Meal Name", validators=[DataRequired(), Length(min=1, max=200)])
    portion = IntegerField("No. Portions", validators=[DataRequired()])
    prep_time_hour = IntegerField("Prep Time (Hours):", validators=[DataRequired()])
    prep_time_min = IntegerField("Prep Time (Mins):", validators=[DataRequired()])
    cook_time_hour = IntegerField("Cook Time (Hours):", validators=[DataRequired()])
    cook_time_min = IntegerField("Cook Time (Mins):", validators=[DataRequired()])
    diet_type = SelectField(
        "Dietary Requirements:",
        choices=["None", "Vegetarian", "Vegan"],
        validators=[DataRequired()],
    )
    health_type = SelectField(
        "Healthy:", choices=["Low", "Medium", "High"], validators=[DataRequired()]
    )
    effort = SelectField(
        "Effort:", choices=["Low", "Medium", "High"], validators=[DataRequired()]
    )
    cost = SelectField(
        "Cost:", choices=["Low", "Medium", "High"], validators=[DataRequired()]
    )
    freezable = SelectField(
        "Freezable:", choices=["Yes", "No"], validators=[DataRequired()]
    )
    num_ingredient = IntegerField(
        "Number of Ingredients:", validators=[DataRequired(), NumberRange(min=0)]
    )
    time_to_go_off = IntegerField(
        "Time to go off: ", validators=[DataRequired(), NumberRange(min=0)]
    )
    cal_per_portion = IntegerField(
        "Calories: ", validators=[DataRequired(), NumberRange(min=0)]
    )
    protein_per_portion = IntegerField(
        "Protein: ", validators=[DataRequired(), NumberRange(min=0)]
    )
    fat_per_portion = IntegerField(
        "Fat: ", validators=[DataRequired(), NumberRange(min=0)]
    )
    carb_per_portion = IntegerField(
        "Carbs: ", validators=[DataRequired(), NumberRange(min=0)]
    )
    recipe = StringField("Recipe:", validators=[DataRequired()], widget=TextArea())
    ingredient = FieldList(FormField(IngredientForm), min_entries=1, max_entries=30)
    submit = SubmitField("Update Meal")
