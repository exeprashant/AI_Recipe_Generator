import requests
import json
import uuid

def get_recipe(user_input):
    # Use a unique sender ID for each request to avoid session persistence
    payload = {"sender": str(uuid.uuid4()), "message": user_input}
    try:
        response = requests.post("http://localhost:5005/webhooks/rest/webhook", json=payload)
        rasa_response = response.json()
        # Collect all text messages and join them with newlines
        full_response = "\n".join(msg["text"] for msg in rasa_response if "text" in msg)
        return full_response or "No response from Rasa."
    except requests.exceptions.ConnectionError:
        return "Error: Rasa server is not running. Please start the Rasa server."

# Command-line interface
print("AI Recipe Generator")
print("Start the Rasa server in another terminal with: rasa run --enable-api --cors '*'")
print("Start the Rasa action server in another terminal with: rasa run actions")
print("Type 'exit' to quit.")
while True:
    user_input = input("Enter your request (e.g., 'Generate a recipe for spaghetti carbonara'): ")
    if user_input.lower() == "exit":
        break
    print("\n=== Recipe ===\n" + get_recipe(user_input) + "\n==============\n")
