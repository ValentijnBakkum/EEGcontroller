from Dataloader import DataReader
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
#from Main import cnnnet1
from torch.utils.data import DataLoader
import numpy as np
import matplotlib.pyplot as plt 
import os

arr = os.listdir("C:\\Users\\Gebruiker\\Desktop\\Bap\\Data")

for _ in arr[:1]:
      arg = "C:\\Users\\Gebruiker\\Desktop\\Bap\\Data\\" + _
      file1 = DataReader(dataset = arg)
      data = file1.load_data()
      #logits
      logits_batch = torch.tensor(np.asarray(data[0]),dtype = torch.float)
      #print(inputlist.shape)
      #result
      array1 = np.asarray(data[1])
      targets_batch = torch.tensor(array1).type(torch.LongTensor)
      

      if _ == "A01T.npz":
          logits = logits_batch
          targets = targets_batch
      else:
          logits = torch.cat((logits,logits_batch),dim = 0)
          targets = torch.cat((targets,targets_batch),dim = 0)
logits = logits[:,None,:,:]
torch.save(logits,"logits2.65sv2.pt")
torch.save(targets,"targets2.65sv2.pt")