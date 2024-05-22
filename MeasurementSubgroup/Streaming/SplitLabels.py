import pandas as pd
df = pd.read_csv("MeasurementSubgroup/Measurement_Labels/TestLabel.csv")

# Get unique values in the 'number' column
unique_values = df['Label'].unique()

# Split the DataFrame and save each subset to a separate CSV file
for value in unique_values:
    subset_df = df[df['Label'] == value]
    
    #filename = f'MeasurementSubgroup/Measurement_Labels/TestLabel_{value}' + '.csv'
    #subset_df.to_csv(filename, index=False)