import streamlit as st
import os, openai
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

st.title('🦜🔗 Langchain + ChatGPT App')

openai_api_key = st.sidebar.text_input('Azure OpenAI API Key', type='password')
openai.api_key = openai_api_key
openai_api_base = st.sidebar.text_input('Azure OpenAI Resource Endpoint', 'https://<aoai-service-name>.openai.azure.com/')
openai.api_base = openai_api_base 
openai.api_version = "2023-05-15"
openai.api_type = "azure"

deployment_name = st.sidebar.text_input('ChatGPT Deployment Name', 'gpt-35-turbo')

def generate_response(input_text):
    llm = AzureChatOpenAI(temperature=0.0,
        openai_api_base=openai.api_base,
        openai_api_version=openai.api_version,
        deployment_name=deployment_name,
        openai_api_key=openai.api_key,
        openai_api_type = openai.api_type,
    )
    
    memory = ConversationBufferMemory()
    conversation = ConversationChain(
        llm=llm, 
        memory = memory,
        verbose=True
    )
    st.info(conversation.predict(input=input_text)) 
  
  

with st.form('my_form'):
    text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
    submitted = st.form_submit_button('Submit')
    if len(openai_api_key) == 0:
        st.warning('Please enter your Azure OpenAI API Key!', icon='⚠')
    if not openai_api_base.endswith('openai.azure.com/'):
        st.warning('Please enter your Azure OpenAI Resource Endpoint!', icon='⚠')
    if submitted and openai_api_base.endswith('openai.azure.com/') and len(openai_api_key) != 0:
        try:
            generate_response(text)
        except Exception as e:
            st.error('Error: {}'.format(e))
  