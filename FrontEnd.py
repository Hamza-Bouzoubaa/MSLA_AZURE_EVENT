import streamlit as st  
from GPTanswer import generate_response  
import os   
from Vectordb import CreateDB,InsertDocument,SearchContainer
from dotenv import load_dotenv
from collections import deque  

load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')



container = CreateDB()
print("Container created")

# Initialize chat history  
if "chat_history" not in st.session_state:  
    st.session_state.chat_history = []  

def save_uploaded_file(directory: str, file):    
    """Save uploaded file to the specified directory and return the path."""    
    if not os.path.exists(directory):    
        os.makedirs(directory)    
    
    filepath = os.path.join(directory, file.name)    
    with open(filepath, 'wb') as f:    
        f.write(file.getbuffer())    
    
    return filepath  
  


def main():   
                 
    st.sidebar.title("Upload your PDF")        
    file = st.sidebar.file_uploader("Drop your file here", type=['pdf'])      

    if file is not None and st.sidebar.button('Submit File'):    
        file_path = save_uploaded_file("Documents", file)
        InsertDocument(container,file_path)  
        print("here")
                        
        st.sidebar.success('File uploaded and processed successfully.')      
    st.header('Ask your document')        
    user_query = st.chat_input('Type your question here...')      
            
    if user_query:        
            

        st.session_state.chat_history.append({"role": "user", "content": user_query})  

        result = SearchContainer(container,user_query,3)
        print(result)
        answer = generate_response(user_query,result,ChatHistory=st.session_state.chat_history)  
        print(st.session_state.chat_history)
         # Add AI response to chat history  
        st.session_state.chat_history.append({"role": "assistant", "content": answer})    

         # Display chat history  
        for chat in st.session_state.chat_history:  
            with st.chat_message(chat['role']):  
                st.write(chat['content'])       
        
if __name__ == "__main__":        
    main()    
