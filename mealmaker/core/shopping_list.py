
from dataclasses import dataclass


@dataclass
class ShoppingListeLogic:
    
    @staticmethod
    def generate_shopping_list(meals)-> dict:
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
        return shopping_list