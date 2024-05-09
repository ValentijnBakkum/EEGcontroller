import torch
import torch.nn as nn
import torch.nn.functional as F
from torchinfo import summary
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#single self attention head
class head(nn.Module):
    def __init__(self, head_size,n_channels):
        super(head,self).__init__()
        self.query = nn.Linear(n_channels,head_size)
        self.key = nn.Linear(n_channels,head_size)
        self.value = nn.Linear(n_channels,head_size)
    def forward(self,x):
        B,T,C = x.shape
        k = self.key(x)
        q = self.query(x)
        v = self.value(x)
        wei = q @ k.transpose(-2,-1) * C ** -0.5
        wei = F.softmax(wei,dim=-1)
        out = wei @ v
        return out
    
#Feedforward
class feedforward(nn.Module):
    def __init__(self,n_channels):
        super(feedforward,self).__init__()
        self.fcs = nn.Sequential(nn.Linear(n_channels,4*n_channels),
                                 nn.Dropout(p=0.3),
                                 nn.ReLU(),
                                 nn.Linear(4*n_channels,n_channels)
        )
    def forward(self,x):
        return self.fcs(x)

#multi self-attention head
class multihead(nn.Module):
    def __init__(self,n_channels,n_heads,head_size):
        super().__init__()
        self.heads = nn.ModuleList([head(int(head_size),int(n_channels)) for _ in range(n_heads)])
        self.linlay = nn.Linear(n_channels,n_channels)
    def forward(self,x):
        inter = torch.cat([h(x) for h in self.heads],dim=-1)
        out = self.linlay(inter)
        return out
    
#above classes combined    
class attentionblock(nn.Module):
    def __init__(self,n_channels,n_head):
        super().__init__()
        head_size = n_channels/n_head
        self.multihead = multihead(n_channels,n_head,head_size)
        self.feedforward = feedforward(n_channels)
        self.layernorm1 = nn.LayerNorm(n_channels)
        self.layernorm2 = nn.LayerNorm(n_channels)
    def forward(self,x):
        inter = self.multihead(x)
        inter = self.layernorm1(x+inter)
        out = self.layernorm2(self.feedforward(x)+inter)
        return out

#Dense class
class Dense(nn.Module):
    def __init__(self):
        super(Dense, self).__init__()
        self.dense = nn.Sequential(nn.Flatten(),
                                   nn.Linear(18432,256),
                                   nn.Dropout(p=0.3),
                                   nn.LeakyReLU(),    
        )
    def forward(self,x):
        return(self.dense(x))

#Class for combining whole self attention module
class blockblock(nn.Module):
    def __init__(self,num_repeat,n_channels,n_heads,length,n_embd):
        super().__init__()
        self.blocks = nn.Sequential(*[attentionblock(n_embd,n_heads) for _ in range(num_repeat)])
        self.pos_embed = nn.Embedding(length,n_embd)
        self.linear_token_embedding = nn.Linear(n_channels,n_embd)
        self.linearnorm = nn.LayerNorm(n_embd)
        self.dense = Dense()
        self.linear = nn.Linear(256,4)
    def forward(self,x):
        x = torch.squeeze(x)
        B,T,C = x.shape
        x_posembd = self.pos_embed(torch.arange(T, device = device))
        x = self.linearnorm(self.linear_token_embedding(x))
        x = x + x_posembd
        return self.linear(self.dense(self.blocks(x)))
    
#summary    
#model = blockblock(6,16,4,576,16).to(device)
#summary(model,input_size=(2,1,576,16))