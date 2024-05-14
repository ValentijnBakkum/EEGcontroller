import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mne

filename = input("enter file name:\n")

rawGDF = mne.io.read_raw_gdf('DataCollection/Testing dataset analysis/' + filename + '.gdf')

(events_A, events_id_A) = mne.events_from_annotations(rawGDF)

startOfRun = events_A[events_A[:, 2]==5, 0]
startIndex = startOfRun[1] + 100
stopIndex = int(((startOfRun[2] - startOfRun[1])/1.25) + startOfRun[1])

allOutputs = rawGDF.to_data_frame()

#with pd.option_context('display.max_rows', 5, 'display.max_columns', None):  # more options can be specified also
#    print(allOutputs)

numpyOutputs = allOutputs.to_numpy()

channels = numpyOutputs[startIndex:stopIndex, [1, 8, 10, 12, 20]].transpose()
counter = numpyOutputs[startIndex:stopIndex, 0].transpose()

location_array = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]

for i in range(0, 5):
    plt.subplot2grid((3,3), location_array[i])
    plt.specgram(channels[i], Fs=250)
    plt.title("EEG " + str(i+1))

plt.tight_layout()

#plt.savefig('DataCollection/Testing dataset analysis/' + filename + ' spectrum.png')

plt.figure()

for i in range(0, 5):
    plt.subplot2grid((3,3), location_array[i])
    plt.plot(counter, channels[i])
    plt.title("EEG " + str(i+1))

plt.tight_layout()


plt.show()
#plt.savefig('DataCollection/Testing dataset analysis/' + filename + '.png')