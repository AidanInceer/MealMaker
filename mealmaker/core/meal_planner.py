from dataclasses import dataclass
import random


@dataclass
class MealPlannerEngine:
    @staticmethod
    def generate_planned_meal_list(meals_list: list) -> list:
        planned_meals = []
        for index in range(7):
            planned_meal = random.choice(meals_list)
            # Meal planner Flags:
            freeze_flag = True if planned_meal.freezable == "Yes" else False
            portion_flag = True if planned_meal.portion == 2 else False
            if index == 0 or index == 1:
                pass
            elif (portion_flag is True) and (
                planned_meals[index - 1] != planned_meals[index - 2]
            ):
                planned_meal = planned_meals[index - 1]

            if planned_meals.count(planned_meal) > 3:
                planned_meal = random.choice(meals_list)

            planned_meals.append(planned_meal)
        return planned_meals
