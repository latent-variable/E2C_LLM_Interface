import requests


URL = 'https://depot-lanes-workstation-projected.trycloudflare.com/v1/chat/completions'

HEADERS = {
    "Content-Type": "application/json"
}

HISTORY = []

def web_llm_call(prompt, conversation=False):
    if conversation:
        HISTORY.append({"role": "user", "content": prompt})
    else:
        HISTORY = [{"role": "user", "content": prompt}]
    data = {
        "mode": "instruct",
        "character":"Assistant",
        "messages": HISTORY
    }
    # Call cloud API 
    response = requests.post(URL, headers=HEADERS, json=data, verify=False)

    if response.status_code != 200:
        print(response.status_code)
        print(response.json())
        return None

    assistant_message = response.json()['choices'][0]['message']['content']
    HISTORY.append({"role": "assistant", "content": assistant_message})
    print(assistant_message)
    return assistant_message




if __name__=="__main__":
    prompt = "Translate the following to english: " + "Hola, como estas?"
    web_llm_call(prompt, conversation=False)


