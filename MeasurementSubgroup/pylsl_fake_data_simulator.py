import time
import numpy as np
from pylsl import StreamInfo, StreamOutlet# Create a new stream info (name, type, channel count, nominal sampling rate, channel format, source id)

info = StreamInfo('FakeDataStream', 'EEG', 8, 100, 'float32', 'myuid34234')

# Create a new outlet with this stream info
outlet = StreamOutlet(info)

print("Now sending data...")

# Parameters for sine wave and noise
sine_freq = 10  # Sine wave frequency in Hz
noise_freq = 50  # Noise frequency in Hz
counter = 0  # Initialize counter
sampling_rate = 250

# Start time
start_time = time.time()

while True:
    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Generate sine wave and noise
    sine_wave = np.sin(2 * np.pi * sine_freq * elapsed_time)
    noise = 0.5 * np.sin(2 * np.pi * noise_freq * elapsed_time)
    
    # Generate the sample with sine wave + noise
    sample = [sine_wave + noise for _ in range(8)]
    
    # Push the sample to the outlet
    outlet.push_sample(sample)
    
    # Increment the counter
    counter += 1
    
    # Sleep to simulate the sampling rate
    time.sleep(1 / sampling_rate)  
    
    # Sleep for a while (simulating a sampling rate of 100 Hz)
    time.sleep(0.01)