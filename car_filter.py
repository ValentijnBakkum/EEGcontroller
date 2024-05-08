import os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from Dataloader import DataReader

def produce_userfile(_):
    
    arg = "/Users/pragun/Technical/BAP/Data/" + _
    file = DataReader(dataset=arg)
    data = file.load_data()

    logits_batch = torch.tensor(np.asarray(data[0]), dtype = torch.float)
    targets_batch = torch.tensor(np.asarray(data[1]), dtype = torch.long)

    logits = logits_batch
    targets = targets_batch
    logits = logits[:,None,:,:]

    index = _[2]
    
    user_logits = "logitsU{}.npz".format(index)
    user_targets = "targetsU{}.npz".format(index)

    user_logitpath = os.path.join(user_directory, user_logits)
    user_targetpath = os.path.join(user_directory, user_targets)

    torch.save(logits, user_logitpath)
    torch.save(targets, user_targetpath)

def load_userfile(_):

    index = _[2]

    user_logits = "logitsU{}.npz".format(index)
    user_targets = "targetsU{}.npz".format(index)

    user_logitpath = os.path.join(user_directory, user_logits)
    user_targetpath = os.path.join(user_directory, user_targets)

    logits = torch.load(user_logitpath)
    targets = torch.load(user_targetpath)

    logits = logits.squeeze(1)

    return logits

def calculate_CAR(logits):

    channel_average = torch.zeros(288, 576)

    for i in range(int(logits.size(0))):
        for j in range(int(logits.size(1))):
            for k in range(int(logits.size(2))):
                channel_average[i][j] += logits[i][j][k]
        channel_average[i][j] = channel_average[i][j] / 16

    return channel_average

def apply_CAR(logits, channel_average):
    
    logits_CAR = torch.empty(int(logits.size(0)), int(logits.size(1)), int(logits.size(2)))

    for i in range(int(logits.size(0))):
        for j in range(int(logits.size(1))):
            for k in range(int(logits.size(2))):
                logits_CAR[i][j][k] = logits[i][j][k] - channel_average[i][j]
    
    return logits_CAR

def output_userfile(_, logits):
    index = _[2]
    user_logits = "logitsU{}.npz".format(index)
    user_logitpath = os.path.join(output_user_directory, user_logits)
    torch.save(logits, user_logitpath)


arr = os.listdir("/Users/pragun/Technical/BAP/Data")
user_directory = "/Users/pragun/Technical/BAP/EEGcontroller/userfiles"
output_user_directory = "/Users/pragun/Technical/BAP/EEGcontroller/userfiles_cleaned"

for _ in arr:
    '''
    print(_)
    produce_userfile(_)
    print('produced')
    '''
    logits = load_userfile(_)
    print('loaded')
    channel_average = calculate_CAR(logits)
    print('calculated')
    logits_CAR = apply_CAR(logits, channel_average)
    print('applied')
    logits = logits_CAR
    print('done')