import pandas as pd
import numpy as np
pageArray = [1,2,3,4 ,4,3,2,1 ,2,3,4,1 ,1,3,4,2 ,3,2,4,1 ,4,1,2,3, 0]
data_df = pd.DataFrame()
label = []
i = 0

counter = 0

while True:
    if counter % (250*(6+6)) == 0: # Each prompt takes 12 seconds in total. Set pageNumber to 0 which is the rest state
        pageNumber = 0
    elif counter % (250*(6)) == 0: # After 6 seconds the action will appear. Set pageNumber to pageArray[i] which is the action
        pageNumber = pageArray[i]
    else: # Else assign the same pageNumber
        pageNumber = pageNumber

    label.append(pageNumber) # Append to list label

    # After 12 seconds add 1 to i, which goes to the next prompt
    #if data_dict['Counter'] % 250 == 0:
    if counter % (250*(6+6)) == 0 and counter != 0 :
        i += 1

    counter += 1

    #if len(data_dict['Counter']) >= 72005: # 72005 = sampling_rate * seconds_per_prompt * num_prompts + 5_seconds_leeway
    if counter >= 72005:
         break

# Add column to the data_df called label
data_df = pd.read_csv("MeasurementSubgroup/Our_measurements/EEGdata-2024-137--16-06-51.csv")
data_df["Label"] = label # add new column to the Dataframe
data_df.to_csv('MeasurementSubgroup/Our_measurements/TestLabel' + '.csv', index = False)

# Get unique values in the 'number' column
unique_values = data_df['Label'].unique()[1:]
subsets = {}

# Split the DataFrame and save each subset to a separate dictionary
for value in unique_values:
    subset_df = data_df[data_df['Label'] == value]
    subsets[value] = subset_dfs

# Assign labels to seperate arrays
Label1 = subsets.get(1)
Label2 = subsets.get(2)
Label3 = subsets.get(3)
Label4 = subsets.get(4)

Label1.to_csv('MeasurementSubgroup/Measurement_labels/Label1Test' + '.csv', index = False)
Label2.to_csv('MeasurementSubgroup/Measurement_labels/Label2Test' + '.csv', index = False)
Label3.to_csv('MeasurementSubgroup/Measurement_labels/Label3Test' + '.csv', index = False)
Label4.to_csv('MeasurementSubgroup/Measurement_labels/Label4Test' + '.csv', index = False)

# Label1 = np.array(subsets.get(1))
# Label2 = np.array(subsets.get(2))
# Label3 = np.array(subsets.get(3))
# Label4 = np.array(subsets.get(4))

print(label)
print(len(label))
print("Finished") 
print(Label1)

# 72005 = sampling_rate * seconds_per_prompt * num_prompts + 5_seconds_leeway
# 72005 = 250*(6+6)*(4*6)+5