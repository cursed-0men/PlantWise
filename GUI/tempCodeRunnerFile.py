import tkinter as tk
from tkinter import messagebox, Text
from tkinter import ttk

from main import predict_disease, symptom_list

# Function to handle the submission of symptoms
def on_submit(event=None):
    user_input = entry.get().lower().split(',')
    user_symptoms = [symptom.strip() for symptom in user_input]
    valid_symptoms = [symptom for symptom in user_symptoms if symptom in symptom_list]

    if not valid_symptoms:
        messagebox.showinfo("Result", "None of the symptoms are recognized. Please try again.")
        return

    predicted_disease, suggested_remedy = predict_disease(valid_symptoms)
    result_message = f"Most likely condition: {predicted_disease}\nSuggested remedy: {suggested_remedy}"
    result_box.config(state=tk.NORMAL)  # Enable the text box
    result_box.delete(1.0, tk.END)  # Clear the text box
    result_box.insert(tk.END, result_message)  # Insert the result message
    result_box.config(state=tk.DISABLED)  # Disable the text box for editing

# Create GUI
root = tk.Tk()
root.title("PlantWise")
root.geometry("800x600")  # Default window size

# Style configuration
style = ttk.Style()
style.configure('TLabel', font=('Arial', 14), padding=10)
style.configure('TEntry', font=('Arial', 12), padding=10)
style.configure('TButton',
                font=('Arial', 12, 'bold'),
                padding=[10, 20],
                relief='flat',
                background='#4CAF50',  # Green background
                foreground='white')
style.configure('TFrame', background='lightblue')

# Create main frame
frame = ttk.Frame(root, padding=20)
frame.pack(expand=True, fill=tk.BOTH)

# Title Label
title_label = tk.Label(frame, text="PlantWise", font=('Arial', 36, 'bold'), bg='lightblue', fg='#2E8B57')
title_label.pack(pady=(30, 20))  # Add padding at the top

# Input Label and Entry
input_label = ttk.Label(frame, text="Enter your symptoms (comma-separated):")
input_label.pack(pady=10)
entry = ttk.Entry(frame, width=60)
entry.pack(pady=5)

# Bind Enter key to submit action
root.bind('<Return>', on_submit)

# Submit Button
submit_button = tk.Button(frame, text="Submit", command=on_submit, font=('Arial', 12, 'bold'), 
                         bg='#4CAF50', fg='white', relief='flat', padx=20, pady=10)
submit_button.pack(pady=20)

# Response Text Box
result_box = Text(frame, wrap=tk.WORD, height=10, width=70, font=('Arial', 12), bg='lightgrey', borderwidth=2, relief='groove')
result_box.pack(pady=10)
result_box.insert(tk.END, "Results will be displayed here...")
result_box.config(state=tk.DISABLED)  # Make text box read-only

# Adjust layout for fullscreen
def on_resize(event):
    frame_width = event.width
    input_label.config(width=int(frame_width * 0.8))
    entry.config(width=int(frame_width * 0.8))
    result_box.config(width=int(frame_width * 0.8))
    submit_button.config(width=int(frame_width * 0.2))  # Adjust button width

root.bind('<Configure>', on_resize)

# Run the main loop
root.mainloop()
