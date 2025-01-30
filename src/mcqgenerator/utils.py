import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.mcqgenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

# Load a file
with open('/config/workspace/Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

# Create a title for the app
st.title('MCQ Creator Application with Langchain')

# Create a form using st.form
with st.form("user_inputs"):
    # File upload
    uploaded_file = st.file_uploader("Upload a PDF or TXT file")

    # Input Fields
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)

    # Subject
    subject = st.text_input("Insert Subject", max_chars=20)

    # Quiz Tone
    tone = st.text_input("Complexity level of Question", max_chars=20, placeholder='Simple')

    # Add Button
    button = st.form_submit_button("Create MCQs")

    # Check if the button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading........"):
            try:
                text = read_file(uploaded_file)
                # Count tokens
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain({
                        'text': text,
                        'number': mcq_count,
                        'subject': subject,
                        'tone': tone,
                        'response_json': json.dumps(RESPONSE_JSON)
                    })

                # Display the response
                if isinstance(response, dict):
                    # Extract the quiz data from response
                    quiz = response.get('quiz')
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            # Display the revision in a text box as well
                            st.text_area(label='Review', value=response.get('review', ''))
                        else:
                            st.error("Error in the table data")
                    else:
                        st.write(response)
            except Exception as e:
                traceback.print_exception(type(e), e, e, e.__traceback__)
                st.error("Error")
            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: {cb.total_cost}")

def read_file(file):
    try:
        if file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        elif file.name.endswith(".txt"):
            return file.read().decode('utf-8')
        else:
            raise Exception("Unsupported file format only PDF and TXT files are supported")
    except Exception as e:
        raise Exception("Error reading the PDF file") from e
