import torch
import torch.nn as nn
import torch.nn.functional as F
from torchinfo import summary
from attentionmod import blockblock,multihead
from bspline import spline_activation
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#device = "cpu"

#convnet decleration/architecture
arch_2 = [
    (16,1),
    (16*3,1),
    (16*3*3,1),
    (16*3*3*3,1)
]

arch_1 = [
    (32,1),
    (64,1),
    (128,1)
]


#rewrite
class L2NormalizationLayer(nn.Module):
    def __init__(self, dim=1, eps=1e-12):
        super(L2NormalizationLayer, self).__init__()
        self.dim = dim
        self.eps = eps
    def forward(self, x):
        return F.normalize(x, p=2, dim=self.dim, eps=self.eps)

#convblock class


#convblock class
class convblock(nn.Module):
    def __init__(self,in_channels,filter_number):
        super(convblock,self).__init__()
        self.conv3 = nn.Conv3d(in_channels = in_channels, out_channels = filter_number,kernel_size=3, stride = 1, padding = 1, bias = False)
        self.conv5 = nn.Conv3d(in_channels = in_channels, out_channels = filter_number,kernel_size=5, stride = 1, padding = 2, bias = False)
        self.conv7 = nn.Conv3d(in_channels = in_channels, out_channels = filter_number,kernel_size=7, stride = 1, padding = 3, bias = False)
        self.conv33 = nn.Conv3d(in_channels = filter_number, out_channels = filter_number,kernel_size=3, stride = 1, padding = 1, bias = False)
        self.conv55 = nn.Conv3d(in_channels = filter_number, out_channels = filter_number,kernel_size=5, stride = 1, padding = 2, bias = False)
        self.conv77 = nn.Conv3d(in_channels = filter_number, out_channels = filter_number,kernel_size=7, stride = 1, padding = 3, bias = False)
        self.batchnorm = nn.BatchNorm3d(filter_number*3)
        self.max = nn.MaxPool3d(kernel_size=(2,2,2))
        self.act = nn.LeakyReLU()
        self.dropout3d = nn.Dropout3d(p=0.3)
    def forward(self,x):
        d,i,ei,e2,e3 = x.shape
        x3 = self.act(self.conv3(x))
        x33 = self.act(self.conv33(x3))
        x333 = self.act(self.conv33(x3))
        x5 = self.act(self.conv5(x))
        x55 = self.act(self.conv55(x5))
        x7 = self.act(self.conv7(x))
        xall = torch.cat((x333,x55,x7),dim = 1)
        x = torch.cat((x,x,x),dim=1)
        if i == 1:
            return self.max(self.batchnorm(xall))
        else:
            return self.max(self.batchnorm(xall+x))

#Lstm layer
class lstmmodule(nn.Module):
    def __init__(self, input_len = 16, hidden_size=256, num_layers=1):
        super(lstmmodule, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_len,hidden_size,num_layers,batch_first=True)
        self.fc = nn.Sequential(nn.Linear(529*hidden_size,256),
                                nn.Dropout(p=0.3),
                                nn.ReLU(),
                                #L2NormalizationLayer(),
                                #spline_activation(device = device,grid = 10, input_dim = 256)
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
                                   nn.ReLU(),
                                   spline_activation(device = device,grid = 20, input_dim = 512),
                                   nn.LeakyReLU(),    
        )
    def forward(self,x):
        return(self.dense(x))

#model
class escargot(nn.Module):
    def __init__(self,in_channels = 1):
        super(escargot,self).__init__()
        self.arch = arch_2
        self.in_channels = in_channels
        self.Cnn = self.Create_conv_layers(self.arch)
        self.nn = self.create_nn()
        self.flatten = nn.Flatten()
        self.lstm = lstmmodule()
        self.dense = Dense()
        self.norm = L2NormalizationLayer()
        #self.decoder = blockblock(2,1,4,1296,8).to(device)
    def forward(self,x):
        N,C,H,W = x.shape # get shape of input
        xr = torch.reshape(x,(N,1,23,23,16)) # reshape input for convolutional neural network
        #convolutional part
        intermediate = self.Cnn(xr)
        intermediate = self.flatten(intermediate)
        #self attention module
        #intermediate = intermediate[:,None,:,None]
        #intermediate = self.decoder(intermediate)
        #intermediate = self.flatten(intermediate)
        
        xlstmi = torch.squeeze(x)
        xlstm = self.lstm(xlstmi)
        intermediate = torch.cat((intermediate,xlstm),dim=1)
        return self.nn(intermediate)
    
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
                             nn.Linear(1552,512,bias=True),
                             nn.Dropout(p=0.3),
                             L2NormalizationLayer(),
                             spline_activation(device = device,grid = 10, input_dim = 512),
                             nn.Linear(512,8),
                             L2NormalizationLayer()
                             #nn.Softmax()
        )
    

#summary of the model
#model = escargot().to(device)
#summary(model,input_size=(40,1,529,16))
#a = torch.rand(1,1,576,16).to(device)
#print(model(a))