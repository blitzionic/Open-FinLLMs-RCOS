import pandas as pd
import requests
import openai
import json
import time
import os
from mistralai import Mistral

with open('config.json', 'r') as configFile:
  config = json.load(configFile)

openai.api_key = config['openai_api_key']
MISTRAL_API_KEY = config['mistral_api_key']
OLLAMA_API_URL = 'http://localhost:11434/api/generate'

client = Mistral(api_key=MISTRAL_API_KEY)

def prompt_gpt4o(systemPrompt, userPrompt):
  try:
    response = openai.ChatCompletion.create(
      model='gpt-4',
      messages=[
        {'role': 'system', 'content': systemPrompt},
        {'role': 'user', 'content': userPrompt}
      ],
      temperature=0.0,
      maxTokens=100
    )
    return response['choices'][0]['message']['content'].strip()
  except Exception as err:
    return f"Error: {err}"
  
def prompt_llama(systemPrompt, userPrompt):
  try:
    promptText = f"{systemPrompt}\n\n{userPrompt}"
    payload = {
      "model": "llama3.1",
      "prompt": promptText,
      "temperature": 0.0
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()
    responseText = response.text.strip()
    responseLines = responseText.splitlines()
        
    result = ''
        
    for line in responseLines:
      line = line.strip()
      if line:
        try:
          data = json.loads(line)
          result += data.get('response', '')
        except json.JSONDecodeError as err:
          print(f"JSONDecodeError: {err}")
          continue
        
    return result.strip()
  except Exception as err:
    print(f"Llama3 Error: {err}")
    return f"Error: {err}"
