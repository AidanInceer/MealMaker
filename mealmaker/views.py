from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Recipe
from . import db
import json
import random
import sqlite3

views = Blueprint('views', __name__)

con = sqlite3.connect("./mealmaker/database.db")
cursor = con.cursor()
meal_list = cursor.execute("SELECT data FROM recipe;").fetchall()
int_list = []
for item in meal_list:
    output = str(''.join(item))
    int_list.append(output)
weekly_meals_list = []
for meal in range(7):
    m = random.choice(int_list)
    weekly_meals_list.append(m)
weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
weekly_food = dict(zip(weekdays,weekly_meals_list))

@views.route('/', methods=['GET', 'POST'])
@login_required
def recipes():
    if request.method == 'POST':
        # recipe_list = json.loads(request.data)
        # random_recipe = random.choice(recipe_list)
        # flash(f'{random_recipe}', category='success')

        recipe = request.form.get('recipe')

        if len(recipe) < 1:
            flash('Not a valid Recipe!', category='error')
        else:
            new_recipe = Recipe(data=recipe, user_id=current_user.id)
            db.session.add(new_recipe)
            db.session.commit()
            flash('recipe added!', category='success')

    return render_template("recipes.html", user=current_user, meals=weekly_food)


@views.route('/delete-recipe', methods=['POST'])
def delete_recipe():
    recipe = json.loads(request.data)
    recipeId = recipe['recipeId']
    recipe = Recipe.query.get(recipeId)
    if recipe:
        if recipe.user_id == current_user.id:
            db.session.delete(recipe)
            db.session.commit()
    return jsonify({})