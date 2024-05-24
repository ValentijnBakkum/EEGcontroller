import torch
import torch.nn as nn
import torch.nn.functional as F
from torchinfo import summary
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#t = torch.rand(9,9,8)
#print(t)

#convnet decleration/architecture
arch_1 = [
    (3,32,1,1),
    (3,32,1,1),
    "m",
    (3,32,1,1),
    (3,32,1,1),
    "m",
    (3,16,1,2),
    (3,16,1,1),
    "m"
]


#convblock class
class convblock(nn.Module):
    def __init__(self,in_channels,kernel_size,filter_number,stride,padding):
        super(convblock,self).__init__()
        self.conv = nn.Conv2d(in_channels = in_channels, out_channels = filter_number,kernel_size=kernel_size, stride = stride, padding = padding,bias = False)
        self.batchnorm = nn.BatchNorm2d(filter_number)
        self.act = nn.ReLU()
    def forward(self,x):
        return self.act(self.batchnorm(self.conv(x)))

class LSTM(nn.Module):
    def __init__(self, input_len = 16, hidden_size=1, num_layers=1):
        super(LSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_len,hidden_size,num_layers,batch_first=True)
    def forward(self,x):
        hidden_states = torch.zeros(self.num_layers, x.size(0),self.hidden_size).to(device)
        cell_states = torch.zeros(self.num_layers, x.size(0),self.hidden_size).to(device)
        out, _ = self.lstm(x,(hidden_states,cell_states))
        return out

#model
class cnnnet1(nn.Module):
    def __init__(self,in_channels = 1):
        super(cnnnet1,self).__init__()
        self.arch = arch_1
        self.in_channels = in_channels
        self.Cnn = self.Create_conv_layers(self.arch)
        self.nn = self.create_nn()
        self.flatten = nn.Flatten()
        self.lstm = LSTM()
    def forward(self,x):
        intermediate = self.Cnn(x)
        xlstmi = x[:,0,:,:]
        xlstm = self.lstm(xlstmi)
        #intermediate = self.flatten(intermediate)
        #intermediate = intermediate[:,None,:]
        #intermediate = intermediate.permute(2,0,1)
        intermediate = self.flatten(intermediate)
        intlstm = self.flatten(xlstm)
        #print(intlstm.shape)
        intermediate = torch.cat((intermediate,intlstm),dim=1)
        #print(intermediate.shape)
        #intermediate = intermediate.permute(1,2,0)
        return(self.nn(intermediate))
    def Create_conv_layers(self,arch):
        in_channels = self.in_channels
        list = []
        for x in arch:
            if type(x) == tuple:
                list += [convblock(in_channels,x[0],x[1],x[2],x[3])]
                in_channels = x[1]
            elif type(x) == str:
                if x == "m":
                    list += [nn.MaxPool2d(kernel_size=(2,2))]
                else:
                    list += [nn.MaxPool2d(kernel_size=(2,1))]
            elif type(x) == list:
                print("placeholder")
        return nn.Sequential(*list) # *unpcks list into nn.Sequential module
    def create_nn(self):
        return nn.Sequential(nn.Flatten(),
                             nn.Linear(1786,64,bias=True),
                             nn.Dropout(p=0.2),
                             nn.LeakyReLU(),
                             nn.Linear(64,32,bias=True),
                             nn.Dropout(p=0.2),
                             nn.LeakyReLU(),
                             nn.Linear(32,4,bias=True)
                             #nn.Softmax()
        )
#summary
#model = cnnnet1()
#summary(model,input_size=(1,1,250,16))
