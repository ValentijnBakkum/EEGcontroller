import torch
import numpy
logits = torch.load("C:\\Users\\Gebruiker\\Desktop\\Bap\\Code\\code\\logits.pt")
targets = torch.load("C:\\Users\\Gebruiker\\Desktop\\Bap\\Code\\code\\labels.pt")
print(logits.shape)
logits1 = logits.numpy()
targets1 = targets.numpy()
index = numpy.where(targets1 ==1)
#print(index)
index2 = numpy.where(targets1 ==4)
#print(index2)
index = numpy.concatenate((index[0],index2[0]),axis = 0)
print(index.shape)
logits = logits[index]
targets = targets[index]
targets1 = targets.numpy()
print(targets1)
index2 = numpy.where(targets1 ==4)
index2 = index2[0].tolist()
print(index2)
numpy.put(targets1,index2,[2])
print(targets1)
torch.save(logits,"logits.pt")
torch.save(targets1,"targets.pt")

