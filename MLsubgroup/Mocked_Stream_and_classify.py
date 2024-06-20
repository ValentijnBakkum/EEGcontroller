#from pylsl import StreamInlet, resolve_stream
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

csv_array = np.genfromtxt('Data/2/EEGdata-2024-150--15-14-53.csv', delimiter=",")[1:]





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
    #zi = lfilter_zi(b,a)
    y_filtered_band = lfilter(b, a, y, axis=0)

    fs = 250  # Sampling frequency
    f0 = 50  # Notch frequency
    Q = 1 # Quality factor

    b, a = signal.iirnotch(f0, Q, fs)
    #zi = lfilter_zi(b,a)*y[0]

    y_filtered = lfilter(b, a, y_filtered_band, axis=0)

    return y_filtered

pull_sample_count = -1
def mock_pull_sample(reader):
    global pull_sample_count
    pull_sample_count += 1
    
    if pull_sample_count >= len(reader[:, 0]):
        return reader[0], 0
    else:
        return reader[pull_sample_count], 0


    




# step 0: initialize lsl 
#streams = resolve_stream()
#inlet = StreamInlet(streams[0])

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
    sample,timestamp = mock_pull_sample(csv_array)

    overlap_win = int(overlap * window)

    y_win[0, :] = np.array(sample[0:8], dtype='double') # EEG data 1
    t_win[0] = (i)/250 # Counter from EEG cap in seconds

    y_win = np.roll(y_win, -1)
    t_win = np.roll(t_win, -1)

    if i % overlap_win == 0 and i >= window:
        # step 5: filtering
        y_win_filt = filter(y_win)
        #print(f'y_win.shape = {y_win.shape}')
        #print(f'y_win_filt.shape = {y_win_filt.shape}')

        #y_shift = y_win_filt[overlap_win:]
        #t_shift = t_win[overlap_win:]
        #print(f'y_shift.shape = {y_shift.shape}')

        #y_shift = np.array(y_shift)
        #t_shift = np.array(t_shift)
        #print(f'y_shift.shape = {y_shift.shape}')

        #y_out = np.concatenate((y_out, y_shift))
        #t_out = np.concatenate((t_out, t_shift))
        #print(f'y_out.shape = {y_out.shape}')

        # step 6: Send data to GUI
        # *** omited for testing *** Update: not necessary

        print(y_win_filt.dtype)

        # step 7: Classify window
        torch_data = torch.from_numpy(y_win_filt).unsqueeze(0).unsqueeze(0)
        print(f'torch_data.shape = {torch_data.shape}')
        model.eval()
        output_vector = model(torch_data.to(device, dtype=torch.float))
        print(f'output_vector = {output_vector}')
        print(f'output_vector.shape = {output_vector.shape}')
        classify_result = torch.max(output_vector, dim=1)

        # step 8: Output classification
        print(classify_result)
    i += 1

