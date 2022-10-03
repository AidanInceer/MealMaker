meal_dict = {
    "A": 2,
    "B": 4,
    "C": 2,
    "D": 1,
    "E": 3
}

planned_meals = ["A","A","B","C","D","B","E"]
stored_meals = {}
for planned_meal in planned_meals:
    # Cook new meal and add spare to store
    if planned_meal not in stored_meals:
        stored_meals[planned_meal] = meal_dict[planned_meal] - 1

    # Use meal from store
    elif planned_meal in stored_meals and stored_meals[planned_meal] > 0:
        stored_meals[planned_meal] = stored_meals[planned_meal] - 1

    # Cook new meal and add spare to store - meal allready in dict
    elif planned_meal in stored_meals and stored_meals[planned_meal] == 0:
        stored_meals[planned_meal] = stored_meals[planned_meal] + meal_dict[planned_meal] - 1
    else:
        pass
