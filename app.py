from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "262e2accabbc46d38e7bc9d9f2eb36ed"  # your Spoonacular API key

def find_recipes(ingredients):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ingredients,
        "number": 5,
        "ranking": 1,
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("API Error:", response.status_code, response.text)
        return []
    return response.json()

def get_nutrition(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
    params = {"apiKey": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Nutrition API Error:", response.status_code, response.text)
        return {}
    return response.json()

def get_recipe_info(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": API_KEY, "includeNutrition": False}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Recipe Info API Error:", response.status_code, response.text)
        return {}
    return response.json()

@app.route("/", methods=["GET", "POST"])
def home():
    recipes = []
    error_message = None
    if request.method == "POST":
        ingredients = request.form.get("ingredients")
        if ingredients:
            found = find_recipes(ingredients)
            if not found:
                error_message = "No recipes found or API error."
            else:
                for recipe in found:
                    if isinstance(recipe, dict) and "id" in recipe:
                        nutrition = get_nutrition(recipe["id"])
                        info = get_recipe_info(recipe["id"])
                        recipes.append({
                            "title": recipe.get("title", "No title"),
                            "calories": nutrition.get("calories", "N/A"),
                            "carbs": nutrition.get("carbs", "N/A"),
                            "fat": nutrition.get("fat", "N/A"),
                            "protein": nutrition.get("protein", "N/A"),
                            "link": recipe.get("sourceUrl", "#"),
                            "image": recipe.get("image", ""),
                            "instructions": info.get("instructions", "No instructions available"),
                            "ingredients": [ing.get("originalString", ing.get("original", "Ingredient info missing")) for ing in info.get("extendedIngredients", [])]
                        })
                    else:
                        print("Skipping invalid recipe data:", recipe)
    return render_template("index.html", recipes=recipes, error=error_message)

if __name__ == "__main__":
    app.run(debug=True)
