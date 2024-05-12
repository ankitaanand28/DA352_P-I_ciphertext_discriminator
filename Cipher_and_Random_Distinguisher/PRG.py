from pylfsr import LFSR
import random
import string
from custom_utility import *
import pandas as pd
import numpy as np



# Create lists to store the generated data
ciphertexts = []
lengths = []
pseudo_random_codes = []

# Generate 321 random ciphertexts
num_ciphertexts = 322
for i in range(num_ciphertexts):
    length = length_generator("ciphertext_set02.csv")
    pseudo_random_code = generate_pseudo_random_code(length)
    ciphertexts.append("Ciphertext " + str(i+1))
    lengths.append(length)
    pseudo_random_codes.append(pseudo_random_code)

# Create a DataFrame
data = {
    'Ciphertext': ciphertexts,
    'Length': lengths,
    'Pseudo-Random Code (Binary)': pseudo_random_codes
}
df = pd.DataFrame(data)

# Print the DataFrame
print(df)

# save the DataFrame to a CSV file
df.to_csv('Dataset_LFSR/random_ciphertexts_set02.csv', index=False)

