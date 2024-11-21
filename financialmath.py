import pandas as pd
import openai
import json
import time
from mistralai import Mistral

df = pd.read_excel('XBRL financial_math.xlsx')

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

openai.api_key = config['openai_api_key']
MISTRAL_API_KEY = config['mistral_api_key']
OLLAMA_API_URL = 'http://localhost:11434/api/generate'

client = Mistral(api_key=MISTRAL_API_KEY)

def create_questions():

    def create_question_dict(row):
        question_dict = {}
        for i in range(1, 21):
            question = row[f'Question {i}']
            if pd.notna(question):
                question_dict[f'Question {i}'] = [question]
        
        formula_sentence = f"Given the formula name: {row['Formula Name']}, formula: {row['Formula']}, and formula explanation: {row['Explanation']}, answer the questions: "
        return formula_sentence + str(question_dict)

    df['Question'] = df.apply(create_question_dict, axis=1)

    df_questions = df[['Question']] 
    df_questions.to_excel('financialmath.xlsx', index=False)  

    print("Successfully created the new Excel file with the structured Questions column.")

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

def process_questions():
    file_path = 'financialmath.xlsx' 
    df = pd.read_excel(file_path)

    result_columns = [
        'GPT-4o Zero Shot Output'
    ]
    for col in result_columns:
        if col not in df.columns:
            df[col] = ''

    system_prompt = (
        "You are an expert at evaluating financial data in XBRL. When you are given an XBRL formula, formula name, formula explanation, and a series of 20 questions based on the formula, answer each question by applying the given formula directly to the data in the question. All answers should be stored in an array."
        "Convert percentages values in each question to decimal values. OMIT percentage signs '%' from your answers. Leave your answer as the immediate result obtained from using the given formula. DO NOT CONVERT FROM DECIMALS TO PERCENTAGES if it is not explicitly in the formula. Round decimals to the nearest hundredth. Omit trailing zeros after the decimal point"
        "Make sure your output is in one line. Start and end the array of answers with square brackets, and put each answer in double quotes. Provide only the calculations, do not explain the calculations, do not say if you are unsure, etc."
    )

    for index, row in df.iterrows():

        question = str(row['Question']).strip()
        if not question:
            continue

        

        zero_shot_user_prompt = f"{question}\nAnswer:"

        time.sleep(1)

        print(f"\nProcessing question at row {index + 2}:")

        gpt4o_zero_shot_response = prompt_gpt4o(system_prompt, zero_shot_user_prompt)
        print(f"GPT-4o Zero-Shot Response:\n{gpt4o_zero_shot_response}\n")

        df.at[index, 'GPT-4o Zero Shot Output'] = gpt4o_zero_shot_response

    df.to_excel('financialmath.xlsx', index=False)
    print("\nProcessing completed. Results saved to 'financialmath.xlsx'.")

if __name__ == "__main__":
    create_questions()
    process_questions()