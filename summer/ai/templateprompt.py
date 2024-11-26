#!/usr/bin/env python3

# PROMPT MODEL TEMPLATE

task = 'text2text-generation'
model = 'google/flan-t5-base'
host = '127.0.0.1'
port = 4000
route = '/ai'

# NOTE - models have their own quirks, so dont forget to configure stuff like temperature, do_sample, max_length, etc...

# Pure (only JSON exchange) API for AI
# Meant to be run standalone. Do not import this
# So that (obviosly) multiple programs can use it simulatneosly
# Saves memory and compute cuz it runs in background

# CURL ACCESS METHOD
# curl -X POST http://127.0.0.1:4000/ai -H "Content-Type: application/json" -d '{"prompt": "hello world"}'

from transformers import pipeline

pipe = pipeline(task, model=model)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route(route, methods=['POST'])
def ai():
    if 'prompt' not in request.get_json():
        return jsonify({'error': 'no string provided'}), 400
    else:
        prompt = request.get_json()['prompt']

    reply = pipe(prompt, max_length=512, do_sample=True)[0]['generated_text']

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(host=host, port=port, debug=False)
