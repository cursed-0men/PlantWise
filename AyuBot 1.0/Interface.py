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
    'stomach ache', 'toothache', 'urinary tract infection', 'vertigo', 'wound', 'yeast infection',
    'acne', 'anemia', 'bruising', 'chills', 'confusion', 'congestion', 'dehydration', 
    'dry mouth', 'fainting', 'hair loss', 'heartburn', 'hives', 'joint pain', 'numbness', 
    'swelling', 'weight loss', 'weight gain', 'shortness of breath', 'sneezing', 'tinnitus',
    'itching', 'loss of appetite', 'menstrual cramps', 'irregular periods', 'nail fungus', 
    'runny nose', 'shivering', 'skin rash', 'sweating', 'trembling', 'wheezing', 'abdominal pain', 
    'acid reflux', 'anaphylaxis', 'angina', 'anorexia', 'appendicitis', 'arrhythmia', 'arthritis', 
    'athlete’s foot', 'autoimmune disease', 'bed sores', 'bleeding', 'blisters', 'blurred vision', 
    'bone pain', 'breast pain', 'broken bone', 'burning sensation', 'calf pain', 'cancer', 
    'canker sores', 'chest pain', 'chronic fatigue', 'cirrhosis', 'colitis', 'conjunctivitis', 
    'coronary artery disease', 'cracked skin', 'cystitis', 'dandruff', 'deformity', 'dental pain', 
    'diabetes', 'digestive issues', 'discoloration', 'dislocation', 'diverticulitis', 
    'earache', 'edema', 'epilepsy', 'eye infection', 'fever blisters', 'flu', 'fracture', 
    'gallstones', 'gastritis', 'gastroenteritis', 'glaucoma', 'gout', 'gum disease', 'halitosis', 
    'hallucinations', 'hemorrhoids', 'hepatitis', 'hernia', 'high blood pressure', 'hormonal imbalance',
    'hyperthyroidism', 'hypoglycemia', 'hypothyroidism', 'immune deficiency', 'impetigo', 
    'incontinence', 'infertility', 'influenza', 'inner ear infection', 'iron deficiency', 
    'irritation', 'jaundice', 'kidney stones', 'knee pain', 'lactose intolerance', 'liver disease', 
    'low blood pressure', 'lumbar pain', 'lung infection', 'malaria', 'migraines', 'muscle cramps', 
    'muscle stiffness', 'myalgia', 'nausea', 'neck pain', 'nerve pain', 'night sweats', 'nosebleed', 
    'numbness', 'oral ulcers', 'osteoporosis', 'pancreatitis', 'paralysis', 'parkinson’s disease', 
    'pelvic pain', 'peripheral neuropathy', 'pharyngitis', 'pneumonia', 'prostate inflammation', 
    'psoriasis', 'rectal pain', 'respiratory infection', 'rheumatoid arthritis', 'sciatica', 
    'seizures', 'shingles', 'shortness of breath', 'sinus congestion', 'sinus headache', 'skin infection', 
    'slurred speech', 'sore gums', 'spinal cord injury', 'splinters', 'sprains', 'stiff neck', 'stomach cramps', 
    'stomach ulcer', 'stroke', 'swollen glands', 'swollen joints', 'thyroid disease', 'torn ligament', 
    'tooth infection', 'urinary infection', 'varicose veins', 'vomiting', 'warts', 'whiplash', 'yellow skin',
    'acute pain', 'adrenal fatigue', 'aids', 'amnesia', 'ant bites', 'apnea', 'arteriosclerosis', 
    'aspiration', 'back strain', 'bacterial infection', 'bedwetting', 'blackheads', 'bladder infection', 
    'blood clot', 'blood disorder', 'body aches', 'bowel obstruction', 'brain fog', 'breathing difficulty',
    'broken nose', 'bruxism', 'burnout', 'bursitis', 'cerebral palsy', 'chapped lips', 'childbirth pain', 
    'chronic pain', 'coughing blood', 'croup', 'cracked heels', 'crohn’s disease', 'dental abscess', 
    'diabetic neuropathy', 'difficulty swallowing', 'drooling', 'dry eyes', 'ear discharge', 'ear ringing', 
    'eclampsia', 'elevated cholesterol', 'endometriosis', 'enlarged spleen', 'esophagitis', 'eye redness', 
    'facial swelling', 'fall injury', 'febrile seizures', 'fibromyalgia', 'frostbite', 'gallbladder pain', 
    'gas pain', 'genital sores', 'groin pain', 'gurgling stomach', 'hand pain', 'head swelling', 
    'heavy menstrual bleeding', 'hip pain', 'hives', 'hoarseness', 'hot flashes', 'inability to urinate', 
    'inflammation', 'intestinal blockage', 'itchy eyes', 'jock itch', 'joint stiffness', 'knee swelling', 
    'labored breathing', 'lactation issues', 'laryngitis', 'leg cramps', 'liver pain', 'lupus', 'meningitis', 
    'mental confusion', 'methanol poisoning', 'mononucleosis', 'morning stiffness', 'motion sickness', 
    'mumps', 'muscle strain', 'nail discoloration', 'nervousness', 'night blindness', 'osteopenia', 
    'ovarian cyst', 'palpitations', 'pancreatic pain', 'pelvic cramps', 'peptic ulcer', 'phlebitis', 
    'pimples', 'pinched nerve', 'plantar fasciitis', 'pleurisy', 'poison ivy', 'poor circulation', 
    'postpartum depression', 'premenstrual syndrome', 'pulmonary embolism', 'quinsy', 'rectal bleeding', 
    'rectal itching', 'renal failure', 'restlessness', 'ringworm', 'rosacea', 'rotator cuff injury', 
    'scoliosis', 'self-harm injury', 'sensitivity to cold', 'sensitivity to light', 'shallow breathing', 
    'shock', 'skin burns', 'slurred speech', 'snoring', 'spinal disc herniation', 'stiff muscles', 
    'stomach bloating', 'subdural hematoma', 'sudden weight loss', 'tendonitis', 'testicular pain', 
    'tingling sensation', 'tongue swelling', 'tonsillitis', 'tooth decay', 'toxic shock', 'trigeminal neuralgia', 
    'ulcerative colitis', 'urethritis', 'urine retention', 'vaginal discharge', 'varicella', 'ventricular fibrillation', 
    'vertigo', 'viral infection', 'vision loss', 'vomiting blood', 'vulvar pain', 'weakness', 'whooping cough', 
    'yellowing of eyes', 'zoster infection', 'bile duct obstruction', 'facial numbness', 'fingernail injury', 
    'gastric bleeding', 'intestinal inflammation', 'joint cracking', 'knee dislocation', 'neuralgia', 
    'palsy', 'parotitis', 'radiculopathy', 'scar tissue pain', 'spinal stenosis', 'subconjunctival hemorrhage', 
    'tarsal tunnel syndrome', 'telangiectasia', 'tibial pain', 'toxemia', 'uremia', 'urticaria', 'vascular disease', 
    'ventricular tachycardia', 'weak pulse', 'wrist pain'
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
