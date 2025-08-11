import requests

API_KEY = "d832adbe7b1f429b86721918c36550f5"  # replace with your actual key

def find_recipes(ingredients):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ingredients,
        "number": 5,          # number of recipes to fetch
        "ranking": 1,         # maximize used ingredients
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

def get_nutrition(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
    params = {"apiKey": API_KEY}
    response = requests.get(url, params=params)
    return response.json()

def main():
    ingredients = input("Enter ingredients (comma separated): ")
    recipes = find_recipes(ingredients)

    for recipe in recipes:
        print(f"\nRecipe: {recipe['title']}")
        nutrition = get_nutrition(recipe['id'])
        print(f"Calories: {nutrition.get('calories', 'N/A')}")
        print(f"Carbs: {nutrition.get('carbs', 'N/A')}")
        print(f"Fat: {nutrition.get('fat', 'N/A')}")
        print(f"Protein: {nutrition.get('protein', 'N/A')}")
        print(f"Recipe link: {recipe.get('sourceUrl', 'No link available')}")

if __name__ == "__main__":
    main()
