# handles all json api boilerplate
# furnishing simple prompt-reply abstraction
# import this in your sources to make stuff easy

import requests

def getreply(prompt, url):
    try:
        api_response = requests.post(url, json={'prompt': prompt})
    except:
        return "<CONNECTION FAILED>"

    if api_response.status_code == 200:
        return api_response.json()['reply']
    else:
        return api_response.json()['status_code']
