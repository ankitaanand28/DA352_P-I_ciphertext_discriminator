#ml_training_dataset_creation.py
from custom_utility import *
import numpy as np
import pandas as pd
ciphertext_1_df=pd.read_csv("ciphertext_set01.csv")
ciphertext_2_df=pd.read_csv("ciphertext_set02.csv")
random_ciphertext_1_df=pd.read_csv("random_ciphertexts_set01.csv")
random_ciphertext_2_df=pd.read_csv("random_ciphertexts_set02.csv")
ciphertext_1=ciphertext_1_df['Encrypted Text (Binary)'].values
ciphertext_2=ciphertext_2_df['Encrypted Text (Binary)'].values
random_ciphertext_1=random_ciphertext_1_df['Pseudo-Random Code (Binary)'].values
random_ciphertext_2=random_ciphertext_2_df['Pseudo-Random Code (Binary)'].values

is_ciphertext = [0] * (len(ciphertext_1) + len(ciphertext_2))
is_random = [1] * len(random_ciphertext_1) + [1] * len(random_ciphertext_2)

# Combine data into a DataFrame
data = {
    'Ciphertext': list(ciphertext_1) + list(ciphertext_2) + list(random_ciphertext_1) + list(random_ciphertext_2),
    'IsRandom': is_ciphertext + is_random
}

df = pd.DataFrame(data)
# Shuffle the DataFrame
df = df.sample(frac=1).reset_index(drop=True)
# Print the DataFrame
print(df)
# save the DataFrame to a CSV file
df.to_csv('lfsr_ciphertext_distinguisher_dataset.csv', index=False)