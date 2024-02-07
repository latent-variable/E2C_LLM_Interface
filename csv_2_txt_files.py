import pandas as pd 
import os 

def csv_2_txt_files(file_path, out_file_path='./text_data'):
    # Read the csv file
    data = pd.read_csv(file_path)
    
    # Convert the data to a list of dictionaries
    data = data.to_dict(orient='records')

    
    # Create a list to store the file names
    file_names = []
    
    # # Loop through the data
    for i, row in enumerate(data):
        # Create a file name
        file_name = os.path.join( out_file_path,  f"file_{i}.txt")
        
        # Append the file name to the list
        file_names.append(file_name)
        
        # Open the file and write the data
        with open(file_name, "w", encoding='utf-8') as file:
            for key, value in row.items():
                file.write(f"{key}: {value}\n")
    
    # Return the file names
    return file_names


if __name__ == "__main__":
    file_path = r"./data/mofcom_translated_cleaned_summarized.csv"
    file_names = csv_2_txt_files(file_path)
    