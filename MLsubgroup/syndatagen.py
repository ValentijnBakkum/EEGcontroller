import torch
import torch.nn as nn
from torch.nn import functional as F
import tiktoken
from torchinfo import summary
enc = tiktoken.get_encoding('r50k_base')

torch.manual_seed(26)

#-----HYPERPARAMETERS/model-----#                   -------diff hyperparameters
vocab_size = enc.n_vocab
block_size = 512
n_embd = 768 #head_size and n_embd need to be divisible to integer otherwise a dimension mismatch input will occur due to rounding
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
n_layer = 12
n_head = 64
#-----HYPERPARAMETERS/model-----#

#-----HEADCLASS-----#
class head(nn.Module):
    def __init__(self,head_size):
        super().__init__()
        self.key = nn.Linear(n_embd,head_size, bias = False)
        self.query = nn.Linear(n_embd, head_size, bias = False)
        self.value = nn.Linear(n_embd,head_size, bias = False)
        self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))
    def forward(self,x):
        B,T,C = x.shape
        k = self.key(x) #(b,t,head_size) Key
        #print(k)
        q = self.query(x) #(b,t,head_size) Query
        #matmul
        wei = q @ k.transpose(-2,-1) * C **-0.5 #(b,t,head_size) * (b,head_size,t) = (b,t,t)
        #mask
        wei = wei.masked_fill(self.tril[:T,:T] == 0,float('-inf'))
        wei = F.softmax(wei, dim=-1)# returns matrix of characters importance for time component
        v = self.value(x) #(b,t,head_size) Value
        out = wei @ v # (b,t(time component),t(Characters importance)) * (b,t,head_size) = (b,t,head_size)
        return out
#-----HEADCLASS-----#

#-----MULTIHEADCLASS-----#
class multihead(nn.Module):
    def __init__(self,num_heads,head_size):
        super().__init__()
        self.heads = nn.ModuleList([head(head_size) for _ in range(num_heads)])
        self.l = nn.Linear(n_embd,n_embd)
    def forward(self,x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.l(out)
        return out
#-----MULTIHEADCLASS-----#
    
#-----FEEDFORWARDCLASS-----#
class feed_forward(nn.Module):
    def __init__(self,n_embd):
        super().__init__()
        self.network = nn.Sequential(nn.Linear(n_embd, 4*n_embd),
                                     nn.ReLU(),
                                     nn.Linear(4*n_embd,n_embd))
    def forward(self,x):
        out = self.network(x)
        return out
#-----FEEDFORWARDCLASS-----#
    

#-----COMBINEDCLASS-----#
class block(nn.Module):
    def __init__(self,n_embd,n_heads):
        super().__init__()
        head_size = n_embd // n_heads 
        self.multihead = multihead(n_heads,head_size)
        self.ff = feed_forward(n_embd)
        self.l1n = nn.LayerNorm(n_embd)
        self.l2n = nn.LayerNorm(n_embd)
    def forward(self,x):
        x = x + self.multihead(self.l1n(x))
        out = x + self.ff(self.l2n(x))
        return out
#-----COMBINEDCLASS-----# 

#-----MODEL-----#
class Vaucluse(nn.Module):
    def __init__(self):
        super().__init__()
        self.tokenembeddingtable = nn.Embedding(vocab_size,n_embd)
        self.positionalembedding = nn.Embedding(block_size,n_embd)
        self.blocks = nn.Sequential(*[block(n_embd, n_heads=n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd)
        self.lm_head = nn.Linear(n_embd, vocab_size)
    def forward(self,idx,targets=None):  
        B,T = idx.shape
        tokens = self.tokenembeddingtable(idx)# B,T,C token embedding
        pos_embedding = self.positionalembedding(torch.arange(T,device = device))# positional embedding T,C
        x = tokens + pos_embedding
        x = self.blocks(x)
        x = self.ln_f(x)
        logits = self.lm_head(x)
        if targets is None:                             # --------different loss
            loss = None
        else:
            B,T,C = logits.shape
            logits = logits.view(B*T,C)
            targets = targets.view(B*T)
            loss = F.mse_loss(logits,targets)
        return logits,loss
    def generate(self,idx,max_new_tokens):
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -block_size:]
            # get the predictions
            logits, loss = self(idx_cond)
            # focus only on the last time step
            logits = logits[:, -1, :] # becomes (B, C)
            # apply softmax to get probabilities
            probs = F.softmax(logits, dim=-1) # (B, C)
            # sample from the distribution
            idx_next = torch.multinomial(probs, num_samples=1) # (B, 1)
            # append sampled index to the running sequence
            idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)
        return idx
#-----MODEL-----#
