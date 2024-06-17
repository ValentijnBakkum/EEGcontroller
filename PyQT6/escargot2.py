import torch
import torch.nn as nn
import torch.nn.functional as F
from torchinfo import summary
from attentionmod import blockblock,multihead
from bspline import spline_activation
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#device = "cpu"
from kan import KAN

#convnet decleration/architecture

filer = 16
arch_2 = [
    (filer,1),
    (filer*2,1)
    #(filer*2*2,1),
    #(filer*2*2*2,1)
]

arch_wavelet = [
    (3,32,2,2),
    (3,64,2,2),
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
class convblock(nn.Module):
    def __init__(self,in_channels,filter_number):
        super(convblock,self).__init__()
        self.conv3 = nn.Conv3d(in_channels = in_channels, out_channels = filter_number,kernel_size=3, stride = 1, padding = 1, bias = False)
        self.conv5 = nn.Conv3d(in_channels = in_channels, out_channels = filter_number,kernel_size=5, stride = 1, padding = 2, bias = False)
        self.conv7 = nn.Conv3d(in_channels = in_channels, out_channels = filter_number,kernel_size=7, stride = 1, padding = 3, bias = False)
        #self.conv33 = nn.Conv3d(in_channels = filter_number, out_channels = filter_number,kernel_size=3, stride = 1, padding = 1, bias = False)
        #self.conv55 = nn.Conv3d(in_channels = filter_number, out_channels = filter_number,kernel_size=5, stride = 1, padding = 2, bias = False)
        #self.conv77 = nn.Conv3d(in_channels = filter_number, out_channels = filter_number,kernel_size=7, stride = 1, padding = 3, bias = False)
        self.batchnorm = nn.BatchNorm3d(filter_number*2)
        self.max = nn.MaxPool3d(kernel_size=(2,2,2))
        self.avg = nn.AvgPool3d(kernel_size=(2,2,2))
        self.act = nn.ReLU()
        self.dropout3d = nn.Dropout3d(p=0.1)
    def forward(self,x):
        d,i,ei,e2,e3 = x.shape
        x3 = self.act(self.conv3(x))
        #x33 = self.act(self.conv33(x3))
        #x333 = self.act(self.conv33(x3))
        x5 = self.act(self.conv5(x))
        #x55 = self.act(self.conv55(x5))
        #x7 = self.act(self.conv7(x))
        xall = torch.cat((x3,x5),dim = 1)
        x = torch.cat((x,x),dim=1)
        if i == 1:
            return self.dropout3d(self.avg(self.batchnorm(xall)))
        else:
            return self.dropout3d(self.avg(self.batchnorm(xall+x)))
    
class CNNBlock(nn.Module):
    def __init__(self,in_channels, out_channels, **kwargs):
        super(CNNBlock,self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, bias=False, **kwargs)
        self.batchnorm = nn.BatchNorm2d(out_channels)
        self.leakyrelu = nn.LeakyReLU()
    def forward(self,x):
        d,i,e2,e3 = x.shape
        if i == 16:
            return self.leakyrelu(self.batchnorm(self.conv(x)))
        else:
            return self.leakyrelu(self.batchnorm(self.conv(x)))
    
class attention(nn.Module):
    def __init__(self,n_channels,n_head):
        super().__init__()
        head_size = n_channels/n_head
        self.multihead = multihead(n_channels,n_head,head_size)
    def forward(self,x):
        inter = self.multihead(x)
        return inter

class lstmmodule1(nn.Module):
    def __init__(self, input_len = 16, hidden_size=256, num_layers=1):
        super(lstmmodule1, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.attention = attention(256,1)
        self.lstm = nn.LSTM(input_len,hidden_size,num_layers,batch_first=True, dropout = 0.3)
    def forward(self,x):
        hidden_states = torch.zeros(self.num_layers, x.size(0),self.hidden_size).to(device)
        cell_states = torch.zeros(self.num_layers, x.size(0),self.hidden_size).to(device)
        out, (hn,cn) = self.lstm(x,(hidden_states.detach(),cell_states.detach()))
        return self.attention(hn)

#model
class escargot(nn.Module):
    def __init__(self,in_channels = 1,in_channels2=16):
        super(escargot,self).__init__()
        self.arch3d = arch_2
        self.arch2d = arch_wavelet
        self.in_channels = in_channels
        self.in_channels2 = in_channels2
        self.Cnn = self.Create_conv_layers3d(self.arch3d)
        self.Cnn2d = self.Create_conv_layers2d(self.arch2d)
        self.nn = self.create_nn()
        self.flatten = nn.Flatten()
        self.lstm = lstmmodule1()
        self.norm = L2NormalizationLayer()
        self.lin = nn.Linear(5184,32)
       #self.transoferm = blockblock(1,1,4,529,22).to(device)
        self.kan = KAN([529,40,60])
    def forward(self,x,xvaw):
        N,C,H,W = x.shape # get shape of input
        
        xr = torch.reshape(x,(N,1,23,23,16)) # reshape input for convolutional neural network
        #3d convolutional part time series
        #intermediate = self.Cnn(xvaw)
        #intermediate = self.flatten(intermediate)
        
        #intermediate = self.Cnn(xvaw)
        #intermediate = self.flatten(intermediate)
        
        xa = torch.squeeze(x)
        list = []
        xa = xa.permute((2,0,1))
        for _ in range(W):
            int2 = self.kan(xa[_])
            list.append(int2)
        output = torch.stack(list)
        output = output.permute((1,2,0))
        output = self.flatten(output)
            
        #2d convolution part wavelet matrix
        #xvaw = torch.squeeze(xvaw)
        #xvaw = torch.permute(xvaw,(0,3,1,2))
        #intermediate2 = self.Cnn2d(xvaw)
        #intermediate2 = self.flatten(intermediate2)
        
        #feeding cnn into lstm
        #int3 = self.lin(intermediate2) 
        #int3 = int3[:,None,:]
        #int3 = torch.permute(int3,(0,2,1))
        #xlstmi = torch.squeeze(int3)
        #xlstm = self.lstm(int3)
        
        #concatenating in one output layer
        #xlstmi = torch.squeeze(x)
        #xlstm = self.lstm(xlstmi)
        #xlstm = torch.squeeze(xlstm)
        #intermediate = torch.cat((intermediate,xlstm,output),dim=1)
        return self.nn(output)
    
    def Create_conv_layers3d(self,arch): #creates the 3d convolution layers used before the lstm
        in_channels = self.in_channels
        list = []
        for x in arch:
            if type(x) == tuple:
                list += [convblock(in_channels,x[0])]
                in_channels = x[0]*2
            elif type(x) == list:
                print("placeholder")
        return nn.Sequential(*list)
    
    def Create_conv_layers2d(self, arch):
        layers = []
        in_channels = self.in_channels2

        for x in arch:
            if type(x) == tuple:
                layers += [
                    CNNBlock(
                        in_channels, x[1], kernel_size=x[0], stride=x[2], padding=x[3],
                    )
                ]
                in_channels = x[1]

            elif type(x) == str:
                if x == "M":
                    layers += [nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))]
                elif x == "UM":
                    layers += [nn.MaxPool2d(kernel_size=(2, 3), stride=(2, 2))]

            elif type(x) == list:
                conv1 = x[0]
                conv2 = x[1]
                num_repeats = x[2]

                for _ in range(num_repeats):
                    layers += [
                        CNNBlock(
                            in_channels,
                            conv1[1],
                            kernel_size=conv1[0],
                            stride=conv1[2],
                            padding=conv1[3],
                        )
                    ]
                    layers += [
                        CNNBlock(
                            conv1[1],
                            conv2[1],
                            kernel_size=conv2[0],
                            stride=conv2[2],
                            padding=conv2[3],
                        )
                    ]
                    in_channels = conv2[1]

        return nn.Sequential(*layers)
    def create_nn(self): #creates the nn used in the model
        return nn.Sequential(nn.Flatten(),
                             nn.Linear(160*6,512,bias=True),
                             nn.Dropout(p=0.2),
                             #nn.ReLU(),
                             L2NormalizationLayer(),
                             spline_activation(device = device,grid = 5, input_dim = 512),
                             nn.Linear(512,16),
                             #nn.Dropout(p=0.3),
                             #nn.ReLU(),
                             L2NormalizationLayer()
                             #spline_activation(device = device,grid = 5, input_dim = 32),
                             #nn.Linear(32,4),
                             #L2NormalizationLayer()
                             #nn.Softmax()
        )
    

#summary of the model
#model = escargot().to(device)
#summary(model, [(40,1,529,16),(40,1,27,27,16)])
#a = torch.rand(40,1,529,16).to(device)
#b = torch.rand(40,1,40,40,16).to(device)
#print(model(a,b))