import streamlit as st
import google.generativeai as genai
import os

# 1. Configuración de la página
st.set_page_config(page_title="Moralogy Gemini Evaluator", layout="centered")

# 2. Configuración de la API Key
# En Streamlit Cloud, añade GOOGLE_API_KEY en Settings > Secrets
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Por favor, configura la GOOGLE_API_KEY en los secretos de Streamlit.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Interfaz de usuario
st.title("🧠 Moralogy Gemini Evaluator")
st.subheader("Evaluador ético y moral potenciado por IA")

user_input = st.text_area("Introduce el dilema o texto a evaluar:", placeholder="Escribe aquí...")

if st.button("Evaluar con Gemini"):
    if user_input:
        with st.spinner("Analizando..."):
            try:
                # Llamada a la API
                response = model.generate_content(user_input)
                
                st.markdown("### Resultado de la Evaluación:")
                # Usamos markdown para una mejor lectura
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Hubo un error: {e}")
    else:
        st.warning("Por favor, introduce algún texto para analizar.")
