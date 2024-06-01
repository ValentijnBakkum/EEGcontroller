import time
import numpy as np
import pandas as pd
from pylsl import StreamInfo, StreamOutlet# Create a new stream info (name, type, channel count, nominal sampling rate, channel format, source id)

info = StreamInfo('FakeDataStream', 'EEG', 8, 250, 'float32', 'myuid34234')

# Create a new outlet with this stream info
outlet = StreamOutlet(info)

print("Now sending data...")

df = pd.read_csv("MeasurementSubgroup/Our_measurements/Measurement_prompt/EEGdata-2024-149--15-57-42.csv", sep=",")
i = 0

while True:
    print(np.array(df[i,:8]))
    sample = np.array(df[i,:8])

    # Push the sample to the outlet
    outlet.push_sample(sample)
    
    # Sleep for a while (simulating a sampling rate of 100 Hz)
    time.sleep(0.004)

    i += 1

# Instructions