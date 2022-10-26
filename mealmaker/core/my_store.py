
from dataclasses import dataclass


@dataclass
class MyStoreLogic:

    @staticmethod
    def generate_stored_meals(planned_meals)-> dict:
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
        return stored_meals
