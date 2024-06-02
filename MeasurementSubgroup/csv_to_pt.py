import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import torch

# Detrend function (remove DC component)
def detrend(input):
    # Define the segment size
    prompt_size = 1500
    prompts = 72000/prompt_size

    for i in range(int(prompts)):
        input[1500*i : 1500*(i+1)] = signal.detrend(input[1500*i : 1500*(i+1)], axis = 0)
    
    return input

# Filter function
def filter(df_input):
    from scipy.signal import butter, lfilter, lfilter_zi
    from scipy import signal

    # Define the filter parameters
    lowcut = 2
    highcut = 30
    fs = 250  # Sampling frequency

    # Calculate the filter coefficients
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(8, [low, high], btype='band')

    # Apply the filter to each column of the DataFrame
    df_filt = lfilter(b, a, df_input, axis = 0)

    # import scipy.signal as signal

    # Define the notch filter parameters
    fs = 250  # Sampling frequency
    f0 = 50  # Notch frequency
    Q = 1 # Quality factor

    # Design the notch filter
    b, a = signal.iirnotch(f0, Q, fs)

    # Apply the filter to each column of the DataFrame
    df_filt1 = lfilter(b, a, df_filt)
    return df_filt1

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

# Read the CSV file into a NumPy array
data_csv = pd.read_csv('C:/Users/JackC/Documents/GIthub/EEGcontroller/MeasurementSubgroup/Our_measurements/Measurement_prompt/EEGdata-2024-148--14-48-17.csv', delimiter=',')
data_csv = data_csv.iloc[:72000,:8] # select the 8 EEG channels and remove 5 samples buffer

data_csv_detr = detrend(data_csv) # remove DC component
data_csv_filt = filter(data_csv_detr) # filter the signal

data_csv = np.array(data_csv)
data_csv_res = data_csv.reshape(288, 1, 250, 8) # 288 seconds per recording, 250 samples per seconds

data_csv_torch = torch.from_numpy(data_csv_res) # Change to Torch format

logits = data_csv_torch.squeeze(1)
data_csv_torch = CAR_filter(logits)
logits = data_csv_torch.unsqueeze(1)

print(logits.shape)

#torch.Size([2880, 1, 256, 16])
# 2280 seconsd
# extra dimension
# 256 samples per sec
# 16 channels