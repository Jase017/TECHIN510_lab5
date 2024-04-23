import os

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

prompt_templete = """

The user's request is:
{prompt}
"""


def generate_content(prompt):
    response = model.generate_content(prompt)
    return response.text

st.title("Let's play with Gemini AI")
prompt = st.text_area("Enter your next travel request (days, destination, activities, etc.):")
if st.button("Give me a plan!"):
    reply = generate_content(prompt)
    st.write(reply)