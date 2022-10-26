import random
from datetime import datetime, date, timedelta
import calendar

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from . import db
from .forms import IngredientForm, NewMealForm, UpdateMealForm
from .models import Ingredient, IngredientStore, Meal, MealPlan, MealStore, ShoppingList

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    # Object preparation
    now = datetime.now()
    week_start_date = now - timedelta(days=now.weekday())
    week_end_date = week_start_date + timedelta(days=6)
    today = date.today()
    no_days_curr_month = calendar.monthrange(datetime.now().year, datetime.now().month)[
        1
    ]
    previous_month_word = (date.today().replace(day=1) - timedelta(days=1)).strftime(
        "%B"
    )
    starting_weekday = datetime(today.year, today.month, 1).weekday()
    end_weekday = datetime(today.year, today.month, no_days_curr_month).weekday()
    no_days_previous_month = calendar.monthrange(
        datetime.now().year, datetime.now().month - 1
    )[1]

    previous_month_list = [x + 1 for x in range(no_days_previous_month)][
        -starting_weekday:
    ]
    current_month_list = [x + 1 for x in range(no_days_curr_month)]
    next_month_list = [x + 1 for x in range((7-1-end_weekday))]
    
    # Calendar object
    calendar_data = {
        "current_day": datetime.now().day,
        "current_weekday": datetime.now().strftime("%A"),
        "week_start_day": week_start_date.day,
        "week_end_day": week_end_date.day,
        "current_month_int": datetime.now().month,
        "current_month_word": datetime.now().strftime("%B"),
        "previous_month_word": previous_month_word,
        "no_days_curr_month": no_days_curr_month,
        "no_days_previous_month": no_days_previous_month,
        "previous_month_list": previous_month_list,
        "current_month_list": current_month_list,
        "next_month_list": next_month_list,
        "starting_weekday": starting_weekday,
        "current_year": datetime.now().year,
    }
    print(next_month_list)
    return render_template("home.html", user=current_user, calendar_data=calendar_data)


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
        meal.name = form.name.data.lower()
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
                name=i["ingredient_name"].lower(),
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
            form.ingredient.append_entry(subform)

        recipe_display = meal.recipe.replace("\r", "").split("\n")
    return render_template(
        "meal.html",
        user=current_user,
        form=form,
        meal=meal,
        ingredient=ingredient,
        legend="Update Meal",
        _template=template_form,
        recipe_display=recipe_display,
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
    if request.method == "POST":
        if request.form["generate-meal-plan"] == "Generate Meal Plan":
            meals = Meal.query.all()
            meals_list = [meal for meal in meals]
            meal_plan = [random.choice(meals_list) for _ in range(7)]
            db.session.query(MealPlan).filter(
                MealPlan.username == current_user.id
            ).delete()
            db.session.commit()
            for meal in meal_plan:
                planned_meal = MealPlan(
                    meal_name=meal.name, username=current_user.id, meal_link=meal.id
                )
                db.session.add(planned_meal)
            db.session.commit()
            return redirect(
                url_for("views.meal_planner", user=current_user, meal_plan=meal_plan)
            )
    elif request.method == "GET":
        checker = db.session.query(MealPlan).filter(
            MealPlan.username == current_user.id
        )
        checker_list = [meal for meal in checker]
        if len(checker_list) == 0:
            meals = Meal.query.all()
            meals_list = [meal for meal in meals]
            meal_plan = []
        else:
            meals = MealPlan.query.filter(MealPlan.username == current_user.id)
            meal_plan = [meal for meal in meals]
    return render_template("meal_planner.html", user=current_user, meal_plan=meal_plan)


@views.route("/my_store", methods=["GET", "POST"])
@login_required
def my_store():
    # Query database for meals in meal plan
    planned_meals = MealPlan.query.filter(MealPlan.username == current_user.id)

    # Method to generate meals in the meal store
    stored_meals = {}
    for planned_meal in planned_meals:
        if (planned_meal.meal_name in stored_meals) and (
            stored_meals[planned_meal.meal_name]["portion"] > 0
        ):
            stored_meals[planned_meal.meal_name] = {
                "meal_id": planned_meal.id,
                "meal_name": planned_meal.meal_name,
                "username": planned_meal.username,
                "portion": stored_meals[planned_meal.meal_name]["portion"] - 1,
                "freezable": planned_meal.meal_id.freezable,
                "time_to_go_off": planned_meal.meal_id.time_to_go_off,
            }
        elif (planned_meal.meal_name in stored_meals) and (
            stored_meals[planned_meal.meal_name]["portion"] == 0
        ):
            stored_meals[planned_meal.meal_name] = {
                "meal_id": planned_meal.id,
                "meal_name": planned_meal.meal_name,
                "username": planned_meal.username,
                "portion": planned_meal.meal_id.portion - 1,
                "freezable": planned_meal.meal_id.freezable,
                "time_to_go_off": planned_meal.meal_id.time_to_go_off,
            }
        elif planned_meal.meal_name not in stored_meals:
            stored_meals[planned_meal.meal_name] = {
                "meal_id": planned_meal.id,
                "meal_name": planned_meal.meal_name,
                "username": planned_meal.username,
                "portion": planned_meal.meal_id.portion - 1,
                "freezable": planned_meal.meal_id.freezable,
                "time_to_go_off": planned_meal.meal_id.time_to_go_off,
            }
        else:
            pass

    # Update meals in the mealstore table
    db.session.query(MealStore).filter(MealStore.username == current_user.id).delete()
    for key, value in stored_meals.items():
        if value["portion"] == 0:
            pass
        else:
            stored_meal = MealStore(
                stored_mealname=key,
                portion=value["portion"],
                freezable=value["freezable"],
                time_to_go_off=value["time_to_go_off"],
                username=current_user.id,
                meal_plan_link=value["meal_id"],
            )
            db.session.add(stored_meal)
    db.session.commit()
    meal_store_list = [
        (key, value["portion"])
        for key, value in stored_meals.items()
        if value["portion"] > 0
    ]

    return render_template(
        "my_store.html",
        user=current_user,
        meal_store_list=meal_store_list,
    )


@views.route("/shopping_list", methods=["GET", "POST"])
@login_required
def shopping_list():
    # Query database for meals in meal plan
    meals = MealPlan.query.filter(MealPlan.username == current_user.id)

    # Method to generate shopping list items
    shopping_list = {}
    for meal in meals:
        for ingredient in list(meal.meal_id.ingredients):
            ingredient_name = ingredient.name.lower()
            if ingredient_name in shopping_list:
                shopping_list[ingredient_name] = {
                    "name": ingredient_name,
                    "id": ingredient.id,
                    "amount": shopping_list[ingredient_name]["amount"]
                    + ingredient.amount,
                    "unit": ingredient.unit,
                }
            else:
                shopping_list[ingredient_name] = {
                    "name": ingredient_name,
                    "id": ingredient.id,
                    "amount": ingredient.amount,
                    "unit": ingredient.unit,
                }

    # Update meals in the mealstore table
    db.session.query(ShoppingList).filter(
        ShoppingList.username == current_user.id
    ).delete()
    for key, value in shopping_list.items():
        stored_meal = ShoppingList(
            name=key,
            amount=value["amount"],
            unit=value["unit"],
            username=current_user.id,
        )
        db.session.add(stored_meal)
    db.session.commit()

    return render_template(
        "shopping_list.html", user=current_user, shopping_list=shopping_list
    )
