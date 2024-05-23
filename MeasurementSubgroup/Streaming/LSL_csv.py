# Source: https://medium.com/the-ultimate-bedroom-bci-guide/collecting-brain-signal-data-using-the-g-tec-unicorn-eeg-headset-in-python-65240c741693

from pylsl import StreamInlet, resolve_stream
from datetime import datetime
import pandas as pd
import numpy as np

# initialize the streaming layer
finished = False
streams = resolve_stream()
inlet = StreamInlet(streams[0])

# initialize the colomns of your data and your dictionary to capture the data.
#columns=['Time','FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8','AccX','AccY','AccZ','Gyro1','Gyro2','Gyro3', 'Battery','Counter','Validation']
columns = ['FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8', 'Counter','Validation']
columns_index_dict = {'FZ': 0, 'C3': 1, 'CZ': 2, 'C4': 3,'PZ': 4, 'PO7': 5, 'OZ': 6, 'PO8': 7, 'Counter': 15, 'Validation': 16}

pageArray = [1,2,3,4 ,4,3,2,1 ,2,3,4,1 ,1,3,4,2 ,3,2,4,1 ,4,1,2,3, 0]
pageNumber = 0

# 1. Right hand, 2. Left hand, 3. Tongue, 4. Feet, 0. Rest
label = []
i = 0

while True:
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

      ### Add label column
      if len(data_dict['Counter']) % int(250*(6+6)) == 0: # Each prompt takes 12 seconds in total. Set pageNumber to 0 which is the rest state
         pageNumber = 0
      elif len(data_dict['Counter']) % int(250*(6)) == 0: # After 6 seconds the action will appear. Set pageNumber to pageArray[i] which is the action
         pageNumber = pageArray[i]
      else: # Else assign the same pageNumber
         pageNumber = pageNumber

      label.append(pageNumber) # Append to list label

      # After 12 seconds add 1 to i, which goes to the next prompt
      if len(data_dict['Counter']) % int(250*(6+6)) == 0 and len(data_dict['Counter']) != 0 :
         i += 1
      
      # data is collected at 250 Hz. Let's stop data collection after 60 seconds. Meaning we stop when we collected 250*60 samples.
      if len(data_dict['Counter']) >= 2005: # 72005 = sampling_rate * seconds_per_prompt * num_prompts + 5_seconds_leeway
         finished = True                     # 72005 = 250*(6+6)*(4*6)+5

   # lastly, we can save our data to a CSV format.
   data_df = pd.DataFrame.from_dict(data_dict) 
   now = datetime.now()
   
   # Add column to the data_df called label
   data_df["Label"] = label # add new column to the Dataframe

   data_df.to_csv('MeasurementSubgroup/Our_measurements/EEGdata-' + now.strftime("%Y-%j--%H-%M-%S") + '.csv', index = False)

   # Get unique values in the 'number' column
   unique_values = data_df['Label'].unique()[1:]
   subsets = {}

   # Split the DataFrame and save each subset to a separate dictionary
   for value in unique_values:
      subset_df = data_df[data_df['Label'] == value]
      subsets[value] = subset_df

   # Assign labels to seperate arrays
   Label1 = np.array(subsets.get(1))
   Label2 = np.array(subsets.get(2))
   Label3 = np.array(subsets.get(3))
   Label4 = np.array(subsets.get(4))

   # save to csv
   Label1.to_csv('MeasurementSubgroup/Measurement_labels/Label1' + now.strftime("%Y-%j--%H-%M-%S") + '.csv', index = False)
   Label2.to_csv('MeasurementSubgroup/Measurement_labels/Label2' + now.strftime("%Y-%j--%H-%M-%S") + '.csv', index = False)
   Label3.to_csv('MeasurementSubgroup/Measurement_labels/Label3' + now.strftime("%Y-%j--%H-%M-%S") + '.csv', index = False)
   Label4.to_csv('MeasurementSubgroup/Measurement_labels/Label4' + now.strftime("%Y-%j--%H-%M-%S") + '.csv', index = False)

   finished = False


