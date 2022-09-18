import sqlite3
con = sqlite3.connect("./mealmaker/database.db")
cursor = con.cursor()

cursor.execute("SELECT * FROM recipe;")
print(cursor.fetchall()) 