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
from .models import Ingredient, Meal
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
    if form.validate_on_submit():
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
            recipe=form.recipe.data,
        )
        db.session.add(meal)
        print(meal)
        for i in form.ingredient.data:
            new_ingredient = Ingredient(**i)

            meal.ingredients.append(new_ingredient)
            print(type(i))

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
    ingredient = Ingredient.query.get_or_404(meal.id)
    form = UpdateMealForm()
    if form.validate_on_submit():
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
        meal.recipe = form.recipe.data
        ingredient.name = form.ingredient.ingredient_name.data
        ingredient.amount = form.ingredient.ingredient_amount.data
        ingredient.unit = form.ingredient.ingredient_unit.data
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
        form.recipe.data = meal.recipe
        form.ingredient.ingredient_name.data = ingredient.name
        form.ingredient.ingredient_amount.data = ingredient.amount
        form.ingredient.ingredient_unit.data = ingredient.unit
    return render_template(
        "meal.html",
        user=current_user,
        form=form,
        meal=meal,
        ingredient=ingredient,
        legend="Update Meal",
    )


@views.route("/meal/<int:id>/delete", methods=["POST"])
@login_required
def delete_post(id):
    meal = Meal.query.get_or_404(id)
    # ingredient = Ingredient.query.get_or_404(id)
    db.session.delete(meal)
    # db.session.delete(ingredient)
    db.session.commit()
    flash("Your meal has been deleted!", "success")
    return redirect(url_for("views.meals"))


@views.route("/my_store", methods=["GET", "POST"])
@login_required
def my_store():
    return render_template("my_store.html", user=current_user)


@views.route("/shopping_list", methods=["GET", "POST"])
@login_required
def shopping_list():
    return render_template("shopping_list.html", user=current_user)


@views.route("/meal_planner", methods=["GET", "POST"])
@login_required
def meal_planner():
    return render_template("meal_planner.html", user=current_user)
