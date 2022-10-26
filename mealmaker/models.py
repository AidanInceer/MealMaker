import pandas as pd
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    name = db.Column(db.String(200), unique=True)
    portion = db.Column(db.Integer)
    prep_time_hour = db.Column(db.Integer)
    prep_time_min = db.Column(db.Integer)
    cook_time_hour = db.Column(db.Integer)
    cook_time_min = db.Column(db.Integer)
    diet_type = db.Column(db.String(20))
    health_type = db.Column(db.String(20))
    effort = db.Column(db.String(5))
    cost = db.Column(db.String(5))
    freezable = db.Column(db.String(5))
    num_ingredient = db.Column(db.Integer)
    time_to_go_off = db.Column(db.Integer)
    cal_per_portion = db.Column(db.Integer)
    protein_per_portion = db.Column(db.Integer)
    fat_per_portion = db.Column(db.Integer)
    carb_per_portion = db.Column(db.Integer)
    recipe = db.Column(db.Text)
    ingredients = db.relationship(
        "Ingredient", back_populates="meal_id", cascade="all, delete"
    )
    meal_plan = db.relationship("MealPlan", back_populates="meal_id")


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    amount = db.Column(db.Integer)
    unit = db.Column(db.String(200))
    meal_link = db.Column(db.Integer, db.ForeignKey("meal.id"))
    meal_id = db.relationship(
        "Meal", back_populates="ingredients", collection_class=list
    )


class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String(200))
    username = db.Column(db.String(200))
    meal_link = db.Column(db.Integer, db.ForeignKey("meal.id"))
    meal_id = db.relationship("Meal")
    meal_store = db.relationship("MealStore", back_populates="meal_plan_id")


class MealStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stored_mealname = db.Column(db.String(200))
    portion = db.Column(db.Integer)
    freezable = db.Column(db.String(5))
    time_to_go_off = db.Column(db.Integer)
    username = db.Column(db.String(200))
    meal_plan_link = db.Column(db.Integer, db.ForeignKey("meal_plan.id"))
    meal_plan_id = db.relationship("MealPlan")


#  TO BE IMPLEMENTED
class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    amount = db.Column(db.Integer)
    unit = db.Column(db.String(200))
    username = db.Column(db.String(200))


class IngredientStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    amount = db.Column(db.Integer)
    unit = db.Column(db.String(200))
