import torch
import torch.nn as nn
import torch.nn.functional as F
from ModelWang import cnnnet1
from Dataloader import DataReader
import numpy as np
import matplotlib.pyplot as plt 
import os

seed = 26
torch.manual_seed(seed)

#-----HYPERPARAMETERS/training-----#
test_size = 32
batch_size = 100
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
learning_rate = 1e-4
lr_warmup = 1e-3
n_warmup = 30
max_iters = 50
eval_interval = 100
#-----HYPERPARAMETERS/training-----#



#-----DataLoader-----#
arr = os.listdir("C:\\Users\\vd00r\\OneDrive\\Desktop\\Bap\\code")

#-----datatest-----#
'''file1 = DataReader(dataset = "C:\\Users\\Gebruiker\\Desktop\\Bap\\A09T.npz")

data = file1.load_data()
logits = torch.tensor(np.asarray(data[0]),dtype = torch.float)
logits = logits[:,None,:,:]
array1 = np.asarray(data[1])
targets = torch.tensor(array1).type(torch.LongTensor)'''
#-----datatest-----#

#-----DataLoader-----#

logits = torch.load("logits2.65s.pt")
targets = torch.load("targets2.65s.pt")
t,f,h,l = logits.shape
rand = torch.randperm(t)
indtr = rand[:int(0.9*t)]
indte = rand[int(0.9*t):]
logits_train = logits[indtr]
targets_train = targets[indtr]
t1,f1,h1,l1 = logits_train.shape
logits_test = logits[indte]
targets_test = targets[indte]
t2,f2,h2,l1 = logits_test.shape
print(logits.shape)
print(logits_train.shape)
print(logits_test.shape)
#-----Model-----#
arr = os.listdir("C:\\Users\\vd00r\\OneDrive\\Desktop\\Bap\\code")
model = cnnnet1().to(device)
#model.load_state_dict(torch.load("cnnnet2.pt"))
model.train()
#-----Model-----#

#-----Warmup-----#
def warmup(current_step):
        if current_step < n_warmup:
            return lr_warmup
        else:
            return 1
        

#-----optim/loss-----#
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
loss = torch.nn.CrossEntropyLoss()
scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer,lr_lambda = warmup)
  #-----optim/loss-----#

#training loop
llist = []
tlist = []
for iter in range(max_iters):
        # evaluate the loss
        ind = torch.randperm(t1)[:batch_size]
        indt = torch.randperm(t2)[:test_size]
        batch_list = logits_train[ind]
        targets_list = targets_train[ind]
        test_list = logits_test[indt]
        ttarget_list = targets_test[indt]
        inputs = model(batch_list.to(device))
        val_input = model(test_list.to(device))
        #print(inputs[0])
        #print(targets_list[0])
        lossvalue = F.cross_entropy(inputs, targets_list.to(device))
        vallvalue = F.cross_entropy(val_input, ttarget_list.to(device))
        print(lossvalue,vallvalue)
        print(scheduler.get_last_lr())
        llist.append(lossvalue.data.cpu().numpy())
        tlist.append(vallvalue.data.cpu().numpy())
        #optimizer step
        optimizer.zero_grad() 
        lossvalue.backward()
        optimizer.step()
        #learning rate steps
        scheduler.step()
torch.save(model.state_dict(),'cnnnet2.pt')

plt.figure(figsize=(10,5))
plt.title("Training Loss")
plt.plot(llist,label="train")
plt.plot(tlist,label="val")
plt.xlabel("iterations")
plt.ylabel("Loss")
plt.legend()
plt.show()