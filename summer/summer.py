#!/usr/bin/env python3

# works best with lamini flan-t5

from flask import Flask, request, jsonify

app = Flask(__name__)

import aiconnect

def preprocess(title, text):
    asciionly = ''.join([char for char in text if char.isascii()])
    linelist = [line for line in asciionly.split('\n')]
    minlinelen = 100
    biglines = [line for line in linelist if len(line)>=minlinelen]
    processed = ''.join(biglines)
    title = 'Title: '+title+'\n'
    text = 'Text: '+processed
    final = title + text
    return final

def getsummary(text):
    maxcharinput = 460
    prefix = ''
    suffix = '. Brief:'
    prompt = prefix + text[:maxcharinput] + suffix
    aiurl = 'http://127.0.0.1:4000/ai'
    summary = aiconnect.getreply(prompt, aiurl)
    return summary

def gettag(summary):
    prefix = ''
    suffix = '. Classification: -Education. -Entertainment. -Health. -Food. -Technology. -Business. -Science. -Aesthetics. -Politics. -Finance. Class:'
    prompt = prefix + summary + suffix
    aiurl = 'http://127.0.0.1:4000/ai'
    tag = aiconnect.getreply(prompt, aiurl)
    return tag

@app.route('/summer', methods=['POST'])
def summer():
    data = request.json
    if 'title' in data and 'text' in data:
        title = data['title']
        text = data['text']

        title = title
        processedtext = preprocess(title, text)
        summary = getsummary(processedtext)
        tag = gettag(summary)

        return jsonify({'title': title, 'tag': tag, 'summary': summary})
    
    else:
        return jsonify({'error': 'data missing'}), 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
