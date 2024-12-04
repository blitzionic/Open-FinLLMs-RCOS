import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse('amazonXBRL/amzn-20231231_htm.xml') 
root = tree.getroot()

namespace_map = {
    'http://fasb.org/us-gaap/2023': 'us-gaap', 
    'http://www.amazon.com/20231231': 'amzn',
    'http://xbrl.sec.gov/dei/2023': 'dei'
}

doc_path = 'amzn-20231231_lab.xml'
doc_type = '10K'
doc_period = str(2023)
source_link = 'https://www.sec.gov/ix?doc=/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm'
company = 'Amazon.com Inc.'
company_sector_gics = 'Consumer Discretionary'
document_information = f"{doc_path}, {doc_type}, {doc_period}, {source_link}, {company}, {company_sector_gics}"

data = []

for elem in root.iter():
    if elem.attrib.get('unitRef') == 'usd':

        if '}' in elem.tag:
            namespace, local_tag = elem.tag.split('}', 1)
            
            namespace = namespace.lstrip('{')

            prefix = namespace_map.get(namespace, 'unknown')
            
            if prefix != 'unknown':
                tag_name = f"{prefix}:{local_tag}"
            else:
                tag_name = local_tag  
        else:
            tag_name = elem.tag 

        id = elem.attrib.get('id')

        value = elem.text.strip() if elem.text else ''

        fact_question = f"What is the fact at the tag '{tag_name}' and context ref '{id}' as reported by {company} for the fiscal year {doc_period}?"
        fact_answer = value

        data.append((fact_question, fact_answer))


df = pd.DataFrame(data, columns=["Question", "Answer"])



print(df)
