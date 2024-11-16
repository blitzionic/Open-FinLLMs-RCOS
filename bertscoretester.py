from bert_score import score

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
        P, R, F1 = score([candidate], [reference], model_type=model_type, lang=lang, verbose=False)
        return F1[0].item()
    except Exception as e:
        print(f"ERROR: could not compute BERTscore for reference: '{reference}' and candidate: '{candidate}'. Error: {e}")
        return None

