import numpy as np
import os

def multifile(directory):

    output = np.empty((0, 11), dtype=int)
    events = np.empty((0,  3), dtype=int)
    i = 0
    
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            data = np.genfromtxt(file_path, delimiter=',')[1:, :]
            output = np.concatenate((output, data), axis=0)
            temp_events = np.array([[1500, 0, 1],
                                    [4500, 0, 2],
                                    [7500, 0, 3],
                                    [10500, 0, 4],
                                    [13500, 0, 4],
                                    [16500, 0, 3],
                                    [19500, 0, 2],
                                    [22500, 0, 1],
                                    [25500, 0, 2],
                                    [28500, 0, 3],
                                    [31500, 0, 4],
                                    [34500, 0, 1],
                                    [37500, 0, 1],
                                    [40500, 0, 3],
                                    [43500, 0, 4],
                                    [46500, 0, 2],
                                    [49500, 0, 3],
                                    [52500, 0, 2],
                                    [55500, 0, 4],
                                    [58500, 0, 1],
                                    [61500, 0, 4],
                                    [64500, 0, 1],
                                    [67500, 0, 2],
                                    [70500, 0, 3]])
            temp_events[:, 0] = temp_events[:, 0] + (i * 72005)
            events = np.concatenate((events, temp_events), axis=0)
            i = i + 1

    return (output, events)

directory = '/Users/pragun/Technical/BAP/2'
allOutputs, events = multifile(directory)

output_csv_path = os.path.join(directory, 'combined_output.csv')
events_csv_path = os.path.join(directory, 'combined_events.csv')

np.savetxt(output_csv_path, allOutputs, delimiter=',', fmt='%d')
np.savetxt(events_csv_path, events, delimiter=',', fmt='%d')