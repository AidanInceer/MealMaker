import sqlite3

con = sqlite3.connect("./mealmaker/database.db")
cursor = con.cursor()
meal_list = cursor.execute("SELECT * FROM meal;").fetchall()
user_list = cursor.execute("SELECT * FROM user;").fetchall()
ingredient_list = cursor.execute("SELECT * FROM ingredient;").fetchall()
print(
    "=================================================================================="
)

print("user TABLE:")
for user in user_list:
    print(user)
print("")
print(
    "=================================================================================="
)

print("meal TABLE:")
for meal in meal_list:
    print(meal)
print("")
print(
    "=================================================================================="
)

print("ingredient TABLE:")
for ingredient in ingredient_list:
    print(ingredient)
print("")
print(
    "=================================================================================="
)
