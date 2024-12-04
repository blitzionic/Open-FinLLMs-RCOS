import pandas as pd


input_file = 'abbreviation_task_acronym.xlsx' 
output_file = 'XBRLTEST.xlsx' 


df = pd.read_excel(input_file)


def keep_first_line(text):
    if isinstance(text, str): 

        return text.split('\n')[0]
    return text 


df['Generated Answer'] = df['Generated Answer'].apply(keep_first_line)


df.to_excel(output_file, index=False)

print(f"Processed file saved as: {output_file}")
