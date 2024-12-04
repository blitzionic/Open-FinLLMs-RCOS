import pandas as pd
import requests
import openai
import json
import time
from mistralai import Mistral

def create_questions(source, destination):

    source_file = source
    destination_file = destination

    df = pd.read_excel(source_file)

    column1 = 'Term'
    column2 = 'Explanation'

    question_list = []
    answer_list = []

    for row in df.iterrows():
        term = str(row[column1]).strip()
        answer = str(row[column2]).strip()

        term_question = f"What is the definition of the term '{term}' in XBRL?"

        question_list.append(term_question)
        answer_list.append(answer)

    df['Question'] = question_list
    df['Answer'] = answer_list

    df = df[['Question', 'Answer']]

    df.to_excel(destination_file, index=False)

    print(f"Combined columns have been copied to '{destination_file}'.")

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

openai.api_key = config['openai_api_key']
MISTRAL_API_KEY = config['mistral_api_key']
OLLAMA_API_URL = 'http://localhost:11434/api/generate'

client = Mistral(api_key=MISTRAL_API_KEY)

def prompt_gpt4o(system_prompt, user_prompt):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            temperature=0.0,
            max_tokens=100
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"

def prompt_llama(system_prompt, user_prompt):
    try:
        prompt_text = f"{system_prompt}\n\n{user_prompt}"
        payload = {
            "model": "llama3.1",
            "prompt": prompt_text,
            "temperature": 0.0
        }
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        
        response_text = response.text.strip()
        
        response_lines = response_text.splitlines()
        
        result = ''
        
        for line in response_lines:
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    result += data.get('response', '')
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e}")
                    continue 
        
        return result.strip()
    except Exception as e:
        print(f"Llama3 Error: {e}")
        return f"Error: {e}"

def prompt_mistral(system_prompt, user_prompt):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {MISTRAL_API_KEY}'
        }
        payload = {
            "model": "mistral-large-latest", 
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.0
        }
        response = requests.post('https://api.mistral.ai/v1/chat/completions', headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Mistral Error: {e}")
        return f"Error: {e}"

def process_questions():
    file_path = 'definitions.xlsx'
    df = pd.read_excel(file_path)

    result_columns = [
        'GPT-4o One Shot Output', 'GPT-4o Zero Shot Output',
        'Mistral Zero-Shot Output', 'Mistral One-Shot Output',
        'Llama3 1-Shot Output', 'Llama3 0-Shot Output'
    ]
    for col in result_columns:
        if col not in df.columns:
            df[col] = ''

    system_prompt = (
        "You are an expert at evaluating financial data in XBRL. When you are given an XBRL term, give the exact definition of the term as it appears in your sources, with great detail when necessary."
        "You can include multiple sentences, but make sure your output is in one line. Provide only the EXACT ANSWER. Try not to repeat the given XBRL term in your answer, try not to use 'this refers to' or 'this represents', do not attempt to give the definition in your own words, do not say if you are unsure, etc."
    )

    one_shot_example_text = (
        "What is the definition of 'XBRL Specification' in XBRL?"
    )
    one_shot_example_answer = (
        "Descriptions and guidelines of XML semantics, syntax, and frameworks used for XBRL construction."
    )

    for index, row in df.iterrows():

        question = str(row['Question']).strip()
        if not question:
            continue

        zero_shot_user_prompt = f"{question}\nAnswer:"

        one_shot_user_prompt = (
            f"{one_shot_example_text}\nAnswer:\n{one_shot_example_answer}\n\n"
            f"{question}\nAnswer:"
        )

        time.sleep(1)

        print(f"\nProcessing question at row {index + 2}:")

        gpt4o_zero_shot_response = prompt_gpt4o(system_prompt, zero_shot_user_prompt)
        print(f"GPT-4o Zero-Shot Response:\n{gpt4o_zero_shot_response}\n")
        gpt4o_one_shot_response = prompt_gpt4o(system_prompt, one_shot_user_prompt)
        print(f"GPT-4o One-Shot Response:\n{gpt4o_one_shot_response}\n")

        mistral_zero_shot_response = prompt_mistral(system_prompt, zero_shot_user_prompt)
        print(f"Mistral Zero-Shot Response:\n{mistral_zero_shot_response}\n")
        mistral_one_shot_response = prompt_mistral(system_prompt, one_shot_user_prompt)
        print(f"Mistral One-Shot Response:\n{mistral_one_shot_response}\n")

        llama_zero_shot_response = prompt_llama(system_prompt, zero_shot_user_prompt)
        print(f"Llama3 0-Shot Response:\n{llama_zero_shot_response}\n")
        llama_one_shot_response = prompt_llama(system_prompt, one_shot_user_prompt)
        print(f"Llama3 1-Shot Response:\n{llama_one_shot_response}\n")

        df.at[index, 'GPT-4o Zero Shot Output'] = gpt4o_zero_shot_response
        df.at[index, 'GPT-4o One Shot Output'] = gpt4o_one_shot_response
        df.at[index, 'Mistral Zero-Shot Output'] = mistral_zero_shot_response
        df.at[index, 'Mistral One-Shot Output'] = mistral_one_shot_response
        df.at[index, 'Llama3 0-Shot Output'] = llama_zero_shot_response
        df.at[index, 'Llama3 1-Shot Output'] = llama_one_shot_response

    df.to_excel('definitions.xlsx', index=False)
    print("\nProcessing completed. Results saved to 'definitions.xlsx'.")

if __name__ == "__main__":
    create_questions('XBRL Terminology.xlsx', 'definitions.xlsx')
    process_questions()