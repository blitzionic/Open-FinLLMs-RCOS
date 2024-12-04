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

def promptGPT4o(systemPrompt, userPrompt):
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
  
def promptLlama(systemPrompt, userPrompt):
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
  
def promptMistral(systemPrompt, userPrompt):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {MISTRAL_API_KEY}'
        }
        payload = {
            "model": "mistral-large-latest",
            "messages": [
                {"role": "system", "content": systemPrompt},
                {"role": "user", "content": userPrompt}
            ],
            "temperature": 0.0
        }
        response = requests.post('https://api.mistral.ai/v1/chat/completions', headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as err:
        print(f"Mistral Error: {err}")
        return f"Error: {err}"

def processAbbrev():
    filePath = 'Task-9 MOF License Dataset-ACM  - Sheet1.csv'
    df = pd.read_csv(filePath)

    resultColumns = [
        'GPT-4o One Shot Output', 'GPT-4o Zero Shot Output',
        'Mistral Zero-Shot Output', 'Mistral One-Shot Output',
        'Llama3 1-Shot Output', 'Llama3 0-Shot Output'
    ]
    for col in resultColumns:
        if col not in df.columns:
            df[col] = ''

    systemPrompt = (
        "You are an expert in open-source licenses. Your task is to translate the abbreviation of an open-source license into its full official name. Provide only the full license name without any additional text or explanations. If you do not recognize the abbreviation, respond with an empty string."
    )

    oneShotAbbr = 'BSD-1-Clause'
    oneShotExp = '1-clause BSD License'

    oneShotUser = (
        f"Example:\n"
        f"Abbreviation: {oneShotAbbr}\n"
        f"Full License Name: {oneShotExp}\n\n"
        f"Abbreviation: {{abbreviation}}\n"
        f"Full License Name:"
    )


    for index, row in df.iterrows():
        abbreviation = str(row['abbreviations']).strip()
        if not abbreviation:
            continue

        zeroShot = f"Abbreviation: {abbreviation}\nFull Form:"

        oneShot = oneShotUser.format(abbreviation=abbreviation)

        time.sleep(1)

        print(f"\nProcessing abbreviation '{abbreviation}' (row {index + 2}):")

        GPT4oZero = promptGPT4o(systemPrompt, zeroShot)
        print(f"GPT-4o Zero-Shot Response: {GPT4oZero}")
        GPT4oOne = promptGPT4o(systemPrompt, oneShot)
        print(f"GPT-4o One-Shot Response: {GPT4oOne}")

        mistralZero = promptMistral(systemPrompt, zeroShot)
        print(f"Mistral Zero-Shot Response: {mistralZero}")
        mistralOne = promptMistral(systemPrompt, oneShot)
        print(f"Mistral One-Shot Response: {mistralOne}")

        llamaZero = promptLlama(systemPrompt, zeroShot)
        print(f"Llama3 0-Shot Response: {llamaZero}")
        llamaOne = promptLlama(systemPrompt, oneShot)
        print(f"Llama3 1-Shot Response: {llamaOne}")

        df.at[index, 'GPT-4o Zero Shot Output'] = GPT4oZero
        df.at[index, 'GPT-4o One Shot Output'] = GPT4oOne
        df.at[index, 'Mistral Zero-Shot Output'] = mistralZero
        df.at[index, 'Mistral One-Shot Output'] = mistralOne
        df.at[index, 'Llama3 0-Shot Output'] = llamaZero
        df.at[index, 'Llama3 1-Shot Output'] = llamaOne

    print("\nColumns in DataFrame before saving:", df.columns)
    print("DataFrame head before saving:")
    print(df.head())

    df.to_csv(filePath, index=False)
    print(f"\nBenchmarking completed. Results saved to '{filePath}'.")

if __name__ == "__main__":
    processAbbrev()