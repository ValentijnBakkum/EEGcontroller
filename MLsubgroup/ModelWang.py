import torch
import torch.nn as nn
import torch.nn.functional as F
from torchinfo import summary
from attentionmod import blockblock,multihead
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#convnet decleration/architecture
arch_1 = [
    (128,1),
    (64,1),
    (32,1)
]

#convblock class
class convblock(nn.Module):
    def __init__(self,in_channels,filter_number):
        super(convblock,self).__init__()
        self.conv3 = nn.Conv3d(in_channels = in_channels, out_channels = filter_number,kernel_size=3, stride = 1, padding = 1, bias = False)
        self.conv5 = nn.Conv3d(in_channels = in_channels, out_channels = filter_number,kernel_size=5, stride = 1, padding = 2, bias = False)
        self.conv7 = nn.Conv3d(in_channels = in_channels, out_channels = filter_number,kernel_size=7, stride = 1, padding = 3, bias = False)
        self.batchnorm = nn.BatchNorm3d(filter_number*3)
        self.max = nn.MaxPool3d(kernel_size=(2,2,2))
        self.act = nn.LeakyReLU()
    def forward(self,x):
        x3 = self.act(self.conv3(x))
        x5 = self.act(self.conv5(x))
        x7 = self.act(self.conv7(x))
        x = torch.cat((x3,x5,x7),dim = 1)
        return self.max(self.act(self.batchnorm(x)))

#Lstm layer
class lstmmodule(nn.Module):
    def __init__(self, input_len = 16, hidden_size=128, num_layers=1):
        super(lstmmodule, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_len,hidden_size,num_layers,batch_first=True)
        self.fc = nn.Sequential(nn.Linear(256*hidden_size,256),
                                nn.Dropout(p=0.3),
                                nn.LeakyReLU()
                                )
        self.flatten = nn.Flatten()
    def forward(self,x):
        hidden_states = torch.zeros(self.num_layers, x.size(0),self.hidden_size).to(device)
        cell_states = torch.zeros(self.num_layers, x.size(0),self.hidden_size).to(device)
        out, (hn,cn) = self.lstm(x,(hidden_states.detach(),cell_states.detach()))
        return self.fc(self.flatten(out))

#Dense layer    
class Dense(nn.Module):
    def __init__(self):
        super(Dense, self).__init__()
        self.dense = nn.Sequential(nn.Flatten(),
                                   nn.Linear(2048,256),
                                   nn.Dropout(p=0.3),
                                   nn.LeakyReLU(),    
        )
    def forward(self,x):
        return(self.dense(x))

#model
class cnnnet1(nn.Module):
    def __init__(self,in_channels = 1):
        super(cnnnet1,self).__init__()
        self.arch = arch_1
        self.in_channels = in_channels
        self.Cnn = self.Create_conv_layers(self.arch)
        self.nn = self.create_nn()
        self.flatten = nn.Flatten()
        self.lstm = lstmmodule()
        self.dense = Dense()
        self.decoder = blockblock(6,16,4,256,16).to(device)
    def forward(self,x):
        N,C,H,W = x.shape # get shape of input
        xr = torch.reshape(x,(N,1,16,16,16)) # reshape input for convolutional neural network
        #convolutional part
        intermediate = self.Cnn(xr)
        intermediate = self.flatten(intermediate)
        #intermediate = self.dense(intermediate) # reshape for LSTM part
        # LSTM part
        #xlstmi = intermediate[:,:,None]
        xlstmi = torch.squeeze(x)
        #print(xlstmi.shape)
        xlstm = self.lstm(xlstmi)
        #print(xlstm.shape)
        #self attention part
        yw = torch.squeeze(x)
        yw = self.flatten(self.decoder(yw))
        intermediate = torch.cat((yw,intermediate,xlstm),dim=1)
        return(self.nn(intermediate))
    
    def Create_conv_layers(self,arch): #creates the 3d convolution layers used before the lstm
        in_channels = self.in_channels
        list = []
        for x in arch:
            if type(x) == tuple:
                list += [convblock(in_channels,x[0])]
                in_channels = x[0]*3
            elif type(x) == list:
                print("placeholder")
        return nn.Sequential(*list) # * unpacks list into nn.Sequential module
    def create_nn(self): #creates the nn used in the model
        return nn.Sequential(nn.Flatten(),
                             nn.Linear(1280,4,bias=True),
                             nn.Dropout(p=0.3)
                             #nn.Softmax()
        )
    

#summary of the model
#model = cnnnet1().to(device)
#summary(model,input_size=(256,1,256,16))
#a = torch.rand(1,1,576,16).to(device)
#print(model(a))
'''
                             nn.Linear(512,512,bias=True),
                             nn.Dropout(p=0.3),
                             nn.LeakyReLU(),
                             '''