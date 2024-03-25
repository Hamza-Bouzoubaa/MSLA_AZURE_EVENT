from Vectordb import CreateDB, InsertDocument,SearchContainer
from GPTanswer import generate_response

container = CreateDB()
#InsertDocument(container,"Documents\Merged.pdf")


while True:
    print("Welcome to the AI Tutor, please enter your question or type 'exit' to quit")
    question = input("Question: ")
    if question == "exit":
        break   
    sources = SearchContainer(container,question)
   
    response = generate_response(question,sources)
    print(response)
