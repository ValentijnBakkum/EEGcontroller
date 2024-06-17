import torch
import torch.nn as nn
import torch.nn.functional as F
from ModelWang import cnnnet1
from Dataloader import DataReader
from attentionmod import blockblock
import numpy as np
import matplotlib.pyplot as plt 
import os
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = cnnnet1().to(device)
model.load_state_dict(torch.load("cnnnet2048.pt"))
model.eval()

#file1 = DataReader(dataset = "C:\\Users\\Gebruiker\\Desktop\\Bap\\A09T.npz")

#data = file1.load_data()
#logits_batch = torch.tensor(np.asarray(data[0]),dtype = torch.float)
#l#ogits_batch = logits_batch[:,None,:,:]
#array1 = np.asarray(data[1])
#targets_batch = torch.tensor(array1).type(torch.LongTensor)
#print(targets_batch.shape)
logits = torch.load("logits_test.pt")
targets = torch.load("targets_test.pt")

out = model(logits.to(device))
values,ind = torch.max(out,dim = 1)
g = targets.shape
print(ind)
print(targets)
a = np.sum((torch.eq(ind.to("cpu"),targets.to("cpu")).numpy()))
print(a)
print((a/g)*100)