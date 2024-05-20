import torch
import torch.nn as nn
import torch.nn.functional as F
from ModelWang import cnnnet1
from attentionmod import blockblock
from Dataloader import DataReader
import numpy as np
import matplotlib.pyplot as plt 
from loss import TripletLoss
from utils import gen_batch
import os

seed = 25
torch.manual_seed(seed)
arr = os.listdir("C:\\Users\\Gebruiker\\Desktop\\Bap\\Code")

#-----HYPERPARAMETERS/training-----#
test_size = 20
batch_size = 40
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
learning_rate = 1e-4
lr_warmup = 1e-3
lr_fin = 1e-8
n_warmup = 30
max_iters = n_warmup + 500
eval_interval = 10
margin = 0.7
#-----HYPERPARAMETERS/training-----#

logits = torch.load("logits0.5-30-1s.pt")
targets = torch.load("targets0.5-30-1s.pt")
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
print(targets_train.shape)



#-----Model-----#
model = cnnnet1().to(device)
#model.load_state_dict(torch.load("cnnnet2.pt"))
model.train()
#-----Model-----#


#-----Warmup-----#
def warmup(current_step):
        if current_step < 2:
            return lr_warmup
        elif current_step < 9000:
            return 1
        else:
          return lr_fin
#-----Warmup-----#


#-----optim/loss/scheduler-----#
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate,weight_decay=0)
loss = TripletLoss(alpha = margin)
scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer,lr_lambda = warmup)
#-----optim/loss/scheduler-----#


#-----training loop-----#
llist = []
tlist = []
for iter in range(max_iters):
        # evaluate the loss
        if iter % eval_interval == 0 or iter == max_iters - 1:
            model.eval()
            posval_tens , anchval_tens, negval_tens = gen_batch(logits_test,targets_test,test_size)
            inputs_anch = model(anchval_tens.to(device))
            inputs_pos = model(posval_tens.to(device))
            inputs_neg = model(negval_tens.to(device))
            val = loss(inputs_anch,inputs_pos,inputs_neg)
            val = torch.mean(val)
            tlist.append(val)
            progress = (iter/max_iters) * 100
            print("validation loss : {}, progress : {}%, lr : {}".format(val, int(progress), scheduler.get_last_lr()))
        else:
            model.train()
            pos_tens , anch_tens, neg_tens = gen_batch(logits_train,targets_train,batch_size)
            inputs_anch = model(anch_tens.to(device))
            inputs_pos = model(pos_tens.to(device))
            inputs_neg = model(neg_tens.to(device))
            lossvalue = loss(inputs_anch,inputs_pos,inputs_neg)
            lossvalue = torch.mean(lossvalue)
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
