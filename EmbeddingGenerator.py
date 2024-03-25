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
    '''Split a document into pages and embed the text on each page. Return a dictionary with the page number, text, and embedding for each page.'''

    




    Document =  {}

 



    
    return Document

def EmbedQuery(Query):
    '''Embed a query using the OpenAI text-embedding-ada-002 model'''









