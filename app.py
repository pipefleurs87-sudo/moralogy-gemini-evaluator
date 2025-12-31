import streamlit as st
import google.generativeai as genai

import streamlit as st
import google.generativeai as genai

genai.configure("AIzaSyBuAhdmzDu_g7PnyrxB0QY1WYjoz75vaDQ")

model = genai.GenerativeModel("gemini-pro")

response = model.generate_content("Hola mundo")

st.write(response.text)



