import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy

#logits = torch.load("logits0.5-30-1s.pt")
#targets = torch.load("targets0.5-30-1s.pt")

def gen_batch(data,classification,batch_size):
    t,f,h,l = data.shape
    anch_pos = torch.randperm(t)[:batch_size]
    anch_id = classification[anch_pos]
    anch_tens = data[anch_pos]
    pos_list = []
    neg_list = []
    for _ in anch_id:
        id_pos = (classification == _.item()).nonzero(as_tuple=True)[0]
        l = id_pos.shape
        sel = torch.randint(0,l[0],(1,))
        pos_list.append(id_pos[sel].item())
    for _ in anch_id:
        id_neg = (classification != _.item()).nonzero(as_tuple=True)[0]
        l = id_neg.shape
        #print(l)
        sel = torch.randint(0,l[0],(1,))
        neg_list.append(id_neg[sel].item())
    
    #print(pos_list)    
    #print(neg_list)    
    pos_tens = data[pos_list]
    neg_tens = data[neg_list]
    return pos_tens, anch_tens , neg_tens

#pos_tens , anch_tens, neg_tens = gen_batch(logits,targets,64)
#print(pos_tens.shape)