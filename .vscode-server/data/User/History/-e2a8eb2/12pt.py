# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 15:50:01 2023

@author: izael.silva
"""

from flask import Flask, request, abort, make_response
import openai
import os
import logging
#from heyoo import WhatsApp
from os import environ
import chat_gpt_resposta


#from flask_ngrok import run_with_ngrok

app = Flask(__name__)
#run_with_ngrok(app)

VERIFY_TOKEN = environ.get("APP_SECRET") #application secret here
WHATSAPP_API_KEY = environ.get("WHATSAPP_API_KEY")

openai.api_key = "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" #environ.get("OPENAI_API_KEY")




messages = [
    #{"role": "system", "content": OPENAI_API_PROMPT},
]
     
     # Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

@app.route('/')
def index():
   return "Server is running."

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            logging.error("Verified webhook")
            response = make_response(challenge, 200)
            response.mimetype = "text/plain"
            return response
        else:
            logging.error("Webhook Verification failed")
            return "Verification token missmatch", 403
               

    
    input_response = request.get_json()
    if request.method == 'POST':
        logging.error("Entrou no post")
        try:
            print(input_response['entry'][0]['changes'][0]['value']['messages'])
            if input_response['entry'][0]['changes'][0]['value']['messages'][0]['id']:
                    input = input_response['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
                    number = input_response['entry'][0]['changes'][0]['value']['messages'][0]['from']
                    logging.error("mandar msg para destinatário")
                    send_text_message(input, number)
        except:
            pass
        return '200 OK HTTPS.'    


def send_text_message(input, number):
        response_assistant = get_assistant_response(input)
        headers = {
            'Authorization': 'Bearer ' + WHATSAPP_API_KEY,
        }
        json_data = {
            'messaging_product': 'whatsapp',
            'to': number,
            'type': 'text',
            "text": {
                "body": response_assistant
            }
        }
        response = requests.post('https://graph.facebook.com/v16.0/111076931974481/messages', headers=headers, json=json_data)
        print(response.text)


def get_assistant_response(input):
     if input:
        logging.error("Entrou no assitente de resposta")
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
    gerar_resposta_chatgpt("Como Fazer bolo de fubá?")
                      