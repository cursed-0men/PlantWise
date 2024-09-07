# main.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from collections import Counter

# Load and preprocess the dataset
data = pd.read_csv('dataset.csv')

# Combine symptom columns into a list
data['Symptoms'] = data[['Symptom 1', 'Symptom 2', 'Symptom 3']].apply(lambda row: list(row.dropna()), axis=1)

# Create a set of all symptoms
symptom_list = set(sum(data['Symptoms'].tolist(), []))

# Create a frequency map for symptoms across diseases
symptom_frequency = Counter(sum(data['Symptoms'].tolist(), []))

# Function to create a binary vector for symptoms
def symptom_vector(symptoms):
    return [1 if symptom in symptoms else 0 for symptom in symptom_list]

# Prepare features and labels
X = data['Symptoms'].apply(symptom_vector).tolist()
y = data['Disease']

# Train the RandomForestClassifier
model = RandomForestClassifier()
model.fit(X, y)

# Map diseases to Ayurvedic Remedies
remedies = dict(zip(data['Disease'], data['Ayurvedic Remedy']))

def predict_disease(symptoms):
    symptom_vec = symptom_vector(symptoms)
    probabilities = model.predict_proba([symptom_vec])[0]
    top_indices = probabilities.argsort()[-3:][::-1]
    top_diseases = model.classes_[top_indices]

    # Weighted scoring based on symptom match
    disease_score = {}
    for disease in top_diseases:
        symptom_count = sum([1 for symptom in symptoms if symptom in data[data['Disease'] == disease].Symptoms.iloc[0]])
        weight = sum([symptom_frequency[symptom] for symptom in symptoms])
        disease_score[disease] = symptom_count / weight

    predicted_disease = max(disease_score, key=disease_score.get)
    return predicted_disease, remedies.get(predicted_disease, "No remedy found")
