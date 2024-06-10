# Source: https://medium.com/the-ultimate-bedroom-bci-guide/collecting-brain-signal-data-using-the-g-tec-unicorn-eeg-headset-in-python-65240c741693

from pylsl import StreamInlet, resolve_stream
from datetime import datetime
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename = "test.log", level = logging.INFO)
logger.info('Started')

# initialize the streaming layer
finished = False

# initialize the colomns of your data and your dictionary to capture the data.
#columns=['Time','FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8','AccX','AccY','AccZ','Gyro1','Gyro2','Gyro3', 'Battery','Counter','Validation']
columns = ['FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8', 'Counter','Validation']
columns_index_dict = {'FZ': 0, 'C3': 1, 'CZ': 2, 'C4': 3,'PZ': 4, 'PO7': 5, 'OZ': 6, 'PO8': 7, 'Counter': 15, 'Validation': 16}

pageArray = [1,2,3,4 ,4,3,2,1 ,2,3,4,1 ,1,3,4,2 ,3,2,4,1 ,4,1,2,3, 0]
pageNumber = 0

# prompt time settings
prompt_time = 6 # time of each prompt in seconds
promptsamples = prompt_time * 48 * 250 # amount of samples of each recording (time * amount of prompts * sampling rate + 5 samples as buffer)

# 1. Right hand, 2. Left hand, 3. Tongue, 4. Feet, 0. Rest


while True:
   logger.info("connected")

   data_dict = dict((k, []) for k in columns)
   label = []

   streams = resolve_stream()
   inlet = StreamInlet(streams[0])

   print("R") #R for ready
   recieved = input()
   logger.info("Received1")
   logger.info(recieved)

   i = 0
   pageNumber = 0

   while not finished:
      # get the streamed data. Columns of sample are equal to the columns variable, only the first element being timestamp
      # concatenate timestamp and data in 1 list

      sample, timestamp = inlet.pull_sample()
      all_data = sample

      #logger.info(len(data_dict['Counter']))

      #print(all_data) # print the data coming from the EEG cap

      # updating data dictionary with newly transmitted samples   
      for column in data_dict.keys(): # iterate over the columns of the data dictionary
         data_dict[column].append(all_data[columns_index_dict[column]]) # append the data to the corresponding column

      ### Add label column
      if len(data_dict['Counter']) % int(250*(prompt_time * 2)) == 0: # Each prompt takes 12 seconds in total. Set pageNumber to 0 which is the rest state
         pageNumber = 0
      elif len(data_dict['Counter']) % int(250*(prompt_time)) == 0: # After 6 seconds the action will appear. Set pageNumber to pageArray[i] which is the action
         pageNumber = pageArray[i]
      else: # Else assign the same pageNumber
         pageNumber = pageNumber

      label.append(pageNumber) # Append to list label

      # After 12 seconds add 1 to i, which goes to the next prompt
      if len(data_dict['Counter']) % int(250*(prompt_time * 2)) == 0 and len(data_dict['Counter']) != 0 :
         i += 1
      
      # data is collected at 250 Hz. Let's stop data collection after 60 seconds. Meaning we stop when we collected 250*60 samples.
      if len(data_dict['Counter']) >= (promptsamples + 5): # 72005 = sampling_rate * seconds_per_prompt * num_prompts + 5_seconds_leeway
         finished = True                     # 72005 = 250*(6+6)*(4*6)+5


      if len(data_dict['Counter']) % int(promptsamples/48) == 0:
         recieved_loop = input()
         logger.info("ReceivedLoop:")
         logger.info(recieved_loop)
         if recieved_loop == "Stop":
            finished = True
            inlet.close_stream() 

   # lastly, we can save our data to a CSV format.
   data_df = pd.DataFrame.from_dict(data_dict) 
   now = datetime.now()

   logger.info(now)
   logger.info(data_dict)

   if recieved_loop != "Stop":
      recieved1 = input()
      logger.info("Received2")
      logger.info(recieved1)

      # Add column to the data_df called label
      data_df["Label"] = label # add new column to the Dataframe
      data_df.to_csv('MeasurementSubgroup/Our_measurements/Measurement_prompt/EEGdata-' + now.strftime("%Y-%j--%H-%M-%S") + '.csv', index = False)

      # Get unique values in the 'number' column
      unique_values = data_df['Label'].unique()[1:]
      subsets = {}

      # Split the DataFrame and save each subset to a separate dictionary
      for value in unique_values:
         subset_df = data_df[data_df['Label'] == value]
         subsets[value] = subset_df

      # Assign labels to seperate arrays
      Label1 = subsets.get(1)
      Label2 = subsets.get(2)
      Label3 = subsets.get(3)
      Label4 = subsets.get(4)

      # # save to csv
      if Label1 is not None and not Label1.empty:
         Label1.to_csv('MeasurementSubgroup/Our_measurements/Measurement_prompt_labels/Label_' + now.strftime("%Y-%j--%H-%M-%S") + '_1.csv', index = False)
      if Label2 is not None and not Label2.empty:
         Label2.to_csv('MeasurementSubgroup/Our_measurements/Measurement_prompt_labels/Label_' + now.strftime("%Y-%j--%H-%M-%S") + '_2.csv', index = False)
      if Label3 is not None and not Label3.empty:
         Label3.to_csv('MeasurementSubgroup/Our_measurements/Measurement_prompt_labels/Label_' + now.strftime("%Y-%j--%H-%M-%S") + '_3.csv', index = False)
      if Label4 is not None and not Label4.empty:
         Label4.to_csv('MeasurementSubgroup/Our_measurements/Measurement_prompt_labels/Label_' + now.strftime("%Y-%j--%H-%M-%S") + '_4.csv', index = False)
   else:
      # Add column to the data_df called label
      data_df["Label"] = label # add new column to the Dataframe
      data_df.to_csv('MeasurementSubgroup/Our_measurements/Measurement_prompt/EEGdata-' + now.strftime("%Y-%j--%H-%M-%S") + '_STOP.csv', index = False)

   inlet.close_stream()

   finished = False
   logger.info('Finished')