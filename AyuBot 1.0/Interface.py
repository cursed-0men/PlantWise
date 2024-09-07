import sys
import re
import cohere
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor

# Replace with your Cohere API key
API_KEY = 'KTn7ndyWTyFbx9yGwzrS27JYOy0TRjttcObYzk5t'

# Initialize the Cohere client
co = cohere.Client(API_KEY)

# A large list of keywords related to herbal medicine, symptoms, conditions, and treatments
HERBAL_KEYWORDS = [
    'herb', 'plant', 'ayurveda', 'symptom', 'disease', 'treatment', 'remedy', 'medicine',
    'condition', 'health', 'wellness', 'fatigue', 'pain', 'nausea', 'infection', 'migraine',
    'cold', 'fever', 'headache', 'cough', 'sore throat', 'diarrhea', 'vomiting', 'allergy',
    'anxiety', 'depression', 'arthritis', 'asthma', 'back pain', 'bloating', 'bronchitis',
    'burns', 'constipation', 'cramps', 'dizziness', 'eczema', 'indigestion', 'insomnia',
    'irritable bowel syndrome', 'muscle pain', 'psoriasis', 'rashes', 'sinusitis', 'stress',
    'stomach ache', 'toothache', 'urinary tract infection', 'vertigo', 'wound', 'yeast infection'
    # (Add more keywords as needed)
]

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

# Function to clean and format the user's input
def clean_input(user_input):
    # Remove any extra spaces, special characters, and lowercase the input
    user_input = re.sub(r'[^a-zA-Z, ]', '', user_input).lower().strip()
    return user_input

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
        self.label = QLabel('Enter your symptoms (comma-separated), and I will suggest possible diseases and remedies:')
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
        self.output_field.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.output_field)

        # Set the main layout
        self.setLayout(layout)

        # Window settings
        self.setWindowTitle('Herbal Remedy Assistant')
        self.setGeometry(400, 200, 600, 500)
        self.show()

    def handle_input(self):
        # Clean and process user input
        user_input = self.input_field.text().lower()
        cleaned_input = clean_input(user_input)

        if not cleaned_input:
            self.output_field.setHtml("<p style='color:red;'>Invalid input. Please enter your symptoms properly.</p>")
            return

        if not is_in_domain(cleaned_input):
            self.output_field.setHtml("<p style='color:red;'>Out of scope. Please ask about symptoms, herbal treatments, or related health conditions.</p>")
            return

        user_symptoms = [symptom.strip() for symptom in cleaned_input.split(",")]

        # Generate AI prompt
        ai_prompt = f"""The user has the following symptoms: {', '.join(user_symptoms)}.
        First, identify potential diseases or health conditions that may be associated with these symptoms.
        Then, as an herbal medicine assistant, suggest plant-based herbal medicines or mixtures of herbs traditionally used in herbal or Ayurvedic treatments for these conditions.
        Focus only on natural remedies using herbs and plants, and avoid recommending any pharmaceutical or synthetic treatments."""

        # Get AI response
        ai_response = get_ai_response(ai_prompt)

        # Display AI response
        if ai_response:
            self.output_field.setHtml(f"<h2>Possible Diseases and Herbal Remedy Suggestions</h2><p>{ai_response}</p>")
        else:
            self.output_field.setHtml("<p style='color:red;'>An error occurred. Please try again.</p>")

# Main function to run the PyQt5 app
def run_app():
    app = QApplication(sys.argv)
    assistant = HerbalAssistant()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_app()
