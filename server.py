# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 15:50:01 2023

@author: izael.silva
"""

from flask import Flask, request, abort, json
import openai
import requests
import os
#from flask_ngrok import run_with_ngrok

app = Flask(__name__)
#run_with_ngrok(app)


messages = [
    #{"role": "system", "content": OPENAI_API_PROMPT},
]

@app.route('/')
def index():
   return "Server is running."

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    input_response = request.get_json()
    if request.method == 'GET':
        VERIFY_TOKEN = 'token_whats_teste'
        mode = request.GET['hub.mode']
        token = request.GET['verify_token']
        challenge = request.GET['hub.challenge']
        
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification token missmatch", 403
               

    # return "Hello world", 200

    if request.method == 'POST':
        try:
            print(input_response['entry'][0]['changes'][0]['value']['messages'])
            if input_response['entry'][0]['changes'][0]['value']['messages'][0]['id']:
                    input = input_response['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
                    number = input_response['entry'][0]['changes'][0]['value']['messages'][0]['from']
                    send_text_message(input, number)
        except:
            pass
        return '200 OK HTTPS.'    


def send_text_message(input, number):
        response_assistant = get_assistant_response(input)
        headers = {
            'Authorization': 'Bearer ' #+ WHATSAPP_API_KEY,
        }
        json_data = {
            'messaging_product': 'whatsapp',
            'to': number,
            'type': 'text',
            "text": {
                "body": response_assistant
            }
        }
        response = requests.post('https://graph.facebook.com/v13.0/116493838087495/messages', headers=headers, json=json_data)
        print(response.text)
    
def get_assistant_response(input):
     if input:
        messages.append({"role": "user", "content": input})
        assistant = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        temperature=1,
                        messages=messages
                    )
        response_assistant = assistant.choices[0].message.content
        messages.append({"role": "assistant", "content": response_assistant})
        print(response_assistant)
        return response_assistant

@app.route('/issue',methods=['POST'])
def issue():
    data = request.json
    print(f'Issue {data["issue"]["title"]} {data["action"]}')
    print(f'{data["issue"]["body"]}')
    print(f'{data["issue"]["url"]}')
    return data

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
                      