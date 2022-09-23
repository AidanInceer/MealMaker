function deleteMeal(MealID) {
  fetch("/delete-meal", {
    method: "POST",
    body: JSON.stringify({ MealID: MealID }),
  }).then((_res) => {
    window.location.href = "/meal-plan";
  });
}

function addIngredient() {
  const ingredientRowContElement = document.querySelector('#ingredient-row-container')
  const ingredientTemplate = `<div class="form-row">
  <div class="col-6">
      <input type="text" class="form-control" id="validationTooltip03">
  </div>
  <div class="col-6">
      <div class="input-group mb-3">
          <input type="number" class="form-control" id="validationTooltip05"
              placeholder="Amount">
          <div class="input-group-append">
              <select class="form-control input-group-text text-left"
                  placeholder="Unit">
                  <option>g</option>
                  <option>kg</option>
                  <option>tbsp</option>
                  <option>tsp</option>
                  <option>item</option>
                  <option>oz</option>
                  <option>ml</option>
                  <option>liter</option>

              </select>
          </div>
      </div>
  </div>
</div>`
  const newIngredientRowElement = document.createElement('div')
  newIngredientRowElement.innerHTML = ingredientTemplate
  ingredientRowContElement.appendChild(newIngredientRowElement)
}

window.addEventListener('load', () => {
  const addIngredientElement = document.querySelector('#add-Ingredient')
  addIngredientElement.addEventListener('click', addIngredient)
})