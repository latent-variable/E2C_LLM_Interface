import pandas as pd 
import requests
from deep_translator import GoogleTranslator

URL = "http://127.0.0.1:5000/v1/chat/completions"

HEADERS = {
    "Content-Type": "application/json"
}

HISTORY = []

def local_llm_call(prompt, conversation=False):
    if conversation:
        HISTORY.append({"role": "user", "content": prompt})
    else:
        HISTORY = [{"role": "user", "content": prompt}]
    data = {
        "mode": "instruct",
        "messages": HISTORY
    }
    # Call local API
    response = requests.post(URL, headers=HEADERS, json=data, verify=False)
    assistant_message = response.json()['choices'][0]['message']['content']
    HISTORY.append({"role": "assistant", "content": assistant_message})
    print(assistant_message)
    return assistant_message


def translate_using_googletrans(data):

    # Translate the text
    print(data['title'])
    title_translation = GoogleTranslator(source='auto', target='en').translate(data['title'])

    # Print the translated text
    print(title_translation)
    data['title_Google_en'] = title_translation

    # Translate the text
    results_translation = GoogleTranslator(source='auto', target='en').translate(data['resulting_text'])

    # Print the translated text
    print(results_translation)
    data['resulting_text_Google_en'] = results_translation

    return data

# Create a translator object

def translate_data_using_llm(data): 

    # Call local API for translation on title
    prompt = "Translate the following to english: " + data['title']
    data['title_Orion_en'] = local_llm_call(prompt, conversation=False)

    # Call local API for translation on resulting_text
    prompt = "Translate the following to english: " + data['resulting_text']
    data['resulting_text_Orion_en'] = local_llm_call(prompt, conversation=False)


    return data
    

  
def translate_test():
    from deep_translator import GoogleTranslator
    print(GoogleTranslator(source='auto', target='es').translate("keep it up, you are awesome"))



def clean_data(file_path):

    

    df = pd.read_csv(file_path)

    print(df.columns)

    df = df.drop_duplicates(subset=['title', 'resulting_text'], keep='first')

    # removed any rows with empty title or resulting_text
    df = df.dropna(subset=['title', 'resulting_text'])

    #save the cleaned data
    file_path = file_path.replace('.csv', '_cleaned.csv')
    df.to_csv(file_path, index=False)



def add_llm_sumamry_column(data):
    # Call local API for summarization    
    prompt = "Summarize the following: " + str(data['translated_title']) + ' ' + str(data['translated_content'])
    data['english_summary'] = local_llm_call(prompt, conversation=False)

    return data


def main(file_path):
    # prompt = "tell me how to In order to make homemade bread,:\n1)"
    # Load the xlsx data
    df = pd.read_csv(file_path)
    # columns title, resulting_text, input_url, returned_url,date

    out_file_path = file_path.replace('.csv', '_summarized.csv')

    # Add the translated columns
    df['english_summary'] = [None] * df.shape[0]
    skip = 0
    for index, row in df.iterrows():
        if index < skip:
            continue
        print(f"Processing row {index + 1}")
        #  summary  using  add_llm_sumamry_column
        row = add_llm_sumamry_column(row)
        df.loc[index] = row

        try:
            # Save the data
            df.to_csv(out_file_path, index=False)
        except Exception as e:
            print(f"Error saving the data: {e}")



if __name__ == '__main__':
    file_path = './data/81.cn_2023-2-9_2024-1-24_translated_cleaned.csv'
    # file_path = './data/mofcom_cleaned.csv'
    # clean_data(file_path)
    main(file_path)
    # translate_test()
