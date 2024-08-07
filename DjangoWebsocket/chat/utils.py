import requests
from django.shortcuts import redirect
from .api_key import API_KEY

def translate(target_lang: str, sentence: str) -> str:
    url = "https://microsoft-translator-text.p.rapidapi.com/translate"

    querystring = {
        "api-version": "3.0",
        "profanityAction": "NoAction",
        "textType": "plain",
        "to": f"{target_lang}"}

    payload = [{
        "Text": f"{sentence}",
    }]

    headers = {
        "x-rapidapi-key": f"{API_KEY}",
        "x-rapidapi-host": "microsoft-translator-text.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)
    return response.json()[0]['translations'][0]['text']