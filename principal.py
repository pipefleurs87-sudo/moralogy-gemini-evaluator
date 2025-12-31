import streamlit as st
import google.generativeai as genai

st.title("Test de Moralogy")

# El código que fallaba, pero bien escrito:
try:
    st.write("Esperando respuesta...")
except Exception as e:
    st.error(f"Error: {e}")

st.info("Si ves esto, el error de sintaxis desapareció.")
