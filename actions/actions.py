import logging
import spacy
import json  # Add this import
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Load spaCy model once globally
nlp = spacy.load("en_core_web_sm")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ActionGenerateRecipe(Action):
    def name(self):
        return "action_generate_recipe"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        food = tracker.get_slot("food") or "unknown"
        doc = nlp(food)
        food_entity = doc.text.lower()
        logger.info(f"Looking for recipe: {food_entity}")

        try:
            with open("recipes.json", "r") as f:
                recipes = json.load(f)
        except FileNotFoundError:
            logger.error("recipes.json not found")
            dispatcher.utter_message(text="Recipe dataset not found.")
            return []

        for recipe in recipes:
            if recipe["dish"].lower() == food_entity:
                response = f"**{recipe['dish'].title()}**\n\n**Ingredients**:\n"
                for ing in recipe["ingredients"]:
                    response += f"- {ing}\n"
                response += "\n**Steps**:\n"
                for i, step in enumerate(recipe["steps"], 1):
                    response += f"{i}. {step}\n"
                dispatcher.utter_message(text=response)
                logger.info(f"Found recipe for {food_entity}")
                return []

        dispatcher.utter_message(text=f"Sorry, no recipe found for {food_entity}.")
        logger.warning(f"No recipe found for {food_entity}")
        return []