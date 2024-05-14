from Dataloader import DataReader
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from ModelWang import cnnnet1
from attentionmod import blockblock
from torch.utils.data import DataLoader
import numpy as np
import matplotlib.pyplot as plt 
import os

seed = 26
torch.manual_seed(seed)
arr = os.listdir("C:\\Users\\Gebruiker\\Desktop\\Bap\\Code")

#-----HYPERPARAMETERS/training-----#
test_size = 32
batch_size = 64
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
learning_rate = 1e-4
lr_warmup = 1e-3
lr_fin = 1e-8
n_warmup = 30
max_iters = n_warmup + 1000
eval_interval = 10
#-----HYPERPARAMETERS/training-----#



#-----DataLoader-----#
arr = os.listdir("C:\\Users\\Gebruiker\\Desktop\\Bap\\Data")

#-----DataLoader-----#
logits = torch.load("logitsU2.pt")
targets = torch.load("targetsU2.pt")
t,f,h,l = logits.shape
rand = torch.randperm(t)
indtr = rand[:int(0.9*t)]
indte = rand[int(0.9*t):]
logits_train = logits[indtr]
targets_train = targets[indtr]
t1,f1,h1,l1 = logits_train.shape
logits_test = logits[indte]
targets_test = targets[indte]
torch.save(logits_test,"logits_test.pt")
torch.save(targets_test,"targets_test.pt")
dataset = torch.utils.data.TensorDataset(logits_train,targets_train)
train_size = int(t1*0.90)
train, test = torch.utils.data.random_split(dataset,[train_size,t1-train_size])
train = DataLoader(train,batch_size = batch_size,shuffle = True)
test = DataLoader(test,batch_size = test_size,shuffle = True)


#-----Warmup-----#
def warmup(current_step):
        if current_step < n_warmup:
            return lr_warmup
        elif current_step < 1000:
            return 1
        else:
          return lr_fin
#-----Warmup-----#


#-----Model-----#
arr = os.listdir("C:\\Users\\Gebruiker\\Desktop\\Bap\\Code")
model = cnnnet1().to(device)
#model.load_state_dict(torch.load("cnnnet1.pt"))
model.train()
#-----Model-----#

#-----optim/loss-----#
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
loss = torch.nn.CrossEntropyLoss()
scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer,lr_lambda = warmup)
  #-----optim/loss-----#

#a = model(inputlist.to(device))
#print(a[0])
#print(classout.shape)
#lossvalue = F.cross_entropy(a, classout.to(device))
#print(lossvalue)

llist = []
tlist = []
avloss = []
#-----training loop-----#
for itere in range(max_iters):
    tf_list,tt_list = next(iter(test))
    f_list,t_list = next(iter(train))
    if itere % eval_interval == 0 or itere == max_iters - 1:
        model.eval()
        out = model(tf_list.to(device))
        values,ind = torch.max(out,dim = 1)
        g = tt_list.shape
        #print(g)
        a = np.sum((torch.eq(ind.to("cpu"),tt_list.to("cpu")).numpy()))
        accuracy = (a/g)*100
        tlist.append(accuracy)
        avgloss = (np.sum(avloss)/(eval_interval-1))
        progress = (itere/max_iters) * 100
        print("accuracy : {}, validation loss : {}, progress : {}".format(accuracy, avgloss, progress))
        avloss = []
        if itere == 0:
            print(" ")
        else:
            llist.append(avgloss)
    else:
        model.train()
        batch_list = f_list
        targets_list = t_list
        test_list = tf_list
        ttarget_list = tt_list
        inputs = model(batch_list.to(device))
        val_input = model(test_list.to(device))
        lossvalue = loss(inputs, targets_list.to(device))
        vallvalue = loss(val_input, ttarget_list.to(device))
        #print(lossvalue,vallvalue)
        avloss.append(vallvalue.data.cpu().numpy())
        #print(scheduler.get_last_lr())
        optimizer.zero_grad(set_to_none=True)
        lossvalue.backward()
        optimizer.step()
        scheduler.step()
#-----training loop-----#    
        
torch.save(model.state_dict(),'cnnnet2048.pt')

plt.figure(figsize=(10,5))
plt.title("Training Loss")
plt.plot(llist,label="val")
#plt.plot(tlist,label="val")
plt.xlabel("iterations")
plt.ylabel("Loss")
plt.legend()
plt.show()
