import random
import sqlite3

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

print(weekly_food)