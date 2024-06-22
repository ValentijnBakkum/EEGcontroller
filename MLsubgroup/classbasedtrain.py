import torch
import numpy as np
import pandas as pd
from scipy import signal
import os 

from torch.utils.data import DataLoader
from escargot3 import escargot
from csv_to_tensor import cleaner

class trainer():

    def __init__(self,batch_size,learning_rate,max_iters,eval_interval):
        self.batch_size = batch_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.learning_rate = learning_rate
        self.max_iters = max_iters
        self.eval_interval = eval_interval

    def train(self,logits_train,targets_train):
        logits_train = torch.load(logits_train)
        targets_train = torch.load(targets_train)
        targets_train = targets_train - 1
        #logits_train = logits_train[:,None,:,:]
        print(logits_train.shape)
        print(targets_train.shape)
        dataset = torch.utils.data.TensorDataset(logits_train,targets_train)
        t = logits_train.shape(0)
        train_size = int(t*0.9)
        train,test = torch.utils.data.random_split(dataset,[train_size,t-train_size])
        train = DataLoader(train,batch_size = self.batch_size,shuffle = True)
        test =  DataLoader(test,batch_size = test_size,shuffle = True)

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
            tf_list,tt_list = next(iter(test))
            tt_list = tt_list.type(torch.LongTensor)
            if itere % self.eval_interval == 0 or itere == self.max_iters - 1:
                with torch.no_grad():
                    model.eval()
                    out = model(tf_list.to(self.device,dtype=torch.float))#tf_list.to(device),tff_list.to(device)
                    #print(torch.max(out,dim=1))
                    values,ind = torch.max(out,dim = 1)
                    g = t_list.shape
                    #print(g)
                    a = np.sum((torch.eq(ind.to("cpu"),tt_list.to("cpu")).numpy()))
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
                    val_input = model(tf_list.to(self.device,dtype=torch.float))#test_list.to(device),tff_list.to(device)
                lossvalue = loss(inputs, t_list.to(self.device))
                #print(lossvalue)
                vallvalue = loss(val_input.to(self.device),tt_list.to(self.device))
                avloss.append(vallvalue.data.cpu().numpy())
                optimizer.zero_grad(set_to_none=True)
                lossvalue.backward()
                optimizer.step()
                scheduler.step()
        #-----training loop-----#    
                
        torch.save(model.state_dict(),'blockblock.pt')
    
    def dataloader(self, input_directory, output_directory):

        combologits = torch.empty(0, 1, 529, 8)
        combolabels = torch.empty(0)

        for filename in os.listdir(input_directory):

            if filename.endswith(".csv"):

                filepath = os.path.join(input_directory, filename)
                data_csv = pd.read_csv(filepath, delimiter=',')
                data_csv = data_csv.iloc[:72000,:8]

                data_csv_detr = cleaner.detrend(data_csv)
                data_csv_filt = cleaner.filter(data_csv_detr)
                data_csv_np = np.array(data_csv_filt)
                (data_csv_res, lables) = cleaner.cursed_reshape(data_csv_np)

                print(data_csv_res.shape)
                print(lables.shape)

                data_torch = torch.from_numpy(data_csv_res) 
                lables_torch = torch.from_numpy(lables)

                logits = data_torch.squeeze(1)
                data_torch = cleaner.CAR_filter(logits)
                logits = data_torch.unsqueeze(1) 

                combologits = torch.cat((combologits,logits), dim=0)
                combolabels = torch.cat((combolabels,lables_torch), dim=0)
        
        user_logits_path = os.path.join(output_directory, 'logits.pt')
        user_labels_path = os.path.join(output_directory, 'labels.pt')
    
        torch.save(combologits, user_logits_path)
        torch.save(combolabels, user_labels_path)


#input_directory = "Data/3"
#output_directory = "Data"
#
#a = trainer(64, 1e-2, 1000, 10)
#a.dataloader(input_directory, output_directory)
#a.train('Data\logits.pt', 'Data\labels.pt')
#a = train(64,1e-1,1000,10,"C:\\Users\\Gebruiker\\Downloads\\EEGdata-2024-150--15-01-30.csv")
