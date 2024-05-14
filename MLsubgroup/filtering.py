import os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from Dataloader import DataReader

files = os.listdir("C:\\Users\\Gebruiker\\Desktop\\Bap\\Data")
print(files)
output_directory = "C:\\Users\\Gebruiker\\Desktop\\Bap\\Code"

def CAR_filter(logits):
    a,b,c = logits.shape
    # initialise zero tensor to hold channel average
    channel_average = torch.zeros(2880, 256)

    # compute average for each channel
    for i in range(int(logits.size(0))):
        for j in range(int(logits.size(1))):
            for k in range(int(logits.size(2))):
                channel_average[i][j] += logits[i][j][k]
            channel_average[i][j] = channel_average[i][j] / 16
    
    # initalise empty tensor to hold filtered logits
    logits_CAR = torch.empty(int(logits.size(0)), int(logits.size(1)), int(logits.size(2)))

    # subtract all readings by channel average to create new 'reference' signals
    for i in range(int(logits.size(0))):
        for j in range(int(logits.size(1))):
            for k in range(int(logits.size(2))):
                logits_CAR[i][j][k] = logits[i][j][k] - channel_average[i][j]
    
    return logits_CAR

def freq_filter(logits):

    # set parameters
    fs = 250
    T = 1 / fs
    L = 256

    # perform FFT
    fft_logits = torch.fft.fftn(logits, dim=(1,))

    # create frequency mask
    frequencies = torch.fft.fftfreq(L, d=T)
    mask = (frequencies >= 0.5) & (frequencies <= 30)
    full_mask = torch.zeros_like(fft_logits, dtype=torch.bool)
    full_mask[:, :len(mask), :] = mask[None, :, None]
    reversed_mask = torch.flip(mask, dims=[0])  
    full_mask[:, -len(mask):, :] = reversed_mask[None, :, None]

    # apply frequency mask
    fft_logits_masked = fft_logits * full_mask

    # perform IFFT
    logits_filtered = torch.fft.ifftn(fft_logits_masked, dim=(1,)).real

    return logits_filtered

for _ in files:

    # set index
    index = _[2]                                                       
    print(_)
    # read/load .npz file for user
    npz_loc = "C:\\Users\\Gebruiker\\Desktop\\Bap\\Data\\" + _                  
    file = DataReader(dataset=npz_loc)                                  
    data = file.load_data()                                             

    # produce tensor for logits and targets
    logits = torch.tensor(np.asarray(data[0]), dtype = torch.float)     
    targets = torch.tensor(np.asarray(data[1]), dtype = torch.long)    
    logits = logits[:,None,:,:]                                        
    logits = logits.squeeze(1)
    
    # perform filtering on logits (calling functions written above)
    logits = CAR_filter(logits) # spatial filtering (CAR)
    logits = freq_filter(logits) # frequency filtering
    logits = logits.unsqueeze(1)

    # set file name for output
    user_logits = "logitsU{}.pt".format(index)                         
    user_targets = "targetsU{}.pt".format(index) 

    # set path for output
    user_logitpath = os.path.join(output_directory, user_logits)
    user_targetpath = os.path.join(output_directory, user_targets)
    
    if _ == "A01T.npz":
          logitsall = logits
          targetsall = targets
    else:
          logitsall = torch.cat((logitsall,logits),dim = 0)
          targetsall = torch.cat((targetsall,targets),dim = 0)
    # output cleaned/filtered logits and targets
    torch.save(logits, user_logitpath)
    torch.save(targets, user_targetpath)
    
torch.save(logitsall, "logits0.5-30-1s")
torch.save(targetsall, "targets0.5-30-1s")

