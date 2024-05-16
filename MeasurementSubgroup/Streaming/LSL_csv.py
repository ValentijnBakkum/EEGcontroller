from pylsl import StreamInlet, resolve_stream
from datetime import datetime
import pandas as pd

# initialize the streaming layer
finished = False
streams = resolve_stream()
inlet = StreamInlet(streams[0])

# initialize the colomns of your data and your dictionary to capture the data.
#columns=['Time','FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8','AccX','AccY','AccZ','Gyro1','Gyro2','Gyro3', 'Battery','Counter','Validation']
columns = ['FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8', 'Counter','Validation']
columns_index_dict = {'FZ': 0, 'C3': 1, 'CZ': 2, 'C4': 3,'PZ': 4, 'PO7': 5, 'OZ': 6, 'PO8': 7, 'Counter': 15, 'Validation': 16}
data_dict = dict((k, []) for k in columns)

print("R") #R for ready
recieved = input()

while not finished:
   # get the streamed data. Columns of sample are equal to the columns variable, only the first element being timestamp
   # concatenate timestamp and data in 1 list

   sample, timestamp = inlet.pull_sample()
   all_data = sample

   #print(all_data) # print the data coming from the EEG cap

   # updating data dictionary with newly transmitted samples   
   for column in data_dict.keys(): # iterate over the columns of the data dictionary
      data_dict[column].append(all_data[columns_index_dict[column]]) # append the data to the corresponding column
    
   # data is collected at 250 Hz. Let's stop data collection after 60 seconds. Meaning we stop when we collected 250*60 samples.
   if len(data_dict['Counter']) >= 500: #72005: # 72005 = sampling_rate * seconds_per_prompt * num_prompts + 5_seconds_leeway
      finished = True                     # 72005 = 250*(6+6)*(4*6)+5

# lastly, we can save our data to a CSV format.
data_df = pd.DataFrame.from_dict(data_dict)
now = datetime.now()

data_df.to_csv('MeasurementSubgroup/Our_measurements/EEGdata-' + now.strftime("%Y-%j--%H-%M-%S") + '.csv', index = False)

