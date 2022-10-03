from os import access
import random
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    jsonify,
    redirect,
    url_for,
    abort,
)
from flask_login import login_required, current_user
from .forms import NewMealForm, UpdateMealForm, IngredientForm
from .models import Ingredient, Meal, MealPlan, ShoppingList, MealStore, IngredientStore
from . import db

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route("/meals", methods=["GET", "POST"])
@login_required
def meals():
    form = NewMealForm()
    template_form = IngredientForm(prefix="ingredient-_-")
    if form.is_submitted():
        meal = Meal(
            name=form.name.data,
            portion=form.portion.data,
            prep_time_hour=form.prep_time_hour.data,
            prep_time_min=form.prep_time_min.data,
            cook_time_hour=form.cook_time_hour.data,
            cook_time_min=form.cook_time_min.data,
            diet_type=form.diet_type.data,
            health_type=form.health_type.data,
            effort=form.effort.data,
            cost=form.cost.data,
            freezable=form.freezable.data,
            num_ingredient=form.num_ingredient.data,
            time_to_go_off=form.time_to_go_off.data,
            cal_per_portion=form.cal_per_portion.data,
            protein_per_portion=form.protein_per_portion.data,
            fat_per_portion=form.fat_per_portion.data,
            carb_per_portion=form.carb_per_portion.data,
            recipe=form.recipe.data,
        )
        db.session.add(meal)
        for i in form.ingredient.data:
            new_ingredient = Ingredient(
                name=i["ingredient_name"],
                amount=i["ingredient_amount"],
                unit=i["ingredient_unit"],
                meal_id=meal.id,
            )
            meal.ingredients.append(new_ingredient)
            db.session.add(new_ingredient)
        db.session.commit()
        flash(f"Meal added successfully!", category="success")
        return redirect(url_for("views.meals"))
    meals = Meal.query.all()
    return render_template(
        "meals.html",
        user=current_user,
        form=form,
        meals=meals,
        legend="Add a new Meal",
        _template=template_form,
    )


@views.route("/meal/<int:id>", methods=["GET", "POST"])
@login_required
def meal(id):
    meal = Meal.query.get_or_404(id)
    ingredient = Ingredient.query.filter(Ingredient.meal_link == id)
    form = UpdateMealForm()
    template_form = IngredientForm(prefix="ingredient-_-")
    if form.is_submitted():
        meal.name = form.name.data
        meal.portion = form.portion.data
        meal.prep_time_hour = form.prep_time_hour.data
        meal.prep_time_min = form.prep_time_min.data
        meal.cook_time_hour = form.cook_time_hour.data
        meal.cook_time_min = form.cook_time_min.data
        meal.diet_type = form.diet_type.data
        meal.health_type = form.health_type.data
        meal.effort = form.effort.data
        meal.cost = form.cost.data
        meal.freezable = form.freezable.data
        meal.num_ingredient = form.num_ingredient.data
        meal.time_to_go_off = form.time_to_go_off.data
        meal.cal_per_portion = form.cal_per_portion.data
        meal.protein_per_portion = form.protein_per_portion.data
        meal.fat_per_portion = form.fat_per_portion.data
        meal.carb_per_portion = form.carb_per_portion.data
        meal.recipe = form.recipe.data
        db.session.query(Ingredient).filter(Ingredient.meal_link == id).delete()
        db.session.commit()
        for i in form.ingredient.data:
            new_ingredient = Ingredient(
                name=i["ingredient_name"],
                amount=i["ingredient_amount"],
                unit=i["ingredient_unit"],
                meal_link=id,
            )
            db.session.add(new_ingredient)
        db.session.query(Ingredient).order_by(Ingredient.name.desc())
        db.session.commit()
        flash("Your meal has been updated!", "success")
        return redirect(url_for("views.meal", id=meal.id))
    elif request.method == "GET":
        form.name.data = meal.name
        form.portion.data = meal.portion
        form.prep_time_hour.data = meal.prep_time_hour
        form.prep_time_min.data = meal.prep_time_min
        form.cook_time_hour.data = meal.cook_time_hour
        form.cook_time_min.data = meal.cook_time_min
        form.diet_type.data = meal.diet_type
        form.health_type.data = meal.health_type
        form.effort.data = meal.effort
        form.cost.data = meal.cost
        form.freezable.data = meal.freezable
        form.num_ingredient.data = meal.num_ingredient
        form.time_to_go_off.data = meal.time_to_go_off
        form.cal_per_portion.data = meal.cal_per_portion
        form.protein_per_portion.data = meal.protein_per_portion
        form.fat_per_portion.data = meal.fat_per_portion
        form.carb_per_portion.data = meal.carb_per_portion
        form.recipe.data = meal.recipe
        for row in ingredient:
            subform = {
                "id": row.id,
                "ingredient_name": row.name,
                "ingredient_amount": row.amount,
                "ingredient_unit": row.unit,
            }
            print(row.name)
            form.ingredient.append_entry(subform)

    '''
    FIX UPDATE FORM

    
    '''
    return render_template(
        "meal.html",
        user=current_user,
        form=form,
        meal=meal,
        ingredient=ingredient,
        legend="Update Meal",
        _template=template_form,
    )


@views.route("/meal/<int:id>/delete", methods=["POST"])
@login_required
def delete_post(id):
    meal = Meal.query.get_or_404(id)
    db.session.delete(meal)
    db.session.commit()
    flash("Your meal has been deleted!", "success")
    return redirect(url_for("views.meals"))


@views.route("/meal_planner", methods=["GET", "POST"])
@login_required
def meal_planner():
    if request.method == 'POST':
        if request.form['generate-meal-plan'] == 'Generate Meal Plan':
            meals = Meal.query.all()
            meals_list = [meal for meal in meals]
            meal_plan = [random.choice(meals_list) for _ in range(7)]
            db.session.query(MealPlan).filter(MealPlan.username == current_user.id).delete()
            db.session.commit()
            for meal in meal_plan:
                planned_meal = MealPlan(meal_name=meal.name, username=current_user.id)
                db.session.add(planned_meal)
            db.session.commit()
            return redirect(url_for("views.meal_planner", user=current_user, meal_plan=meal_plan))

    elif request.method == 'GET':
        checker = db.session.query(MealPlan).filter(MealPlan.username == current_user.id)
        checker_list = [meal for meal in checker]
        if len(checker_list) == 0:
            meals = Meal.query.all()
            meals_list = [meal for meal in meals]
            meal_plan = [random.choice(meals_list) for _ in range(7)]
            db.session.query(MealPlan).filter(MealPlan.username == current_user.id).delete()
            db.session.commit()
            for meal in meal_plan:
                planned_meal = MealPlan(meal_name=meal.name, username=current_user.id)
                db.session.add(planned_meal)
            db.session.commit()
            flash("Meal Plan Generated!", "success")
        else:
            meals = MealPlan.query.filter(MealPlan.username == current_user.id)
            meal_plan = [meal for meal in meals]
    return render_template("meal_planner.html", user=current_user, meal_plan=meal_plan)


@views.route("/my_store", methods=["GET", "POST"])
@login_required
def my_store():
    meals = MealPlan.query.all()
    meal_store_list = []
    for meal in meals:
        meal_name = meal.meal_name
        queried_meal = Meal.query.filter(Meal.name == meal_name).all()[0]
        stored_meal = MealStore(
            stored_mealname=queried_meal.name,
            portion=queried_meal.portion,
            freezable=queried_meal.freezable,
            time_to_go_off=queried_meal.time_to_go_off,
            username=current_user.id,
        )
        meal_store_list.append(stored_meal)
    '''
    DO PROCESSING ON MEALS IN STORE
    - link properly to databases
    - update and delete meals in the store
    - ability to reduce the number of portions or add portions with +/-

    '''
    return render_template(
        "my_store.html",
        user=current_user,
        meal_store_list=meal_store_list,
    )


@views.route("/shopping_list", methods=["GET", "POST"])
@login_required
def shopping_list():
    meals = MealPlan.query.all()
    shopping_list = []
    for meal in meals:
        meal_name = meal.meal_name
        queried_meal = Meal.query.filter(Meal.name == meal_name).all()[0]
        ingredients_query = queried_meal.ingredients
        for ingredient in ingredients_query:
            shopping_ingredient = ShoppingList(
                name = ingredient.name,
                amount = ingredient.amount,
                unit = ingredient.unit,
                username = current_user.id
            )
            shopping_list.append(shopping_ingredient)
    '''
    DO PROCESSING ON SHOPPING LIST
    - link properly to databases
    - update and delete items in the ingredient list
    - merge like for like items in different recipes
    - conversions between units for the same ingredient type
    - map from ingredients -> to sainsburys ingredients?
    '''
    return render_template("shopping_list.html", user=current_user, shopping_list=shopping_list)
