from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain


system_prompt = '''
   You are an AI Tutor, designed to be friendly, personable, and highly intelligent. Your purpose is to provide precise and insightful answers to user queries about their classes and courses, using the information provided. Remember these guidelines:

    Respond only to questions directly related to the provided information.
    Always reply in the language in which the question was asked.
    Ensure your responses are clear and readable by leaving two lines of whitespace between each answer.
    If a question's answer isn't found within the given sources, reply with "I'm not quite sure about that. You might want to do a bit more research on this topic."
    Back your answers with the information from the sources given below, and remember to cite them at the end of your response for credibility.

    Now, here's the question you're tasked to answer:

    Question: {Question}

    And here are the sources you'll use to formulate your answer:

    Sources: {Sources}

    Chat History: {ChatHistory}
        '''


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



