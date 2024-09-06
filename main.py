import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from collections import Counter

# Load the dataset
data = pd.read_csv('dataset.csv')  # Update the path if necessary

# Combine the symptom columns into a single list of symptoms for each row
data['Symptoms'] = data[['Symptom 1', 'Symptom 2', 'Symptom 3']].apply(lambda row: list(row.dropna()), axis=1)

# Create a set of all symptoms from the dataset
symptom_list = set(sum(data['Symptoms'].tolist(), []))

# Create a frequency map for symptoms across diseases (for weighting purposes)
symptom_frequency = Counter(sum(data['Symptoms'].tolist(), []))

# Function to create a binary vector for symptoms with weighting
def symptom_vector(symptoms):
    vector = [1 if symptom in symptoms else 0 for symptom in symptom_list]
    return vector

# Prepare features (X) and labels (y)
X = data['Symptoms'].apply(symptom_vector).tolist()
y = data['Disease']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Map diseases to Ayurvedic Remedies
remedies = dict(zip(data['Disease'], data['Ayurvedic Remedy']))

# Optimized chatbot logic with symptom count feedback and debug output
def chatbot(user_symptoms_input=None):
    if user_symptoms_input:
        user_input = user_symptoms_input
    else:
        print("Hello! I'm your personal health assistant. You can describe your symptoms, and I'll try to diagnose a possible condition.")
        user_input = input("\nEnter symptoms (comma-separated) or type 'exit' to stop: ").lower()
        
        if user_input == 'exit':
            print("Goodbye! Take care.")
            return None, None

    # Process user symptoms input
    user_symptoms = [symptom.strip() for symptom in user_input.split(",")]

    # Validate the symptoms against the known symptoms from the dataset
    valid_symptoms = [symptom for symptom in user_symptoms if symptom in symptom_list]

    if not valid_symptoms:
        print("It seems that none of the symptoms you entered are recognized. Please try again with different symptoms.")
        return None, None

    # Check number of symptoms provided and offer feedback
    if len(valid_symptoms) == 1:
        print("\nNote: You've entered only one symptom. While I'll still provide a diagnosis, adding more symptoms could improve accuracy.")
    elif len(valid_symptoms) == 2:
        print("\nNote: You've entered only two symptoms. The more symptoms you provide, the better the diagnosis might be.")

    # Predict the disease based on valid symptoms
    symptom_vec = symptom_vector(valid_symptoms)
    probabilities = model.predict_proba([symptom_vec])[0]
    top_indices = probabilities.argsort()[-3:][::-1]  # Get top 3 predictions
    top_diseases = model.classes_[top_indices]

    # Debug: Print probabilities for top diseases
    print(f"Prediction probabilities: {[(model.classes_[i], probabilities[i]) for i in top_indices]}")

    # Weighted scoring based on symptom match
    disease_score = {}
    for disease in top_diseases:
        symptom_count = sum([1 for symptom in valid_symptoms if symptom in data[data['Disease'] == disease].Symptoms.iloc[0]])
        weight = sum([symptom_frequency[symptom] for symptom in valid_symptoms])
        disease_score[disease] = symptom_count / weight

    # Get the top disease based on symptom match scores
    predicted_disease = max(disease_score, key=disease_score.get)
    suggested_remedy = remedies.get(predicted_disease, "No remedy found")

    if not user_symptoms_input:  # Only print if it's a chatbot interaction
        print(f"\nBased on the symptoms you provided, the most likely condition is: \033[91m{predicted_disease}.\033[0m")
        print(f"\033[92mSuggested Ayurvedic remedy: {suggested_remedy}\033[0m")
        '''print("\nOther possible conditions include:")
        for disease in top_diseases[1:]:
            print(f"- {disease} (probability: {probabilities[top_indices[top_diseases.tolist().index(disease)]]:.2f})")'''

    return predicted_disease, suggested_remedy

chatbot()
