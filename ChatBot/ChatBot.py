import streamlit as st
import os 
from dotenv import load_dotenv
import google.generativeai as genai 
import replicate

load_dotenv()
Googl_Api_key = os.getenv('Google_Api_key')
genai.configure(api_key=Googl_Api_key)
gemini_model = genai.GenerativeModel("gemini-pro")

st.set_page_config(page_title="💬 Resume Helper")
 
 

def generate_response(name, temperature, top_p, max_length ,prompt_input,messages):
    name = 'Gemini-pro'
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. do not start the sentance with assitant: '."
    for dict_message in messages:
        content = dict_message["content"]

        if content is not None:
            if dict_message["role"] == "user":
                string_dialogue += f"User: {content}\n\n"
            else:
                string_dialogue += f"Assistant: {content}\n\n"

    if name == 'Llama3-70B':
        try:
            llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
            llama_3='meta/meta-llama-3-70b-instruct'
            output = replicate.run(llama_3, 
                                input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                        "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
            result = list(output)
            final_output = "".join(result)
            return final_output
        except Exception as e:
            st.info("Error loading Llama2-13B model choose other model")
             
    
    elif name == 'Llama3-8B':
        try:
            llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
            llama_3='meta/meta-llama-3-8b-instruct'
            output = replicate.run(llama_3, 
                                input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                        "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
            result = list(output)
            final_output = "".join(result)
            return 'final_output'
        except Exception as e:
            st.info("Error loading Llama2-13B model choose other model")
             
    
    elif name == 'Gemini-pro':
        prompt = f"{string_dialogue} {prompt_input} Assistant: " + f'temperature={temperature}, {top_p}=top_p, max_length={max_length}, repetition_penalty=1'
        try:
            model = gemini_model
            response = model.generate_content(prompt).text
            return response
        except Exception as e:
            st.info("Error with Gemini-pro model choose other model")
                          
        
def main():
    with st.sidebar:
        st.title('💬Resume Helper ')
        uploaded_files = st.file_uploader("Upload your Resume", type=['pdf'],help="Please upload your resume in PDF format")
        submit_button = st.button("Submit")
        job_description=st.text_area("Enter the Job Description here") 
        st.subheader('Models and parameters')
        model_name = st.selectbox('Choose a model', ['Gemini-pro','Llama3-8B','Llama3-70B',])
        temperature = st.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
        top_p = st.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
        max_length = st.slider('max_length', min_value=32, max_value=128, value=120, step=8)
     
    
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = [{"role": "assistant", "content": 'Hello there! How can I help you today?'}]
        st.session_state.chat_history = []

    if 'messages' not in st.session_state:
        st.session_state.messages=[{"role": "assistant", "content": 'Hello there! How can I help you today?'}]
        st.session_state.chat_history = []
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])    

    if prompt := st.chat_input('How can I help you today? '):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant") :
            with st.spinner("Thinking..."):
                try:                   
                    response = generate_response(model_name, temperature, top_p, max_length,prompt_input=prompt,messages=st.session_state.messages)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.markdown(response)
                except Exception as e:
                    st.info("There was a problem generating content. Please try again in 2 minutes or change The Model.")
                    




 

 
main() 