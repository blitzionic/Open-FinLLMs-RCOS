import pandas as pd
from bert_score import score
from tqdm import tqdm

def calculate_bertscore_f1(referenceText, candidateModel, model_type='bert-base-uncased', lang='en'):
    """
    Function calculates BERTscore F1 for the reference and candidate text

    Parameters:
        referenceText (str): The absolute truth.
        candidate (str): The evaluation text.
        model_type (str): The model of BERT to use.
        lang (str): The language.

    Returns:
        float or None: BERTScore F1 score, or None if inputs are invalid.
    """
    
    if not referenceText or not candidateModel:
        return None

    try:
        P, R, F1 = score([candidateModel], [referenceText], model_type=model_type, lang=lang, verbose=False)
        return F1[0].item()
    except Exception as e:
        print(f"ERROR: could not compute BERTscore for reference: '{referenceText}' and candidate: '{candidateModel}'. Error: {e}")
        return None

def process_bertscore(file_path, output_file):
    """
    Function processes the TSV file to compute BERTScore F1 for each model's Definition output.

    Args:
        file_path (str): Path to the input TSV file.
        output_file (str): Path to save the output TSV file with BERTScore results.
    """
    try:
        df = pd.read_csv(file_path, sep='\t', on_bad_lines='skip', dtype=str)
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    print(f"Total rows (including header): {len(df)}")
    print(f"Columns: {df.columns.tolist()}")

    reference_col = 'answer'

    definition_to_score_column = {
        'GPT-4o Zero Shot Answer': 'GPT-4o Zero Shot',
        'GPT-4o One Shot Answer': 'GPT-4o One Shot',
        'Mistral Zero-Shot Answer': 'Mistral Zero-Shot',
        'Mistral One-Shot Answer': 'Mistral One-Shot',
        'Llama3 0-Shot Answer': 'Llama3 0-Shot',
        'Llama3 1-Shot Answer': 'Llama3 1-Shot'
    }

    missing_def_cols = [def_col for def_col in definition_to_score_column.keys() if def_col not in df.columns]
    missing_score_cols = [score_col for score_col in definition_to_score_column.values() if score_col not in df.columns]

    if missing_def_cols:
        print(f"Missing Definition columns in the dataset: {missing_def_cols}")
    if missing_score_cols:
        print(f"Missing BERTScore F1 target columns in the dataset: {missing_score_cols}")

    if missing_def_cols or missing_score_cols:
        print("Please ensure all necessary columns are present in the dataset.")
        return
    else:
        print("All required Definition and BERTScore F1 target columns are present.")

    df.fillna('', inplace=True)

    print("\nStarting BERTScore F1 computation...")
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        reference = str(row[reference_col]).strip()
        if not reference:
            continue

        for def_col, score_col in definition_to_score_column.items():
            candidate = str(row[def_col]).strip()
            if not candidate:
                df.at[index, score_col] = None
                continue

            F1 = calculate_bertscore_f1(reference, candidate)

            df.at[index, score_col] = F1

    print("\nBERTScore F1 computation completed.")

    print("\nCalculating average BERTScore F1 for each model...")
    average_scores = {}
    for def_col, score_col in definition_to_score_column.items():
        df[score_col] = pd.to_numeric(df[score_col], errors='coerce')

        avg_f1 = df[score_col].mean()
        average_scores[score_col] = avg_f1

    avg_row = {col: '' for col in df.columns} 
    if 'term' in df.columns:
        avg_row['term'] = 'Average'
    elif 'answer' in df.columns:
        avg_row['answer'] = 'Average'

    for score_col, avg_f1 in average_scores.items():
        avg_row[score_col] = avg_f1

    avg_row_df = pd.DataFrame([avg_row])

    df = pd.concat([df, avg_row_df], ignore_index=True)
    try:
        df.to_csv(output_file, sep='\t', index=False)
        print(f"\nResults saved successfully to '{output_file}'.")
    except Exception as e:
        print(f"Error saving the file: {e}")

if __name__ == "__main__":
    input_file = 'Task-4 Long-form QA Dataset - Securities and Exchanges.tsv'
    output_file = 'Task-4 Long-form QA Dataset - Securities and Exchanges.tsv'

    process_bertscore(input_file, output_file)
