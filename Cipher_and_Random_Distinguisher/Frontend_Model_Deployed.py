import pickle
from custom_utility import *
# Load the model from the file
with open('Saved_Model_Weights/model_LFSR.pkl', 'rb') as f:
    model_LFSR = pickle.load(f)
with open('Saved_Model_Weights/model_Fiestel.pkl', 'rb') as f:
    model_Fiestel = pickle.load(f)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import torch
import re


# Generate random text and encrypt it using Feistel cipher
def generate_random_text(length):
    random_text = ''
    for _ in range(length):
        random_char = chr(random.randint(32, 126))  # ASCII range for printable characters
        random_text += random_char
    return random_text





def test_lfsr_ciphertext():
    # Implementation of LFSR ciphertext testing
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

# Functions for Fiestal Cipher



def test_fiestal_ciphertext():
    # Get the input mode
    input_mode = input_mode_var.get()

    # Get the ciphertext from the entry field based on the input mode
    if input_mode == "Encrypt" :
        key = rand_key(len(ciphertext_entry_l.get()) * 8 // 2)
        ciphertext = feistel_cipher(ciphertext_entry_l.get(),key)

    elif input_mode == "Input":
        ciphertext = ciphertext_entry_l.get()
    elif input_mode=="Generate":
        # Generate random text and real words
        length = int(ciphertext_entry_l.get())
        key = rand_key(length * 8 // 2)
        ciphertext =  feistel_cipher(generate_random_text(random.randint(5,8)) ,key)
    else:
        messagebox.showerror("Error", "Invalid input mode selected.")
        return

    # Preprocess the ciphertext
    preprocessed_ciphertext = torch.tensor([int(c) for c in ciphertext]).unsqueeze(0).unsqueeze(2).float()

    # Test the model
    model_Fiestel.eval()
    with torch.no_grad():
        output = model_Fiestel(preprocessed_ciphertext)
        _, predicted_class = torch.max(output, 1)

    # Convert predicted class to label
    predicted_label = "Random" if predicted_class.item() == 1 else "Ciphertext"
    
    # Show the result
    messagebox.showinfo("Prediction Result", f"The provided ciphertext is classified as: {predicted_label}")

# Function to test ciphertext based on selected mode
def test_ciphertext():
    # Get the selected cipher mode
    cipher_mode = cipher_mode_var.get()

    # Test LFSR ciphertext
    if cipher_mode == "LFSR":
        test_lfsr_ciphertext()
    # Test Fiestal ciphertext
    elif cipher_mode == "Fiestel":
        test_fiestal_ciphertext()
    else:
        messagebox.showerror("Error", "Invalid cipher mode selected.")

# Create the main application window
root = tk.Tk()
root.title("Ciphertext Classification")

# Create a frame for LFSR cipher
lfsr_frame = ttk.Frame(root, padding="10")
lfsr_frame.grid(row=0, column=0, padx=10, pady=10)

# Create widgets for LFSR cipher
ciphertext_label = ttk.Label(lfsr_frame, text="Generate Ciphertext / Input Ciphertext:")
ciphertext_label.grid(row=2, column=0, sticky="W")
ciphertext_entry_l = ttk.Entry(lfsr_frame, width=50)
ciphertext_entry_l.grid(row=2, column=1, padx=(0, 10))

input_mode_var = tk.StringVar(value="Generate")
input_mode_generate = ttk.Radiobutton(lfsr_frame, text="Generate", variable=input_mode_var, value="Generate")
input_mode_generate.grid(row=1, column=0, sticky="W")

input_mode_input = ttk.Radiobutton(lfsr_frame, text="Encrypt Text", variable=input_mode_var, value="Encrypt")
input_mode_input.grid(row=1, column=1, sticky="W")

input_mode_input = ttk.Radiobutton(lfsr_frame, text="Input", variable=input_mode_var, value="Input")
input_mode_input.grid(row=1, column=2, sticky="W")

# Create a frame for Fiestal cipher
fiestal_frame = ttk.Frame(root, padding="10")
fiestal_frame.grid(row=0, column=1, padx=10, pady=10)

# Create widgets for Fiestal cipher


# Create a radio button to choose cipher mode
cipher_mode_var = tk.StringVar(value="LFSR")
lfsr_mode_radiobutton = ttk.Radiobutton(root, text="LFSR", variable=cipher_mode_var, value="LFSR")
lfsr_mode_radiobutton.grid(row=0, column=2, sticky="W")

fiestal_mode_radiobutton = ttk.Radiobutton(root, text="Fiestal", variable=cipher_mode_var, value="Fiestel")
fiestal_mode_radiobutton.grid(row=0, column=3, sticky="W")

# Create a button to test the ciphertext
test_button = ttk.Button(root, text="Test Ciphertext", command=test_ciphertext)
test_button.grid(row=4, columnspan=3)

# Run the application
root.mainloop()

