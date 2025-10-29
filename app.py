from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
from rapidfuzz import fuzz
import ollama

app = FastAPI(
    title="AI Recipe Chatbot",
    description="Suggest recipes based on entered ingredients using local LLM + similarity search",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow React/Streamlit frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("train.json", "r", encoding="utf-8") as f:
    recipes = json.load(f)

print(f"Loaded {len(recipes)} recipes")


def find_best_match(user_ingredients):
    """
    Compute the best recipe match based on ingredient similarity.
    """
    best_score = 0
    best_recipe = None

    for recipe in recipes:
        ingredients_text = ", ".join(recipe["ingredients"])
        score = fuzz.token_set_ratio(user_ingredients, ingredients_text)
        if score > best_score:
            best_score = score
            best_recipe = recipe

    return best_recipe, best_score


def is_ingredients_query(query):
    """
    Determine if the query looks like a list of ingredients.
    """
    query_lower = query.lower()
    # Check for commas (common in ingredient lists)
    if "," in query:
        return True
    # Check for common ingredient words
    common_ingredients = ["egg", "onion", "tomato", "chicken", "beef", "rice", "potato", "carrot", "milk", "cheese", "bread", "butter", "oil", "salt", "pepper", "sugar", "flour", "garlic", "ginger", "lemon", "apple", "banana", "orange"]
    words = query_lower.split()
    ingredient_count = sum(1 for word in words if word in common_ingredients)
    return ingredient_count >= 2  # At least 2 common ingredients suggest it's a list

@app.post("/get_recipe")
async def get_recipe(request: Request):
    """
    Input:
        {
            "ingredients": "egg, onion, tomato"
        }
    Output:
        {
            "best_cuisine": "greek",
            "matched_ingredients": [...],
            "similarity_score": 87,
            "llm_recipe": "Full recipe suggestion..."
        }
    """
    data = await request.json()
    user_ingredients = data.get("ingredients", "").lower()

    if not user_ingredients.strip():
        return {"error": "Please provide ingredients."}

    # Step 1: Find best match from dataset
    best_recipe, score = find_best_match(user_ingredients)

    if not best_recipe:
        return {"message": "No similar recipe found."}

    # Step 2: Generate LLM-based description
    prompt = f"""
    Suggest a recipe using these ingredients: {user_ingredients}.
    You can take inspiration from {best_recipe['cuisine']} cuisine.
    Give a short cooking description.
    """
    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        recipe_text = response["message"]["content"]
    except Exception as e:
        recipe_text = f"(Local LLM unavailable) Suggested cuisine: {best_recipe['cuisine']}."

    # Step 3: Return response
    return {
        "best_cuisine": best_recipe["cuisine"],
        "matched_ingredients": best_recipe["ingredients"],
        "similarity_score": score,
        "llm_recipe": recipe_text
    }


@app.post("/chat")
async def chat(request: Request):
    """
    Unified chat endpoint for recipe suggestions and general conversation.
    Input:
        {
            "query": "egg, onion" or "Hello"
        }
    Output:
        {
            "response": "Recipe suggestion or chat response..."
        }
    """
    data = await request.json()
    query = data.get("query", "").strip()

    if not query:
        return {"response": "Please provide a query."}

    if is_ingredients_query(query):
        # Treat as ingredients query
        user_ingredients = query.lower()

        # Step 1: Find best match from dataset
        best_recipe, score = find_best_match(user_ingredients)

        if not best_recipe:
            return {"response": "Sorry, I couldn't find a recipe with those ingredients. Try something else!"}

        # Step 2: Generate LLM-based description
        prompt = f"""
        Suggest a recipe using these ingredients: {user_ingredients}.
        You can take inspiration from {best_recipe['cuisine']} cuisine.
        Give a short cooking description.
        """
        try:
            response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
            recipe_text = response["message"]["content"]
        except Exception as e:
            # Fallback: Suggest a simple recipe using matched ingredients
            ingredients_list = ", ".join(best_recipe["ingredients"])
            recipe_text = f"(Local LLM unavailable) Try a simple {best_recipe['cuisine']} dish using your ingredients: {user_ingredients}. Suggested ingredients from match: {ingredients_list}. Basic idea: Cook the ingredients together with spices for a quick meal."

        return {"response": recipe_text}
    else:
        # Treat as general chat query
        query_lower = query.lower().strip()
        # Simple hardcoded responses for common queries
        if query_lower in ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]:
            chat_response = "Hello! How can I help you today? Try entering some ingredients for recipe suggestions!"
        elif query_lower in ["how are you", "how are you?", "how's it going"]:
            chat_response = "I'm doing great, thanks! Ready to suggest some recipes. What ingredients do you have?"
        elif query_lower in ["bye", "goodbye", "see you", "thanks", "thank you"]:
            chat_response = "Goodbye! Come back anytime for more recipe ideas."
        else:
            # Try LLM for other queries
            prompt = f"Respond to this query: {query}"
            try:
                response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
                chat_response = response["message"]["content"]
            except Exception as e:
                chat_response = "I'm sorry, I can't chat right now. Try asking for recipes with ingredients like 'egg, onion'!"

        return {"response": chat_response}

