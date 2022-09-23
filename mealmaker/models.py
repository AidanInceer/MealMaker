from xmlrpc.client import Boolean
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    name = db.Column(db.String(200))
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
    time_to_go_off = db.Column(db.Integer)  # in Days
    recipe = db.Column(db.Text)
    # ingredients = relationship('Ingredient')


class Ingredient:
    id = db.Column(db.Integer, primary_key=True)
    # meal_id = db.Column(db.Integer, db.ForeignKey("parent.id"))
    name = db.Column(db.String(200))
    amount = db.Column(db.Integer)
    unit = db.Column(db.String(200))
