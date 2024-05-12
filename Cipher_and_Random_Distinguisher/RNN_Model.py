
import torch
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
import torch.nn as nn
import torch.optim as optim
import pandas as pd

# Define a custom dataset class
class CipherDataset(Dataset):
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        ciphertext = self.data.iloc[idx, 0]
        is_random = self.data.iloc[idx, 1]
        return torch.tensor([int(c) for c in ciphertext]), is_random
# Modify the data loading process to pad sequences
def collate_fn(batch):
    ciphertexts, labels = zip(*batch)
    ciphertexts_padded = pad_sequence(ciphertexts, batch_first=True, padding_value=0)
    return ciphertexts_padded, torch.tensor(labels)



# Model Architecture for LFSR

class RNNClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(RNNClassifier, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.rnn(x, h0)
        out = self.fc(out[:, -1, :])
        return out
    
# Model Architecture for Fiestel

class RNNClassifier_fiestel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(RNNClassifier_fiestel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)  # Add dropout for regularization
        self.fc1 = nn.Linear(hidden_size, hidden_size)  # Add an additional fully connected layer
        self.relu = nn.ReLU()  # Add a ReLU activation function
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        batch_size = x.size(0)  # Get the batch size
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_size).to(x.device)  # Initialize the hidden state

        out, _ = self.rnn(x, h0)  # Pass the input and hidden state to the RNN
        out = self.fc1(out[:, -1, :])  # Pass the output of the last time step to the first fully connected layer
        out = self.relu(out)  # Apply ReLU activation
        out = self.fc2(out)  # Pass the output to the second fully connected layer
        return out


# Training loop
def train_model(model, criterion, optimizer, train_loader, val_loader, num_epochs=10):
    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0
        for ciphertext, labels in train_loader:
            optimizer.zero_grad()
            ciphertext = ciphertext.unsqueeze(2)  # Add extra dimension for RNN input
            outputs = model(ciphertext.float())
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * ciphertext.size(0)
        train_loss /= len(train_loader.dataset)

        # Validation
        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        with torch.no_grad():
            for ciphertext, labels in val_loader:
                ciphertext = ciphertext.unsqueeze(2)  # Add extra dimension for RNN input
                outputs = model(ciphertext.float())
                loss = criterion(outputs, labels)
                val_loss += loss.item() * ciphertext.size(0)
                _, predicted = torch.max(outputs, 1)
                correct += (predicted == labels).sum().item()
                total += labels.size(0)
        val_loss /= len(val_loader.dataset)
        accuracy = correct / total
        if epoch%10==0:
            print(f'Epoch [{epoch+1}/{num_epochs}], '
                f'Train Loss: {train_loss:.4f}, '
                f'Val Loss: {val_loss:.4f}, '
                f'Val Acc: {accuracy:.4f}')