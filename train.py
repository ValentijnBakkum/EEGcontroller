import torch
import torch.nn as nn
import torch.nn.functional as F
from Main import cnnnet
from Dataloader import DataReader
import numpy as np
import matplotlib.pyplot as plt 
import os

seed = 26
torch.manual_seed(seed)

#-----HYPERPARAMETERS/training-----#
block_size = 512
batch_size = 128
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
learning_rate = 1e-5
max_iters = 6000
eval_interval = 100
#-----HYPERPARAMETERS/training-----#



#-----DataLoader-----#
arr = os.listdir("C:\\Users\\vd00r\\OneDrive\\Desktop\\Bap\\Data")

for _ in arr:
      arg = "C:\\Users\\vd00r\\OneDrive\\Desktop\\Bap\\Data\\" + _
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
torch.save(logits,"logits.pt")
torch.save(targets,"targets.pt")

#-----DataLoader-----#

print(logits.shape)
print(targets.shape)
#-----Model-----#
model = cnnnet().to(device)
#model.load_state_dict(torch.load("C:\\Users\\Gebruiker\\Desktop\\Bap\\Code\\cnnnet.pt"))
model.train()
#-----Model-----#

#-----optim/loss-----#
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
loss = torch.nn.CrossEntropyLoss()
  #-----optim/loss-----#

#a = model(inputlist.to(device))
#print(a[0])
#print(classout.shape)
#lossvalue = F.cross_entropy(a, classout.to(device))
#print(lossvalue)

llist = []
for iter in range(max_iters):
        # evaluate the loss
        t,f,h,l = logits.shape
        ind = torch.randperm(t)[:batch_size]
        batch_list = logits[ind]
        targets_list = targets[ind]
        #print(batch_list.shape)
        #print(targets_list.shape)
        inputs = model(batch_list.to(device))
        print(inputs[0])
        lossvalue = F.cross_entropy(inputs, targets_list.to(device))
        print(lossvalue)
        llist.append(lossvalue.data.cpu().numpy())
        optimizer.zero_grad(set_to_none=True)
        lossvalue.backward()
        optimizer.step()
        
torch.save(model.state_dict(),'cnnnet.pt')

plt.figure(figsize=(10,5))
plt.title("Training Loss")
plt.plot(llist,label="train")
plt.xlabel("iterations")
plt.ylabel("Loss")
plt.legend()
plt.show()