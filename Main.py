import torch
import torch.nn as nn
import torch.nn.functional as F
from torchinfo import summary
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#t = torch.rand(9,9,8)
#print(t)

#convnet decleration/architecture
arch_1 = [
    (5,16,1,2),
    (3,16,1,1),
    "m",
    (5,32,1,2),
    (3,32,1,1),
    "m",
    #(4,64,1,0),
    (5,64,1,2),
    (3,64,1,1),
    "m",
    (5,128,1,2),
    (3,128,1,1),
    (1,128,1,0)
    ]

#Hyperparameters

#convblock class
class convblock(nn.Module):
    def __init__(self,in_channels,kernel_size,filter_number,stride,padding):
        super(convblock,self).__init__()
        self.conv = nn.Conv2d(in_channels = in_channels, out_channels = filter_number,kernel_size=kernel_size, stride = stride, padding = padding)
        self.batchnorm = nn.BatchNorm2d(filter_number)
        self.act = nn.GELU()
    def forward(self,x):
        return self.act(self.batchnorm(self.conv(x)))

#model
class cnnnet(nn.Module):
    def __init__(self,in_channels = 1):
        super(cnnnet,self).__init__()
        self.arch = arch_1
        self.in_channels = in_channels
        self.Cnn = self.Create_conv_layers(self.arch)
        self.nn = self.create_nn()
    def forward(self,x):
        return(self.nn(self.Cnn(x)))
    def Create_conv_layers(self,arch):
        in_channels = self.in_channels
        list = []
        for x in arch:
            if type(x) == tuple:
                list += [convblock(in_channels,x[0],x[1],x[2],x[3])]
                in_channels = x[1]
            elif type(x) == str:
                list += [nn.MaxPool2d(kernel_size=(2,2))]
            elif type(x) == list:
                print("placeholder")
        return nn.Sequential(*list) # *unpcks list into nn.Sequential module
    def create_nn(self):
        return nn.Sequential(nn.Flatten(),
                             nn.Linear(7936,4096,bias=True),
                             nn.Dropout(p=0.3),
                             nn.LeakyReLU(),
                             nn.Linear(4096,4096,bias=True),
                             nn.Dropout(p=0.3),
                             nn.LeakyReLU(),
                             nn.Linear(4096,4,bias=True),
                             nn.Sigmoid()
        )
#summary
#model = cnnnet()
#summary(model,input_size=(1,1,250,16))

