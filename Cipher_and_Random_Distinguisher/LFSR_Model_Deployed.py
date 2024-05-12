import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import torch
import re
import pickle
from custom_utility import *
# Load the model from the file
with open('Saved_Model_Weights/model_LFSR.pkl', 'rb') as f:
    model_LFSR = pickle.load(f)
# Function to test the ciphertext
def test_ciphertext():
    # Get the input mode
    input_mode = input_mode_var.get()

    # Get the ciphertext from the entry field based on the input mode
    if input_mode == "Generate":
        length = int(ciphertext_entry_l.get())
        ciphertext = generate_pseudo_random_code(length)
    elif input_mode == "Input":
        ciphertext = ciphertext_entry_l.get()
    elif input_mode == "Encrypt":
        ciphertext=encrypt(ciphertext_entry_l.get(),polynomial=[5,4,3,2], initial_state=[1,0,1,0,1])
    else:
        messagebox.showerror("Error", "Invalid input mode selected.")
        return

    # Preprocess the ciphertext
    preprocessed_ciphertext = torch.tensor([int(c) for c in ciphertext]).unsqueeze(0).unsqueeze(2).float()

    # Test the model
    model_LFSR.eval()
    with torch.no_grad():
        output = model_LFSR(preprocessed_ciphertext)
        _, predicted_class = torch.max(output, 1)

    # Convert predicted class to label
    predicted_label = "Random" if predicted_class.item() == 1 else "Ciphertext"
    
    # Show the result
    messagebox.showinfo("Prediction Result", f"The provided ciphertext is classified as: {predicted_label}")

# Check if input is an integer, string, or binary
def is_non_binary_int_or_string(input_value):
    # Check if input is an integer
    if isinstance(input_value, int):
        # Check if input is a binary integer
        if re.match(r'^[01]+$', str(input_value)):
            return False
        else:
            return True
    # Check if input is a string
    elif isinstance(input_value, str):
        return False
    else:
        return False

# Create the main application window
root = tk.Tk()
root.title("Ciphertext Classification")

# Create a frame to hold the input fields and buttons
input_frame = ttk.Frame(root, padding="10")
input_frame.grid(row=0, column=0, padx=10, pady=10)

# Create a label and entry field for the ciphertext
ciphertext_label = ttk.Label(input_frame, text="Generate Ciphertext / Input Ciphertext:")
ciphertext_label.grid(row=1, column=0, sticky="W")
ciphertext_entry_l = ttk.Entry(input_frame, width=50)
ciphertext_entry_l.grid(row=1, column=1, padx=(0, 10))

# Create a radio button to choose input mode
input_mode_var = tk.StringVar(value="Generate")
input_mode_generate = ttk.Radiobutton(input_frame, text="Generate", variable=input_mode_var, value="Generate")
input_mode_generate.grid(row=0, column=0, sticky="W")

input_mode_input = ttk.Radiobutton(input_frame, text="Encrypt Text", variable=input_mode_var, value="Encrypt")
input_mode_input.grid(row=0, column=1, sticky="W")

input_mode_input = ttk.Radiobutton(input_frame, text="Input", variable=input_mode_var, value="Input")
input_mode_input.grid(row=0, column=2, sticky="W")

# Create a button to test the ciphertext
test_button = ttk.Button(input_frame, text="Test Ciphertext", command=test_ciphertext)
test_button.grid(row=2, column=3, rowspan=2)

# Run the application
root.mainloop()