function deleteMeal(MealID) {
  fetch("/delete-meal", {
    method: "POST",
    body: JSON.stringify({ MealID: MealID }),
  }).then((_res) => {
    window.location.href = "/meal-plan";
  });
}