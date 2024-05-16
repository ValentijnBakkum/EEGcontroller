
#from pylsl import StreamInlet, resolve_stream
import pandas as pd
import time
import logging

# initialize the streaming layer
finished = False


logger = logging.getLogger(__name__)

logging.basicConfig(filename = "test.log", level = logging.INFO)
logger.info("1")
logger.info("Init")

#streams = resolve_stream()
#inlet = StreamInlet(streams[0])

# initialize the colomns of your data and your dictionary to capture the data.
#columns=['Time','FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8','AccX','AccY','AccZ','Gyro1','Gyro2','Gyro3', 'Battery','Counter','Validation']
columns=['FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8']
data_dict = dict((k, []) for k in columns)

logger.info("Before Rprint")
print("R") #R for ready

logger.info("Before input")

recieved = input()
logger.info("Past input")
logger.info(str(recieved))

time.sleep(5)


#while not finished:
   # get the streamed data. Columns of sample are equal to the columns variable, only the first element being timestamp
   # concatenate timestamp and data in 1 list
   #data, timestamp = inlet.pull_sample()
   #all_data = data

   #print(all_data) # print the data coming from the EEG cap

   # updating data dictionary with newly transmitted samples   
   #i = 0
   #for column in data_dict.keys(): # iterate over the columns of the data dictionary
   #   data_dict[column].append(all_data[i]) # append the data to the corresponding column
   #   i = i + 1
    
   # data is collected at 250 Hz. Let's stop data collection after 60 seconds. Meaning we stop when we collected 250*60 samples.
   #if len(data_dict['Time']) >= 250*60:
      #finished = True

# lastly, we can save our data to a CSV format.
#data_df = pd.DataFrame.from_dict(data_dict)
#data_df.to_csv('EEGdata.csv', index = False)