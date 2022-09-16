import random
import pandas as pd
from IPython import display

meal_list = [
    {'meal_name':'meat bolognase', 'ingredients':['a','b','c'], 'portion_size': 4, 'meal_type':'lunch', 'macro_nutrition_abs':{'carb':100, 'fat': 300, 'protein':75}},
    {'meal_name':'stir fry', 'ingredients':['d','e','f'], 'portion_size': 2, 'meal_type':'dinner', 'macro_nutrition_abs':{'carb':80, 'fat': 640, 'protein':123}},
    {'meal_name':'lentil bolognase', 'ingredients':['b','c','g'], 'portion_size': 6, 'meal_type':'dinner', 'macro_nutrition_abs':{'carb':235, 'fat': 234, 'protein':724}},
    {'meal_name':'omelette and chips', 'ingredients':['h','i','j'], 'portion_size': 1, 'meal_type':'dinner', 'macro_nutrition_abs':{'carb':762, 'fat': 523, 'protein':132}}
]

meal_names = []
for i in meal_list:
    meal_names.append(i['meal_name'])

weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
weekly_mealplan = []
for i in range(7):
    weekly_mealplan.append(random.choice(meal_names))

data = zip(weekdays,weekly_mealplan)

df = pd.DataFrame(data, columns=["Weekdays","Meals"]).set_index("Weekdays")

print(df)