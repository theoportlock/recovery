import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torchkan import KAN
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score

# Load microbiome data (X: features, y: labels)
def load_data():
    # Placeholder: Replace with actual microbiome dataset
    X = np.random.rand(500, 50)  # 500 samples, 50 microbial features
    y = np.random.randint(0, 2, 500)  # Binary labels (CRC vs. control)
    return X, y

# Data preparation
X, y = load_data()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert to PyTorch tensors
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# Define KAN Model
class KANClassifier(nn.Module):
    def __init__(self, input_dim):
        super(KANClassifier, self).__init__()
        self.kan = KAN(input_dim, [64, 32], 1)
    
    def forward(self, x):
        return torch.sigmoid(self.kan(x))  # Sigmoid for binary classification

# Model Initialization
model = KANClassifier(input_dim=X_train.shape[1])
criterion = nn.BCELoss()  # Binary cross-entropy loss
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training Loop
def train_model(model, train_loader, criterion, optimizer, epochs=20):
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(train_loader):.4f}")

# Train the model
train_model(model, train_loader, criterion, optimizer)

# Evaluation
def evaluate_model(model, test_loader):
    model.eval()
    y_pred, y_true = [], []
    with torch.no_grad():
        for X_batch, y_batch in test_loader:
            outputs = model(X_batch).cpu().numpy()
            y_pred.extend(outputs)
            y_true.extend(y_batch.cpu().numpy())
    
    y_pred = np.array(y_pred).flatten()
    y_pred_labels = (y_pred > 0.5).astype(int)
    auc = roc_auc_score(y_true, y_pred)
    acc = accuracy_score(y_true, y_pred_labels)
    print(f"Test AUC: {auc:.4f}, Accuracy: {acc:.4f}")

# Run evaluation
evaluate_model(model, test_loader)
