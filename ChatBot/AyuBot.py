import cohere

# Replace with your Cohere API key
API_KEY = 'KTn7ndyWTyFbx9yGwzrS27JYOy0TRjttcObYzk5t'

# Initialize the Cohere client
co = cohere.Client(API_KEY)

# List of keywords related to herbal medicine and symptoms (used for checking domain relevance)
HERBAL_KEYWORDS = ['herb', 'plant', 'symptom', 'disease', 'treatment', 'remedy', 'medicine', 'condition', 'health', 'wellness', 'ayurveda', 'fatigue', 'pain', 'nausea', 'infection', 'migraine', 'cold', 'fever']

# Function to check if the input is relevant to the domain
def is_in_domain(user_input):
    return any(keyword in user_input for keyword in HERBAL_KEYWORDS)

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

# Main function to interact with the user
def chatbot():
    print("Welcome! I'm your herbal remedy assistant. Describe your symptoms, and I'll provide possible diseases and plant-based or herbal medicine suggestions.")
    
    while True:
        # Get user input
        user_input = input("\nEnter symptoms (comma-separated) or type 'exit' to stop: ").lower()

        if user_input == 'exit':
            print("Goodbye! Stay healthy with nature's remedies.")
            break

        # Check if the input is within the herbal medicine domain
        if not is_in_domain(user_input):
            print("The question seems to be out of scope. Please ask about symptoms, herbal treatments, or related health conditions.")
            continue

        # Process user symptoms input
        user_symptoms = [symptom.strip() for symptom in user_input.split(",")]

        # Generate a domain-specific prompt for Cohere focused on herbal medicine and disease suggestions
        ai_prompt = f"""The user has the following symptoms: {', '.join(user_symptoms)}.
        First, identify potential diseases or health conditions that may be associated with these symptoms.
        Then, as an herbal medicine assistant, suggest plant-based herbal medicines or mixtures of herbs traditionally used in herbal or Ayurvedic treatments for these conditions.
        Focus only on natural remedies using herbs and plants, and avoid recommending any pharmaceutical or synthetic treatments."""

        # Get the AI response
        ai_response = get_ai_response(ai_prompt)
        print(f"\nPossible Diseases and Herbal Remedy Suggestions: {ai_response}\n")

# Run the chatbot
chatbot()
