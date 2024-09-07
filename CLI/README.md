# 🌿 **PlantWise**  
*Your Ayurvedic Health Companion for Disease Prediction and Natural Remedies*  

---

## 🌟 **Overview**  
**PlantWise** is a machine learning tool designed to predict diseases based on symptoms and offer <strong style="color:#90EE90;">Ayurvedic remedies</strong>. Its <strong style="color:#7093fa;">user-friendly interface</strong> makes it easy to input symptoms and receive predictions along with natural treatments.

---

## ✨ **Key Features**  

- **🔍 Disease Prediction:**  
   Utilizes a <strong style="color:#90EE90;">RandomForestClassifier</strong> to predict potential diseases from a list of user-provided symptoms.  
   
- **🌱 Ayurvedic Remedies:**  
   Suggests <strong style="color:#90EE90;">effective</strong>, natural remedies based on the predicted diseases using traditional Ayurvedic knowledge.

- **💻 User-Friendly Interface:**  
   Offers an <strong style="color:#7093fa;">intuitive graphical interface</strong> for symptom input and instant remedy suggestions.

---

## 🛠 **Project Components**  

### `main.py`
- <strong style="color:#4974f5;">Loads and preprocesses</strong> the dataset.
- Trains a machine learning model using <strong style="color:#90EE90;">RandomForest</strong>.
- <strong style="color:#4974f5;">Predicts diseases</strong> and provides corresponding Ayurvedic remedies.

### `gui.py`
- Built using <strong style="color:#7093fa;">Tkinter</strong> to create a simple yet effective GUI.
- Handles <strong style="color:#4974f5;">user inputs</strong>, processes symptom data, and displays <strong style="color:#4974f5;">predictions and remedies</strong>.

### `dataset.csv`
- A structured dataset containing <strong style="color:#4974f5;">symptoms, diseases, and Ayurvedic remedies</strong>.

---

## 🧑‍💻 **How to Use**  

1. <strong style="color:#7093fa;">Enter symptoms</strong> in the input field on the GUI.
2. Click the <strong style="color:#7093fa;">"Submit"</strong> button to get the <strong style="color:#4974f5;">disease prediction</strong>.
3. Receive <strong style="color:#90EE90;">Ayurvedic remedies</strong> for the predicted disease.

---

## 🚀 **Future Enhancements**  

- <strong style="color:#90EE90;">Expand the dataset</strong> to improve <strong style="color:#4974f5;">prediction accuracy</strong>.
- <strong style="color:#90EE90;">Explore advanced machine learning models</strong> for more precise predictions.
- <strong style="color:#90EE90;">Incorporate user feedback</strong> for continuous improvement of the tool.
