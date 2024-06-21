from pylsl import StreamInlet, resolve_stream
import numpy as np
import torch
from escargot3 import escargot

# config:
#   Window settings
window = 529
overlap = 0.9

#   ML settings

# initial values:
y_win = np.zeros((window, 8))  # window array
t_win = np.zeros(window)  # time array
t = 1
i = 1
y_out = np.empty((0, 8))
t_out = np.array([])





# functions:
def filter(y):
    from scipy.signal import butter, lfilter, lfilter_zi
    from scipy import signal

    y = signal.detrend(y, axis=0)

    lowcut = 0.5
    highcut = 38
    fs = 250  # Sampling frequency

    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(4, [low, high], btype='band')

    y_filtered_band = lfilter(b, a, y, axis=0)

    # Define the filter parameters
    lowcut = 49
    highcut = 51
    fs = 250  # Sampling frequency

    # Calculate the filter coefficients
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(4, [low, high], btype='bandstop')
    #zi = lfilter_zi(b,a)*y[0]

    # Apply the filter to each column of the DataFram
    y_filtered= lfilter(b, a, np.array(y_filtered_band), axis=0)

    return y_filtered





# step 0: initialize lsl 
streams = resolve_stream()
inlet = StreamInlet(streams[0])

# step 1: read user id
user_id = input()

# step 2: load corresponding model
# *** up to machine learning group to implement
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = escargot().to(device)
#model.load_state_dict(torch.load("blockblock.pt")) # filename is temporary use user ID in future

# step 3: synchronise with gui
print("R") #R for ready
recieved = input()
if "G" != recieved:
    raise Exception(f"Expected \"G\" during synchrnisation step. Got \"{recieved}\" instead.")

# loop
while True:
    # step 4: windowing
    sample,timestamp = inlet.pull_sample() 

    overlap_win = int((1 - overlap) * window)
    if overlap_win < 1:
        raise Exception("overlap is too large")


    y_win[0, :] = sample[0:8] # EEG data 1
    t_win[0] = (i)/250 # Counter from EEG cap in seconds

    y_win = np.roll(y_win, -1)
    t_win = np.roll(t_win, -1)

    if i % window == 0 and i != window and i != 0:
        # step 5: filtering
        y_win_filt = filter(y_win)

        # step 6: Send data to GUI
        # *** omited for testing *** Update: not necessary

        # step 7: Classify window
        with torch.nograd():
            torch_data = torch.from_numpy(y_win_filt).unsqueeze(0).unsqueeze(0)
            model.eval()
            output_vector = model(torch_data.to(device, dtype=torch.float))
            classify_result = torch.max(output_vector, dim=1)[1][0].item()

        # step 8: Output classification
        print(classify_result)
    i += 1

