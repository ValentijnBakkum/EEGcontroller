from Dataloader import DataReader
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, TensorDataset
from ModelWang import cnnnet1
from attentionmod import blockblock
from torch.utils.data import DataLoader
import numpy as np
import matplotlib.pyplot as plt 
import os
from sklearn.model_selection import KFold

seed = 26
torch.manual_seed(seed)

test_size = 32
batch_size = 64
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
learning_rate = 1e-4
lr_warmup = 1e-3
lr_fin = 1e-8
n_warmup = 30
max_iters = n_warmup + 1000
eval_interval = 10

logits = torch.load("/Users/pragun/Technical/BAP/Processed/logitsU2.pt")
targets = torch.load("/Users/pragun/Technical/BAP/Processed/targetsU2.pt")
t, f, h, l = logits.shape

dataset = TensorDataset(logits, targets)

kf = KFold(n_splits=5, shuffle=True, random_state=seed)

def warmup(current_step):
    if current_step < n_warmup:
        return lr_warmup
    elif current_step < 1000:
        return 1
    else:
        return lr_fin
    
fold_accuracies = []
fold_losses = []

for fold, (train_idx, val_idx) in enumerate(kf.split(dataset)):
    print(f"Fold {fold+1}/{5}")
    
    train_subsampler = torch.utils.data.SubsetRandomSampler(train_idx)
    val_subsampler = torch.utils.data.SubsetRandomSampler(val_idx)

    trainloader = DataLoader(dataset, batch_size=batch_size, sampler=train_subsampler)
    valloader = DataLoader(dataset, batch_size=test_size, sampler=val_subsampler)

    model = cnnnet1().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    loss_fn = torch.nn.CrossEntropyLoss()
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=warmup)

    llist = []
    tlist = []
    avloss = []

    for itere in range(max_iters):
        model.train()
        for batch in trainloader:
            batch_list, targets_list = batch
            inputs = model(batch_list.to(device))
            lossvalue = loss_fn(inputs, targets_list.to(device))

            optimizer.zero_grad(set_to_none=True)
            lossvalue.backward()
            optimizer.step()
            scheduler.step()

        if itere % eval_interval == 0 or itere == max_iters - 1:
            model.eval()
            correct = 0
            total = 0
            val_loss = 0.0
            with torch.no_grad():
                for val_batch in valloader:
                    val_inputs, val_targets = val_batch
                    outputs = model(val_inputs.to(device))
                    val_loss += loss_fn(outputs, val_targets.to(device)).item()
                    _, predicted = torch.max(outputs.data, 1)
                    total += val_targets.size(0)
                    correct += (predicted == val_targets.to(device)).sum().item()

            accuracy = 100 * correct / total
            tlist.append(accuracy)
            avgloss = val_loss / len(valloader)
            llist.append(avgloss)

            print(f"Iteration {itere}: Accuracy: {accuracy:.2f}%, Loss: {avgloss:.4f}")

    fold_accuracies.append(tlist)
    fold_losses.append(llist)

# Plotting the results
plt.figure(figsize=(10,5))
for i in range(5):
    plt.plot(fold_losses[i], label=f'Fold {i+1} Loss')
plt.title("Validation Loss per Fold")
plt.xlabel("Evaluation Intervals")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.figure(figsize=(10,5))
for i in range(5):
    plt.plot(fold_accuracies[i], label=f'Fold {i+1} Accuracy')
plt.title("Validation Accuracy per Fold")
plt.xlabel("Evaluation Intervals")
plt.ylabel("Accuracy (%)")
plt.legend()
plt.show()

# Save the final model
torch.save(model.state_dict(), 'cnnnet2048.pt')