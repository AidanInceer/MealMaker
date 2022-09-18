function deleteRecipe(recipeId) {
  fetch("/delete-recipe", {
    method: "POST",
    body: JSON.stringify({ recipeId: recipeId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}