import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from Main import cnnnet1
from torch.utils.data import DataLoader
import numpy as np
import matplotlib.pyplot as plt 
import os

seed = 26
torch.manual_seed(seed)

#-----HYPERPARAMETERS/training-----#
block_size = 512
batch_size = 256
test_size = 12
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
learning_rate = 1e-5
max_iters = 500
eval_interval = 100
#-----HYPERPARAMETERS/training-----#



#-----DataLoader-----#
arr = os.listdir("C:\\Users\\vd00r\\OneDrive\\Desktop\\Bap\\Data")

'''for _ in arr:
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
torch.save(targets,"targets.pt")'''

#-----DataLoader-----#
logits = torch.load("logits.pt")
targets = torch.load("targets.pt")
dataset = torch.utils.data.TensorDataset(logits,targets)
t,f,h,l = logits.shape
train_size = int(t*0.9)
train, test = torch.utils.data.random_split(dataset,[train_size,t-train_size])
train = DataLoader(train,batch_size = batch_size,shuffle = True)
test = DataLoader(test,batch_size = test_size,shuffle = True)

f_list,t_list = next(iter(train))
tf_list,tt_list = next(iter(test))
#-----Model-----#
arr = os.listdir("C:\\Users\\vd00r\\OneDrive\\Desktop\\Bap\\code")
model = cnnnet1().to(device)
#model.load_state_dict(torch.load("cnnnet1.pt"))
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
tlist = []
for iter in range(max_iters):
        # evaluate the loss
        #print(batch_list.shape)
        #print(targets_list.shape)
        inputs = model(f_list.to(device))
        inputst = model(tf_list.to(device))
        print(inputs[0])
        print(t_list[0])
        lossvalue = F.cross_entropy(inputs, t_list.to(device))
        losstest = F.cross_entropy(inputst, tt_list.to(device))
        print(lossvalue,losstest)
        llist.append(lossvalue.data.cpu().numpy())
        tlist.append(losstest.data.cpu().numpy())
        optimizer.zero_grad(set_to_none=True)
        lossvalue.backward()
        optimizer.step()
        
torch.save(model.state_dict(),'cnnnet2048.pt')

plt.figure(figsize=(10,5))
plt.title("Training Loss")
plt.plot(llist,label="train")
plt.plot(tlist,label="val")
plt.xlabel("iterations")
plt.ylabel("Loss")
plt.legend()
plt.show()