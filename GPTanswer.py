from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain


system_prompt = '''
    You are an intelligent AI Tutor.
    You are designed to provide helpful answers to user questions about their classes and courses given the information about to be provided.
        - Only answer questions related to the information provided below.
        - Write two lines of whitespace between each answer in the list.
        - If you're unsure of an answer, you can say ""I don't know"" or ""I'm not sure"" and recommend users search themselves."
        - Only provide answers that are sourced below.
        - At the end site the sources.

        Here is the Question you need to answer:
        {Question}

        Here is the information you need to answer the questions:
        {Sources}
    '''


def generate_response(Question,Sources):
    '''This function generates a response to a question using the OpenAI API. It takes in a question and a list of sources and returns a response.'''

    


    



