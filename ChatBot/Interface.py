import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
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

# PyQt5 Interface for the Chatbot
class HerbalAssistant(QWidget):
    def __init__(self):
        super().__init__()

        # Setting up the GUI layout
        self.init_ui()

    def init_ui(self):
        # Main layout
        layout = QVBoxLayout()

        # Instructions label
        self.label = QLabel('Welcome to the Herbal Remedy Assistant. Enter symptoms (comma-separated) and press Submit:')
        layout.addWidget(self.label)

        # Text input for symptoms
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText('Enter symptoms, e.g., headache, nausea, fatigue')
        layout.addWidget(self.input_field)

        # Button to submit the symptoms
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.handle_input)
        layout.addWidget(self.submit_button)

        # Output field for the AI response
        self.output_field = QTextEdit(self)
        self.output_field.setReadOnly(True)
        layout.addWidget(self.output_field)

        # Set the main layout
        self.setLayout(layout)

        # Window settings
        self.setWindowTitle('Herbal Remedy Assistant')
        self.setGeometry(400, 200, 600, 400)
        self.show()

    def handle_input(self):
        user_input = self.input_field.text().lower()

        # Check if input is within the herbal medicine domain
        if not is_in_domain(user_input):
            self.output_field.setText("The question seems to be out of scope. Please ask about symptoms, herbal treatments, or related health conditions.")
        else:
            # Process user symptoms input
            user_symptoms = [symptom.strip() for symptom in user_input.split(",")]

            # Generate AI prompt
            ai_prompt = f"""The user has the following symptoms: {', '.join(user_symptoms)}.
            First, identify potential diseases or health conditions that may be associated with these symptoms.
            Then, as an herbal medicine assistant, suggest plant-based herbal medicines or mixtures of herbs traditionally used in herbal or Ayurvedic treatments for these conditions.
            Focus only on natural remedies using herbs and plants, and avoid recommending any pharmaceutical or synthetic treatments."""

            # Get AI response
            ai_response = get_ai_response(ai_prompt)
            self.output_field.setText(f"Possible Diseases and Herbal Remedy Suggestions:\n\n{ai_response}")

# Main application
def run_app():
    app = QApplication(sys.argv)
    assistant = HerbalAssistant()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_app()
