#!/usr/bin/env python3

# ctrl-d to exit

import aiconnect

url = 'http://127.0.0.1:4000/ai'

def chat():
    while True:
        print('PROMPT:')
        try:
            prompt = input()
        except:
            print('<EXIT>')
            break
        print('REPLY:')
        print(aiconnect.getreply(prompt, url))
        print('-'*80)

chat()
