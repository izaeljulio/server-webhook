# -*- coding: utf-8 -*-
"""
Created on Thu May 11 14:36:12 2023

@author: Izael
"""

import requests
import json

API_KEY = "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"

def gerar_resposta_chat_gpt(input):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    link = "https://api.openai.com/v1/chat/completions"
    id_modelo = "gpt-3.5-turbo"


    body_mensagem = {
        "model": id_modelo,
        "messages": [{"role": "user", "content": "como fazer bolo de fubá?"}]
        }

    body_mensagem = json.dumps(body_mensagem)

    requisicao = requests.post(link, headers=headers, data=body_mensagem)

    resposta = requisicao.json()
    mensagem = resposta["choices"][0]["message"]["content"]
    print(mensagem)



if __name__ == '__main__':
    gerar_resposta_chat_gpt("Como Fazer bolo de fubá?")