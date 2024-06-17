import time
import numpy as np
import pandas as pd
from pylsl import StreamInfo, StreamOutlet# Create a new stream info (name, type, channel count, nominal sampling rate, channel format, source id)

info = StreamInfo('FakeDataStream', 'EEG', 17, 250, 'float32', 'myuid34234')

# Create a new outlet with this stream info
outlet = StreamOutlet(info)

print("Now sending data...")

df = pd.read_csv("MeasurementSubgroup/Our_measurements/Measurement_prompt/EEGdata-2024-149--15-57-42.csv", sep=",")

for i in range(6):
    # Insert empty columns at index 8 to set counter at index 15, and mimic real data
    df.insert(8, 'empty_col'+str(7-i), 0)

i = 0

data = np.array(df)

while True:
    #sample = [i, i, i, i, i, i, i, i, 0, 0, 0, 0, 0, 0, 0, 0 ,0]
    sample = data[i,:]

    # Push the sample to the outlet
    outlet.push_sample(sample)
    
    # Sleep for a while (simulating a sampling rate of 250 Hz)
    time.sleep(0.004)

    if i > 72000:
        i = 0

    i += 1

# Instructions
# 1. Change the 'sample' or 'df' if needed to the desired file/data
# 2. Run this code in a seperate console
# 3. Run the code of another file needing the LSL streaming
# 4. It will stream 'sample' data (representing the real data) without needing the cap
