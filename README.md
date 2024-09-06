# PlantWise
PlantWise is a tool for predicting diseases based on symptoms and suggesting Ayurvedic remedies.

## Features
Disease Prediction: Uses a RandomForestClassifier to identify potential diseases from symptoms.
Ayurvedic Remedies: Suggests natural remedies for the predicted disease.
User-Friendly Interface: Easy-to-use GUI for symptom input and results display.
## Components
main.py:
- Loads and preprocesses data.
- Trains a machine learning model.
- Predicts disease and provides remedies.<br>

gui.py:
- Creates a graphical interface using Tkinter.
- Handles user input and displays results.<br>

dataset.csv:
- Contains symptoms, diseases, and Ayurvedic remedies.

Enter symptoms in the text field and click "Submit" to see predictions and remedies.

## Future Plans
- Expand the dataset for better accuracy.
- Explore advanced machine learning models.
- Add user feedback to improve predictions.
