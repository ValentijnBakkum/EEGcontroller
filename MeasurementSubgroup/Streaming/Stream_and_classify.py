from pylsl import StreamInlet, resolve_stream
import numpy as np
import torch

# config:
#   Window settings
window = 50
overlap = 0.9

# initial values:
y_win = np.zeros(window, 8)  # window array
t_win = np.zeros(window)  # time array
t = 1
i = 1
y_out = np.array([])
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
    b, a = butter(8, [low, high], btype='band')
    zi = lfilter_zi(b,a)*y[0]

    y_filtered_band, _= lfilter(b, a, np.array(y), zi = zi, axis=0)

    fs = 250  # Sampling frequency
    f0 = 50  # Notch frequency
    Q = 1 # Quality factor

    b, a = signal.iirnotch(f0, Q, fs)
    zi = lfilter_zi(b,a)*y[0]

    y_filtered, _ = lfilter(b, a, np.array(y_filtered_band), zi = zi, axis=0)

    return y_filtered





# step 0: initialize lsl 
streams = resolve_stream()
inlet = StreamInlet(streams[0])

# step 1: read user id
user_id = input()

# step 2: load corresponding model
# *** up to machine learning group to implement

# step 3: synchronise with gui
print("R") #R for ready
recieved = input()
if "G" != recieved:
    raise Exception(f"Expected \"G\" during synchrnisation step. Got \"{recieved}\" instead.")

# loop
while True:
    # step 4: windowing
    sample,timestamp = inlet.pull_sample() 

    overlap_win = int(overlap * window)

    y_win[0] = sample[0:7] # EEG data 1
    t_win[0] = (i)/250 # Counter from EEG cap in seconds

    y_win = np.roll(y_win, -1)
    t_win = np.roll(t_win, -1)

    if i % window == 0 and i != window and i != 0:
        # step 5: filtering
        y_win_filt = filter(y_win)

        y_shift = y_win_filt[overlap_win:]
        t_shift = t_win[overlap_win:]

        y_shift = np.array(y_shift)
        t_shift = np.array(t_shift)

        y_out = np.concatenate((y_out, y_shift))
        t_out = np.concatenate((t_out, t_shift))

        # step 6: Send data to GUI
        # *** omited for testing ***

        # step 7: Classify window
        torch_data = torch.from_numpy(y_out).unsqueeze(0).unsqueeze(0)
        # *** up to machine learning group to implement

        # step 8: Output classification
        print(classify_result)

