import tkinter as tk
from tkinter import Text, messagebox, ttk
from PIL import Image, ImageTk
from main import predict_disease, symptom_list

def on_submit(event=None):
    user_input = entry.get().lower().split(",")
    user_symptoms = [symptom.strip() for symptom in user_input]
    valid_symptoms = [symptom for symptom in user_symptoms if symptom in symptom_list]

    if not valid_symptoms:
        messagebox.showinfo(
            "Result", "None of the symptoms are recognized. Please try again."
        )
        return
    predicted_disease, suggested_remedy = predict_disease(valid_symptoms)
    result_message = f"Most likely condition: {predicted_disease}\nSuggested remedy: {suggested_remedy}"
    result_box.config(state=tk.NORMAL) 
    result_box.delete(1.0, tk.END)  
    result_box.insert(tk.END, result_message)  
    result_box.config(state=tk.DISABLED)  

def resize_background_image(event):
    global background_image_tk, background_image_resized
    scale_factor = 1.5 
    new_size = (int(event.width * scale_factor), int(event.height * scale_factor))
    background_image_resized = background_image.resize(
        new_size, Image.Resampling.LANCZOS
    )
    background_image_tk = ImageTk.PhotoImage(background_image_resized)
    canvas.config(width=new_size[0], height=new_size[1])
    canvas.create_image(0, 0, anchor=tk.NW, image=background_image_tk)
    canvas.lower("bg_image") 


root = tk.Tk()
root.title("PlantWise")
root.geometry("800x600")  
background_image = Image.open("background.jpg")
initial_size = (1200, 900)  
background_image_resized = background_image.resize(
    initial_size, Image.Resampling.LANCZOS
)
background_image_tk = ImageTk.PhotoImage(background_image_resized)

canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)
canvas.create_image(0, 0, anchor=tk.NW, image=background_image_tk, tags="bg_image")
frame = ttk.Frame(canvas, padding=20)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.8, relheight=0.8)

# Style configuration
style = ttk.Style()
style.configure("TLabel", font=("Arial", 14), padding=10)
style.configure("TEntry", font=("Arial", 12), padding=10)
style.configure(
    "TButton",
    font=("Arial", 12, "bold"),
    padding=[10, 20],
    relief="flat",
    background="#4CAF50", 
    foreground="white",
)
style.configure("TFrame", background="lightblue")

title_label = tk.Label(
    frame, text="PlantWise", font=("Arial", 36, "bold"), bg="lightblue", fg="#2E8B57"
)
title_label.pack(pady=(30, 20))

input_label = ttk.Label(frame, text="Enter your symptoms (eg: cough, fever, sore throat):")
input_label.pack(pady=10)
entry = ttk.Entry(frame, width=60)
entry.pack(pady=5)
root.bind("<Return>", on_submit)

# Submit Button
submit_button = tk.Button(
    frame,
    text="Submit",
    command=on_submit,
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    relief="flat",
    padx=20,
    pady=10,
)
submit_button.pack(pady=20)

# Response Text Box
result_box = Text(
    frame,
    wrap=tk.WORD,
    height=10,
    width=70,
    font=("Arial", 12),
    bg="lightgrey",
    borderwidth=2,
    relief="groove",
)
result_box.pack(pady=10)
result_box.insert(tk.END, "Results will be displayed here...")
result_box.config(state=tk.DISABLED)

# Adjust layout for resizing
def on_resize(event):
    resize_background_image(event)
    frame_width = event.width * 0.8
    input_label.config(width=int(frame_width * 0.8))
    entry.config(width=int(frame_width * 0.8))
    result_box.config(width=int(frame_width * 0.8))
    submit_button.config(width=int(frame_width * 0.2))

root.bind("<Configure>", on_resize)
root.mainloop()
