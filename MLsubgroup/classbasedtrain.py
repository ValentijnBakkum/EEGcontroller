import torch
from torch.utils.data import DataLoader
from escargot3 import escargot
import numpy as np
import pandas as pd
import os 

class train():

    def __init__(self,batch_size,learning_rate,max_iters,eval_interval,load_cvs):
        self.batch_size = batch_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.learning_rate = learning_rate
        self.max_iters = max_iters
        self.eval_interval = eval_interval
        self.load = load_cvs

    def train(self,logits_train,targets_train):
        logits_train = torch.load(logits_train)
        targets_train = torch.load(targets_train)
        logits_train = logits_train[:,None,:,:]
        print(logits_train.shape)
        print(targets_train.shape)
        dataset = torch.utils.data.TensorDataset(logits_train,targets_train)
        train = DataLoader(dataset,batch_size = self.batch_size,shuffle = True)
        model = escargot().to(self.device)
        model.train()
        optimizer = torch.optim.Adam(model.parameters(), lr=self.learning_rate, weight_decay=1e-3)
        loss = torch.nn.CrossEntropyLoss()
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.7)
        llist = []
        tlist = []
        avloss = []
        acc_list = []
        #-----training loop-----#
        for itere in range(self.max_iters):
            f_list,t_list = next(iter(train))
            t_list = t_list.type(torch.LongTensor)
            if itere % self.eval_interval == 0 or itere == self.max_iters - 1:
                with torch.no_grad():
                    model.eval()
                    out = model(f_list.to(self.device,dtype=torch.float))#tf_list.to(device),tff_list.to(device)
                    #print(torch.max(out,dim=1))
                    values,ind = torch.max(out,dim = 1)
                    g = t_list.shape
                    #print(g)
                    a = np.sum((torch.eq(ind.to("cpu"),t_list.to("cpu")).numpy()))
                    #print(a)
                    accuracy = (a/g)*100
                    tlist.append(accuracy)
                    avgloss = (np.sum(avloss)/(len(avloss)))
                    progress = (itere/self.max_iters) * 100
                    print("accuracy : {}, validation loss : {}, progress : {}%, lr : {}".format(accuracy, avgloss, int(progress), scheduler.get_last_lr()))
                    avloss = []
                    if itere == 0:
                        print(" ")
                    else:
                        llist.append(avgloss)
                        acc_list.append(accuracy)
            else:
                model.train()
                inputs = model(f_list.to(self.device,dtype=torch.float))#,ff_list.to(device)batch_list.to(device)
                #print(inputs[0])
                with torch.no_grad():
                    val_input = model(f_list.to(self.device,dtype=torch.float))#test_list.to(device),tff_list.to(device)
                lossvalue = loss(inputs, t_list.to(self.device))
                #print(lossvalue)
                vallvalue = loss(val_input.to(self.device),t_list.to(self.device))
                avloss.append(vallvalue.data.cpu().numpy())
                optimizer.zero_grad(set_to_none=True)
                lossvalue.backward()
                optimizer.step()
                scheduler.step()
        #-----training loop-----#    
                
        torch.save(model.state_dict(),'blockblock.pt')

def dataloader(directory):

    output_list = []
    label_list = []

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)

            label_1 = df.loc[df['Label'] == 0]
            label_2 = df.loc[df['Label'] == 1]
            label_3 = df.loc[df['Label'] == 2]
            label_4 = df.loc[df['Label'] == 3]
            label_5 = df.loc[df['Label'] == 4]

            label_1mod = label_2.drop(columns=["Counter", "Validation", "Label"]).to_numpy()
            label_2mod = label_3.drop(columns=["Counter", "Validation", "Label"]).to_numpy()
            label_3mod = label_4.drop(columns=["Counter", "Validation", "Label"]).to_numpy()
            label_4mod = label_5.drop(columns=["Counter", "Validation", "Label"]).to_numpy()

        
            list_class = [label_1mod,label_2mod,label_3mod,label_4mod]
            g = 0

            for i in list_class:

                for _ in range(6):

                    index = _ * 1500
                    for waa in range(30):

                        a = i[index+25*waa:index + 529+25*waa]
                        a = torch.tensor(a)
                    
                        if g == 0:
                            output_list.append(a)
                            label_list.append(0)
                        elif g == 1:
                            output_list.append(a)
                            label_list.append(1)
                            pass
                        elif g == 2:
                            output_list.append(a)
                            label_list.append(2)
                            pass
                        elif g == 3:
                            output_list.append(a)
                            label_list.append(1)

                g = g + 1
        
    output_label1 = np.stack(output_list)
    output_label1 = torch.tensor(output_label1)
    targets = torch.tensor(label_list)

    print(output_label1.shape)    

    torch.save(output_label1,"own.pt")
    torch.save(targets,"owntargets.pt")

    return True

dataloader("/Users/pragun/Technical/BAP/2")

#a = train(64,1e-1,1000,10,"C:\\Users\\Gebruiker\\Downloads\\EEGdata-2024-150--15-01-30.csv")
#a.dataloader()
#a.train("own.pt","owntargets.pt")