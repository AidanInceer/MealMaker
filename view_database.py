import sqlite3
con = sqlite3.connect("./mealmaker/database.db")
cursor = con.cursor()
meal_list = cursor.execute("SELECT * FROM meal;").fetchall()
print(meal_list)