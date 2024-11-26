#!/usr/bin/env python3

task = 'text2text-generation'
model = 'google/flan-t5-base'
host = '127.0.0.1'
port = 4000
route = '/ai'

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
