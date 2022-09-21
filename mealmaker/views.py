from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort
from flask_login import login_required, current_user
from .forms import NewMealForm
from .models import Meal
from . import db
from flask_sqlalchemy import SQLAlchemy
import json


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/meal-plan', methods=['GET', 'POST'])
@login_required
def meal_plan():
    form = NewMealForm()
    if form.validate_on_submit():
        meal = Meal(name=form.name.data, portion=form.portion.data)
        db.session.add(meal)
        db.session.commit()
        flash(f'Meal added successfully!', category='success')
        return redirect(url_for('views.meal_plan'))
    meals = Meal.query.all()
    return render_template("meal_plan.html", user=current_user, form=form, meals=meals, legend= 'Add a new Meal')


@views.route("/meal-plan/<int:id>")
def meal(id):
    meal = Meal.query.get_or_404(id)
    return render_template('meal.html', meal_name=Meal.name, meal=meal, user=current_user)


@views.route("/meal-plan/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_meal(id):
    meal = Meal.query.get_or_404(id)
    form = NewMealForm()
    if form.validate_on_submit():
        meal.name = form.name.data
        meal.portion = form.portion.data
        db.session.commit()
        flash('Your meal has been updated!', 'success')
        return redirect(url_for('views.meal', id=meal.id))
    elif request.method == 'GET':
        form.name.data = meal.name
        form.portion.data = meal.portion
    return render_template("meal_plan.html", user=current_user, form=form, meal=meal, legend = 'Udpdate Meal')


@views.route("/meal-plan/<int:id>/delete", methods=['POST'])
@login_required
def delete_post(id):
    meal = Meal.query.get_or_404(id)
    db.session.delete(meal)
    db.session.commit()
    flash('Your meal has been deleted!', 'success')
    return redirect(url_for('views.meal_plan'))