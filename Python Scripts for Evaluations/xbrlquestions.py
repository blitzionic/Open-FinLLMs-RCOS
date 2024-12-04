import pandas as pd

source_file = 'XBRLtest.xlsx'
destination_file = 'Task-3 XBRL Dataset.xlsx'

df = pd.read_excel(source_file)

column1 = 'Element:Text'
column2 = 'Attribute:id'

doc_path = 'amzn-20231231_lab.xml'
doc_type = '10K'
doc_period = str(2023)
source_link = 'https://www.sec.gov/ix?doc=/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm'
company = 'Amazon.com Inc.'
company_sector_gics = 'Consumer Discretionary'
document_information = f"{doc_path}, {doc_type}, {doc_period}, {source_link}, {company}, {company_sector_gics}"

question_list = []
for index, row in df.iterrows():
    element_text = str(row[column1]).strip()
    attribute_id = str(row[column2]).strip()

    attribute_id = attribute_id[4:attribute_id.find('_', 4)]
    attribute_id = attribute_id.replace("-", " ")
    attribute_id = attribute_id.upper()

    tag_question = f"What is the {attribute_id} XBRL tag for the label '{element_text}' as reported by {company} for the fiscal year {doc_period}?"

    question_list.append(tag_question)

df['Question'] = question_list

df = df[['Question']]

df.to_excel(destination_file, index=False)

print(f"Combined columns have been copied to '{destination_file}'.")


