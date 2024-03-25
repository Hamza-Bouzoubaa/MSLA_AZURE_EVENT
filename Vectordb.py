from azure.cosmos import CosmosClient,exceptions,PartitionKey
from EmbeddingGenerator import SplitDocumentInPages,EmbedQuery
from sklearn.metrics.pairwise import cosine_similarity 
import numpy as np
import random

import os 
from dotenv import load_dotenv

load_dotenv()
cosmosdb_endpoint = os.getenv('COSMOSDB_ENDPOINT')
cosmosdb_key = os.getenv('COSMOSDB_KEY')


client = CosmosClient(cosmosdb_endpoint, cosmosdb_key)


def CreateDB(DatabaseName="AITutor", ContainerName ="Documents",Partition_Key = "/Group_id" ,offer_throughput=1000):
    '''Create a database and container in Azure Cosmos DB'''

    






    return container

def InsertPage(container,Document_name,Page_number,Text,Embedding):
    '''Insert a page into the container in Azure Cosmos DB'''
    



    
    

def InsertDocument(container,Document):
    '''Insert a document (multiple pages) into the container in Azure Cosmos DB'''
    




    

def QueryDocuments(container,GroupID=1):
    '''Query all documents in the container in Azure Cosmos DB'''

   




def VectorSimilaritySearch(Query,Vectors,Top_n=3):
    '''Search for the most similar vectors to the query vector in the list of vectors'''

    




def SearchContainer(container,Query,Top_n=3):
    '''Search the container for the most similar pages to the query'''


    




