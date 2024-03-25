# Microsoft Student Learn Ambassador Event - Customizable Chat Bots  
   
This repository contains the codebase for a customizable chat bot that uses augmented generation technology to empower Open AI or any other large language model with our data PDFs.  
   
## Pre-requisites  
Before starting, please ensure you have the following installed and set up:  
1. Python  
2. Azure account  
   
If you are a student at the University of Ottawa, you can get $100 free through Azure Students Deals [here](https://azure.microsoft.com/en-ca/free/students).  
   
## Installation  
After setting up Python and Azure, you can start by cloning this repository. The repository contains both complete code and also files with incomplete code that we'll complete during the event.  
   
To clone the repository and install the requirements, open a command line interface on VS Code or any other terminal and run the following commands:  
```  
git clone https://github.com/Hamza-Bouzoubaa/MSLA_AZURE_EVENT.git
pip install -r requirement.txt  
```  
   
## Azure Setup  
After setting up your local environment, you need to set up your Azure account.  
   
1. **OpenAI:** In Azure, create an OpenAI instance and create a GPT-3.5 model and a text embedding `ada-002` embedding model. Obtain the keys and URL endpoints.  
   
2. **CosmoDB:** Create a CosmoDB noSQL instance on your Azure account and get the primary key,  and the connection string.   
  <img width="893" alt="azure" src="https://github.com/Hamza-Bouzoubaa/MSLA_AZURE_EVENT/assets/104928656/b77d9734-3e94-4770-a267-5984581aae0e">
  <img width="941" alt="azure" src="https://github.com/Hamza-Bouzoubaa/MSLA_AZURE_EVENT/assets/104928656/90148391-c62b-4478-ae49-d3cebb7e3f0a">

## Codebase Walkthrough  
Once you have the OpenAI keys and CosmoDB keys, you can start working on the code files.   
  
### Embedding Generator  
First, we need to complete the `EmbeddingGenerator.py` code.  
   
1. **SplitDocumentInPages:** This function splits a document into pages, extracts the text and the page number and creates a dictionary with the parameters: text, page, and text embedding.
```  
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

```  
  
2. **EmbedQuery:** This function takes a query as input and outputs an embedding of the query.
```
def EmbedQuery(Query):
    return embeddings.embed_documents([Query])
```
   
### Vector DB  
Next, we move on to `Vectordb.py`.  
   
1. **CreateDB:** This function creates the database and the container inside of CosmoDB using the provided keys.
```
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
```
   
2. **InsertPage, InsertDocument:** These functions are used to insert pages and documents into the CosmoDB container.
```
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
```
```
def InsertDocument(container,Document):
    Document = SplitDocumentInPages(Document)
    try:
        for page in Document:
            InsertPage(container,Document[page]["name"],Document[page]["page_number"],Document[page]["text"],Document[page]["embedding"])

        return True
    except Exception as e:
        print(e)
        return False
```
    
3. **QueryDocuments:** This function queries all documents inside of a container.
```

def QueryDocuments(container,GroupID=1):
    query ="SELECT * FROM my_container"
    query_iterable = container.query_items(
        query=query,
        partition_key=(GroupID) # use user_id as partition key
    )
    results = list(query_iterable)

    return results
```

4. **VectorSimilaritySearch:** This function takes a query as an embedding and the vectors of the documents as another parameter and returns the best matching vectors and pages.
```
def VectorSimilaritySearch(Query,Vectors,Top_n=3):

    similarity_scores = cosine_similarity(Query, Vectors)
    most_similar_indices = np.argsort(similarity_scores)[0][-Top_n:]
    return most_similar_indices
```
     
5. **SearchContainer:** This function searches a container using a query which has been embedded. It calls the function, `VectorSimilaritySearch`.
```
def SearchContainer(container,Query,Top_n=3):


    Query = EmbedQuery(Query)
    
    results = QueryDocuments(container)
    Vectors = [result['Embedding'] for result in results]
    most_similar_indices = VectorSimilaritySearch(Query,Vectors,Top_n)
    TextRes  = [f"{result['Page_Text']} Sourced from : page {result['Document_name']} page {result['Page_number']}|)" for result in results]

    return [TextRes[i] for i in most_similar_indices]
```

   
   

   
### GPT Answer  
Lastly, complete the `GPTanswer.py`.  
   
1. **generate_response:** This function generates an answer given a question and a source. We ask GPT to give us an answer to this question using this source.
```
   def generate_response(Question,Sources,ChatHistory):

    LLM = AzureChatOpenAI(
    openai_api_version="2023-05-15",
    azure_deployment="AiTutor",
    )

    Prompt = PromptTemplate(  
    input_variables=["Question","Sources","ChatHistory"],  
    template=system_prompt  
    ) 
    
    Chain = LLMChain(llm=LLM, prompt=Prompt)
    response = Chain.run(Question = Question,Sources=Sources,ChatHistory=ChatHistory)
    return response
```

   
## Run the Application  
After completing all the functions in the three files, you can run the `frontend.py` file. This combines all the functions into a functional frontend.  
```python -m streamlit run FrontEnd.py```
   
## Conclusion  
Follow all the steps mentioned above and you will have a working customizable chat bot powered by OpenAI and Azure. Happy coding!
