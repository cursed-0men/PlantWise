import cohere
import re

# Replace with your Cohere API key
API_KEY = 'KTn7ndyWTyFbx9yGwzrS27JYOy0TRjttcObYzk5t'

# Initialize the Cohere client
co = cohere.Client(API_KEY)

# Function to generate AI response using Cohere
def get_ai_response(prompt):
    try:
        response = co.generate(
            model='command-xlarge-nightly',  # Use the appropriate model
            prompt=prompt,
            max_tokens=250,  # Increased token count for disease and remedy suggestions
            temperature=0.7
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Function to clean and format the user's input
def clean_input(user_input):
    # Remove any extra spaces, special characters, and lowercase the input
    user_input = re.sub(r'[^a-zA-Z, ]', '', user_input).lower().strip()
    return user_input

# Function to remove markdown formatting
def remove_markdown(text):
    text = re.sub(r'\*\*', '', text)  # Remove bold markers
    text = re.sub(r'[_]', '', text)   # Remove italic markers if any
    text = re.sub(r'[`]', '', text)   # Remove inline code markers if any
    text = re.sub(r'~', '', text)     # Remove strikethrough markers if any
    return text

# Main function to interact with the user
def chatbot():
    print("Welcome! I'm your herbal remedy assistant. Describe your symptoms, and I'll provide possible diseases and plant-based or herbal medicine suggestions.")
    
    while True:
        # Get user input
        user_input = input("\nEnter symptoms (comma-separated) or type 'exit' to stop: ")

        if user_input.lower() == 'exit':
            confirmation = input("Are you sure you want to exit? (yes/no): ").lower()
            if confirmation == 'yes':
                print("Goodbye! Stay healthy with nature's remedies.")
                break
            else:
                continue

        # Clean the input
        cleaned_input = clean_input(user_input)

        # Check if the input is valid
        if not cleaned_input:
            print("Invalid input. Please describe your symptoms properly.")
            continue

        # Process user symptoms input
        user_symptoms = [symptom.strip() for symptom in cleaned_input.split(",")]

        # Provide feedback to the user
        print("\nProcessing your symptoms...")

        # Generate a domain-specific prompt for Cohere focused on herbal medicine and disease suggestions
        ai_prompt = f"""The user has the following symptoms: {', '.join(user_symptoms)}.
        First, identify potential diseases or health conditions that may be associated with these symptoms.
        Then, as an herbal medicine assistant, suggest plant-based herbal medicines or mixtures of herbs traditionally used in herbal or Ayurvedic treatments for these conditions.
        Focus only on natural remedies using herbs and plants, and avoid recommending any pharmaceutical or synthetic treatments."""

        # Get the AI response
        ai_response = get_ai_response(ai_prompt)

        # Remove markdown formatting from the AI response
        ai_response = remove_markdown(ai_response)

        # Display formatted response
        if ai_response:
            print("\n--- Possible Diseases and Herbal Remedy Suggestions ---\n")
            print(ai_response)
        else:
            print("Sorry, I couldn't generate a response. Please try again.")

# Run the chatbot
chatbot()
