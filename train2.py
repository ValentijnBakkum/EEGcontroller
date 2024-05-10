import torch
import torch.nn as nn
import torch.nn.functional as F
from ModelWang import cnnnet1
from attentionmod import blockblock
from Dataloader import DataReader
import numpy as np
import matplotlib.pyplot as plt 
import os

seed = 26
torch.manual_seed(seed)
arr = os.listdir("C:\\Users\\Gebruiker\\Desktop\\Bap\\Code")

#-----HYPERPARAMETERS/training-----#
test_size = 40
batch_size = 128
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
learning_rate = 1e-4
lr_warmup = 1e-3
lr_fin = 1e-8
n_warmup = 30
max_iters = n_warmup + 500
eval_interval = 3
#-----HYPERPARAMETERS/training-----#

logits = torch.load("logitsU1.pt")
targets = torch.load("targetsU1.pt")
t,f,h,l = logits.shape

rand = torch.randperm(t)
indtr = rand[:int(0.8*t)]
indte = rand[int(0.8*t):]
logits_train = logits[indtr]
targets_train = targets[indtr]
t1,f1,h1,l1 = logits_train.shape
logits_test = logits[indte]
targets_test = targets[indte]
torch.save(logits_test,"logits_test.pt")
torch.save(targets_test,"targets_test.pt")
t2,f2,h2,l1 = logits_test.shape
print(logits.shape)
print(logits_train.shape)
print(logits_test.shape)



#-----Model-----#
model = cnnnet1().to(device)
#model.load_state_dict(torch.load("cnnnet2.pt"))
model.train()
#-----Model-----#


#-----Warmup-----#
def warmup(current_step):
        if current_step < 1:
            return lr_warmup
        elif current_step < 900:
            return 1
        else:
          return lr_fin
#-----Warmup-----#


#-----optim/loss/scheduler-----#
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
loss = torch.nn.CrossEntropyLoss()
scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer,lr_lambda = warmup)
#-----optim/loss/scheduler-----#


#-----training loop-----#
llist = []
tlist = []
for iter in range(max_iters):
        # evaluate the loss
        if iter % eval_interval == 0 or iter == max_iters - 1:
            #print('a')
            model.eval()
            out = model(logits_test.to(device))
            values,ind = torch.max(out,dim = 1)
            g = targets_test.shape
            a = np.sum((torch.eq(ind.to("cpu"),targets_test.to("cpu")).numpy()))
            accuracy = (a/g)*100
            print(accuracy)
            tlist.append(accuracy)
        else:
            #print('b')
            model.train()
            ind = torch.randperm(t1)[:batch_size]
            indt = torch.randperm(t2)[:test_size]
            batch_list = logits_train[ind]
            targets_list = targets_train[ind]
            #print(batch_list.shape,targets_list.shape)
            #test_list = logits_test[indt]
            #ttarget_list = targets_test[indt]
            inputs = model(batch_list.to(device))
            #val_input = model(test_list.to(device))
            #print(inputs[0])
            #print(targets_list[0])
            lossvalue = F.cross_entropy(inputs, targets_list.to(device), reduction="mean")
            #vallvalue = F.cross_entropy(val_input, ttarget_list.to(device), reduction="mean")
            print(lossvalue)
            llist.append(lossvalue.data.cpu().numpy())
            #print(scheduler.get_last_lr())
            optimizer.zero_grad(set_to_none=True)
            lossvalue.backward()
            optimizer.step()
            scheduler.step()
#-----training loop-----#

torch.save(model.state_dict(),'cnnnet2.pt')

plt.figure(figsize=(10,5))
plt.title("Training Loss")
#plt.plot(llist,label="train")
plt.plot(tlist,label="val")
plt.xlabel("iterations")
plt.ylabel("Loss")
plt.legend()
plt.show()
