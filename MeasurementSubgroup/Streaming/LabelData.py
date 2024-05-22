pageArray = [1,2,3,4 ,4,3,2,1 ,2,3,4,1 ,1,3,4,2 ,3,2,4,1 ,4,1,2,3, 0]
import pandas as pd
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
data_df["Label"] = label # add new column to the Dataframe
data_df.to_csv('MeasurementSubgroup/Our_measurements/TestLabel' + '.csv', index = False)

print(label)
print(len(label))
print("Finished")  

data_df

# 72005 = sampling_rate * seconds_per_prompt * num_prompts + 5_seconds_leeway
# 72005 = 250*(6+6)*(4*6)+5