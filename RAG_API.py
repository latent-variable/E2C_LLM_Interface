import requests
import pandas as pd 

URL = "http://127.0.0.1:5002/api/v1/"
"http://192.168.0.12:5002/api/v1/"

HEADERS = {
    "Content-Type": "application/json"
}

def GET_docs_call(prompt, conversation=False):

    data = {
        "mode": "instruct",
        "search_strings": [prompt]
        # "messages": HISTORY
    }

    # Call local API for fallacy detection or other tasks
    response = requests.post(URL +'get', headers=HEADERS, json=data, verify=False)
    if response.status_code != 200:
        print(response.status_code)
        print(response.json())
        return None
    
    print(response.json()['results'][1])
    # assistant_message = response.json()['choices'][0]['message']['content']
    # HISTORY.append({"role": "assistant", "content": assistant_message})
    # print(assistant_message)
    # return assistant_message


def ADD_Docs_Call(corpus, metadata=None, clear_before_adding=False):
    data = {
        "corpus": corpus, 
        "clear_before_adding": clear_before_adding,
        "metadata": {
            "source": "API-ADD"
        }
    }
    response = requests.post(URL +'add', headers=HEADERS, json=data, verify=False)
    print(response.json())


# Add the data to the corpus
def add_csv_data_to_corpus(file_path):
    # Read the csv file
    data = pd.read_csv(file_path)
    
    # Convert the data to a list of dictionaries
    data = data.to_dict(orient='records')
    
    # # Loop through the data
    for i, row in enumerate(data):
        if i ==1:
            # Create a file name
            corpus = row['english_summary']
            metadata = {
                "source": "mofcom",
                "title": row['title'],
                "translated_title": row['translated_title'],
            }
            ADD_Docs_Call(corpus, metadata=metadata)



# reset the database
def clear_DB():
    print("Clearing the database")
    print(URL +'clear')
    response = requests.delete(URL +'clear', headers=HEADERS, verify=False)
    print(response.json())


            
    
if __name__ == "__main__":
    # prompt = "Methods of levying anti-dumping duties From January 1, 2023? "
    # GET_docs_call(prompt, conversation=False)

    file_path = r"./data/mofcom_translated_cleaned_summarized_v2.csv"
    add_csv_data_to_corpus(file_path)


    # clear_DB()