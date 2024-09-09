import requests

FOOD_FACTS_API_URL = "https://world.openfoodfacts.org/cgi/search.pl"

def get_nutrition_facts_by_name(food_name):
    params = {
        "search_terms": food_name,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }
    response = requests.get(FOOD_FACTS_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('products'):
            product = data['products'][0]
            nutrition_facts = product.get('nutriments', {})
            return nutrition_facts
        else:
            return {"error": "Product not found."}
    else:
        return {"error": "Failed to fetch data from Open Food Facts API."}
