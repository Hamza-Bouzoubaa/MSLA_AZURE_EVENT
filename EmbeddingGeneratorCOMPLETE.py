from langchain_openai import AzureOpenAIEmbeddings
from PyPDF2 import PdfReader
import json
import os 
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')



embeddings =  AzureOpenAIEmbeddings(openai_api_key = AZURE_OPENAI_API_KEY,azure_endpoint=AZURE_OPENAI_ENDPOINT,model="text-embedding-ada-002")  # Generating embeddings


def SplitDocumentInPages(Document):
    reader = PdfReader(Document)
    name = Document.split("\\")[-1]
    number_of_pages = len(reader.pages)

    Document =  {}

 

    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        Document[f"document_page_{i}"] = {'name': name, 'page_number': i+1, 'text': text}
        print(i,number_of_pages)

    DocumentVectors = embeddings.embed_documents([Document[page]['text'] for page in Document])

    k= 0
    for page in Document:
        Document[page]["embedding"] = DocumentVectors[k]
        k = k + 1

    return Document

def EmbedQuery(Query):
    return embeddings.embed_documents([Query])



#doc = SplitDocumentInPages("Documents\Merged.pdf")

#with open('data.json', 'w') as f:
#    json.dump(doc, f)









