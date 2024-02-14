import os
import pandas as pd
from random import randint
import time

# Return 10 consecutive rows from a dataframe starting from a random timestamp
def get_consecutive_rows(data):
    random_start = randint(0, len(data) - 10)
    return data.iloc[random_start: random_start + 10]

def predict_next_3_values(data):
    price_column = data.columns[2] 
    highest_value = data[price_column].nlargest(2).iloc[1]
    first_prediction = highest_value
    second_prediction = first_prediction - (first_prediction - data[price_column].iloc[-1]) / 2      # I chose to make my predictions according to the last 
    third_prediction = second_prediction - (second_prediction - first_prediction) / 4                         # predicted value in order to have closer values to the sampled data

    #second_prediction = (first_prediction - data[price_column].iloc[-1]) / 2                # Uncomment these lines if you would like to have the requested prediction algorithm
    #third_prediction = (second_prediction - first_prediction) / 4                                   # and comment lines 15 and 16

    # Get the last timestamp value from the DF
    last_timestamp = pd.to_datetime(data['Timestamp'].iloc[-1], format='%d-%m-%Y')
    
    # Calculate next 3 days
    timestamps = pd.date_range(start=last_timestamp + pd.Timedelta(days=1), periods=3, freq='D')
    
    # Create a DataFrame based on the predictions
    predictions_df = pd.DataFrame({
        'Stock-ID': [data['Stock-ID'].iloc[0]] * 3,  
        'Timestamp': timestamps.strftime('%d-%m-%Y'),
        'Stock-Price': [first_prediction, second_prediction, third_prediction]
    })
    data = pd.concat([data, predictions_df], ignore_index=True)
    
    return data

def save_to_csv(dataframe, dest_path):
    try:
        dataframe.to_csv(dest_path, header=None, index=False)
    except PermissionError:     #Adding delay in order to close the file
        print(f"'{dest_path}' is currently opened by another program. Please close it and make sure you saved your work in a different file as this one will be replaced.")
        print("Retrying in 10 seconds...")
        time.sleep(10)
        save_to_csv(dataframe, dest_path)

# Main function 
def process_files(folder_path, num_files): 
    if num_files == 0:
        print("\nNo prediction was made. Have a nice day!\n")
        return("Please change the 'num_file' value to 1 or 2")   
    for dir_path, _, files in os.walk(folder_path):      
        counter = 0   
        if not files and dir_path != folder_path:
            print("\nWARNING! The below folders have no CSV files.")
            print(os.path.basename(dir_path),"\n")                  
        for file in files:          
            counter += 1                             
            data = pd.DataFrame(columns=['Stock-ID', 'Timestamp', 'Stock-Price'])
            if file.endswith('.csv'):  
                file_path = os.path.join(dir_path, file)
                temp_data = pd.read_csv(file_path, header=None, names=['Stock-ID', 'Timestamp', 'Stock-Price'])
                data = pd.concat([data, temp_data], ignore_index=True)
                if(len(data) < 10):
                    print("\nThe below file has under 10 rows. A prediction can`t be made. ")
                    print(os.path.basename(file_path),"\n")
                    break
                consecutive_data = get_consecutive_rows(data)
                predictions = predict_next_3_values(consecutive_data)
                final_csv_file = file.replace('.csv', '_output.csv')
                save_to_csv(predictions, final_csv_file)
                print("Data saved to", final_csv_file)

            if counter >= num_files:
                break

# Input parameters
num_files_input = 1
folder_name = "stock_price_data_files"

# Main execution
directory_path = os.path.join(os.getcwd(), folder_name)
process_files(directory_path, num_files_input)
