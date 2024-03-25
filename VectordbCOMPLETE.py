from azure.cosmos import CosmosClient,exceptions,PartitionKey
import random
from EmbeddingGenerator import SplitDocumentInPages,EmbedQuery
from sklearn.metrics.pairwise import cosine_similarity 
import numpy as np


import os 
from dotenv import load_dotenv

load_dotenv()
cosmosdb_endpoint = os.getenv('COSMOSDB_ENDPOINT')
cosmosdb_key = os.getenv('COSMOSDB_KEY')


client = CosmosClient(cosmosdb_endpoint, cosmosdb_key)


def CreateDB(DatabaseName="AITutor", ContainerName ="Documents",Partition_Key = "/Group_id" ,offer_throughput=1000):

    # Create a database in Azure Cosmos DB.
    try:
        database = client.create_database_if_not_exists(id=DatabaseName)
        print(f"Database created: {database.id}")

    except exceptions.CosmosResourceExistsError:
        print("Database already exists.")

    # Create a container in Azure Cosmos DB.  
    try:  
        partition_key_path = PartitionKey(path=Partition_Key)  

        container = database.create_container_if_not_exists(  
            id=ContainerName,  
            partition_key=partition_key_path,
            offer_throughput= offer_throughput,  
        )  
        print(f"Container created: {container.id}")  
    except exceptions.CosmosResourceExistsError:  
        print("Container already exists.")  

    return container

def InsertPage(container,Document_name,Page_number,Text,Embedding):
    random_id = random.randint(1,1000000)
    print(f"Inserting page {Page_number} from {Document_name} into the container")

    item_body = {
        'id' : str(random_id),
        'Group_id': 1,
        'Document_name': Document_name,
        'Page_number': Page_number,
        'Page_Text': Text,
        'Embedding': Embedding
    }
    
    container.upsert_item(body=item_body)

def InsertDocument(container,Document):
    Document = SplitDocumentInPages(Document)
    try:
        for page in Document:
            InsertPage(container,Document[page]["name"],Document[page]["page_number"],Document[page]["text"],Document[page]["embedding"])

        return True
    except Exception as e:
        print(e)
        return False
    

def QueryDocuments(container,GroupID=1):
    query ="SELECT * FROM my_container"
    query_iterable = container.query_items(
        query=query,
        partition_key=(GroupID) # use user_id as partition key
    )
    results = list(query_iterable)

    return results

def VectorSimilaritySearch(Query,Vectors,Top_n=3):

    similarity_scores = cosine_similarity(Query, Vectors)
    most_similar_indices = np.argsort(similarity_scores)[0][-Top_n:]
    return most_similar_indices


def SearchContainer(container,Query,Top_n=3):


    Query = EmbedQuery(Query)
    
    results = QueryDocuments(container)
    Vectors = [result['Embedding'] for result in results]
    most_similar_indices = VectorSimilaritySearch(Query,Vectors,Top_n)
    TextRes  = [f"{result['Page_Text']} Sourced from : page {result['Document_name']} page {result['Page_number']}|)" for result in results]

    return [TextRes[i] for i in most_similar_indices]




