# import LFSR
from pylfsr import LFSR
import random
import pandas as pd
import numpy as np
import re
import random


# Random bits key generation
def rand_key(p):
    key1 = ""
    p = int(p)
    for i in range(p):
        temp = random.randint(0, 1)
        temp = str(temp)
        key1 = key1 + temp
    return key1

# Function to implement bit exor
def exor(a, b):
    temp = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            temp += "0"
        else:
            temp += "1"
    return temp

# Defining BinarytoDecimal() function
def BinaryToDecimal(binary):
    string = int(binary, 2)
    return string

# Feistel Cipher
def feistel_cipher(PT, key):
    # Converting the plain text to ASCII
    PT_Ascii = [ord(x) for x in PT]

    # Converting the ASCII to 8-bit binary format
    PT_Bin = [format(y, '08b') for y in PT_Ascii]
    PT_Bin = "".join(PT_Bin)

    n = int(len(PT_Bin) // 2)
    L1 = PT_Bin[0:n]
    R1 = PT_Bin[n::]
    m = len(R1)

    # first round of Feistel
    f1 = exor(R1, key)
    R2 = exor(f1, L1)
    L2 = R1

    # Second round of Feistel
    f2 = exor(R2, key)
    R3 = exor(f2, L2)
    L3 = R2

    # Cipher text
    bin_data = L3 + R3
    return bin_data

#To check if it is binary digits (0s and 1s)
def is_binary(s):
    # Regular expression to match binary string
    pattern = "^[01]+$"
    
    # Check if the input string matches the pattern
    if re.match(pattern, s):
        return True
    else:
        return False
    
#To check if a string contains characters other than integers or binary digits (0s and 1s)
def contains_non_int_or_binary(s):
    # Regular expression to match non-integer or non-binary characters
    pattern = "[^01\d]"

    # Check if the input string contains non-integer or non-binary characters
    if re.search(pattern, s):
        return True
    else:
        return False
    


# to check for integer
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



# Function to convert text to binary
def text_to_binary(text):
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    return binary_text

# Function to convert binary to text
def binary_to_text(binary_string):
    # Split the binary string into 8-bit chunks
    chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    # Convert each 8-bit chunk to its corresponding ASCII character and join them together
    text = ''.join(chr(int(chunk, 2)) for chunk in chunks)
    return text

# Function to encrypt text using LFSR
def encrypt(text, polynomial=[5,4,3,2], initial_state=[1,0,1,0,1]):
    # Convert text to binary
    binary_text = text_to_binary(text)
    
    # Initialize LFSR
    lfsr = LFSR(fpoly=polynomial, initstate=initial_state)
    
    # Generate keystream
    keystream = ""
    for _ in range(len(binary_text)):
        lfsr.next()
        keystream += str(lfsr.state[-1])
    
    # Encrypt text by XORing with keystream
    encrypted_text = ""
    for i in range(len(binary_text)):
        encrypted_bit = str(int(binary_text[i]) ^ int(keystream[i]))
        encrypted_text += encrypted_bit
    
    return encrypted_text

# Function to decrypt text using LFSR
def decrypt(encrypted_text, polynomial=[5,4,3,2], initial_state=[1,0,1,0,1]):
    # Initialize LFSR
    lfsr = LFSR(fpoly=polynomial, initstate=initial_state)
    
    # Generate keystream
    keystream = ""
    for _ in range(len(encrypted_text)):
        lfsr.next()
        keystream += str(lfsr.state[-1])
    
    # Decrypt text by XORing with keystream
    decrypted_text = ""
    for i in range(len(encrypted_text)):
        decrypted_bit = str(int(encrypted_text[i]) ^ int(keystream[i]))
        decrypted_text += decrypted_bit
    
    return decrypted_text

def generate_pseudo_random_code(length):
    # Define the polynomial and initial state for the LFSR
    polynomial = [5, 4, 3, 2]
    initial_state = [random.randint(0, 1) for _ in range(max(polynomial)-1)]
    initial_state.append(1) #Initial state vector can not be All Zeros
    
    # Initialize the LFSR
    lfsr = LFSR(fpoly=polynomial, initstate=initial_state)
    
    # Generate binary sequence
    binary_sequence = ''.join(str(lfsr.next()) for _ in range(length))
    
    return binary_sequence

def length_generator(filepath):
    ciphertext=pd.read_csv(filepath)
    encrypted_text_length=np.array([len(x) for x in ciphertext['Encrypted Text (Binary)'].values])
    encrypted_text_max=encrypted_text_length.max()
    encrypted_text_min=encrypted_text_length.min()
    return random.randint(encrypted_text_min, encrypted_text_max) # Length of the pseudo-random code