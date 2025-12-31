import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moralogy Gemini Evaluator", page_icon="🧠")

st.title("🧠 Moralogy Gemini Evaluator")

# Configuración de API Key desde Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    user_input = st.text_area("Introduce el dilema ético o situación a evaluar:", height=200)

    if st.button("Evaluar con Gemini"):
        if user_input:
            with st.spinner("Gemini está analizando la moralidad del texto..."):
                try:
                    response = model.generate_content(user_input)
                    st.markdown("### Análisis Ético:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error al conectar con la API: {e}")
        else:
            st.warning("Escribe algo para poder evaluarlo.")
else:
    st.error("⚠️ Falta la API Key. Ve a Settings > Secrets en Streamlit Cloud y añade: GOOGLE_API_KEY = 'tu_clave'")
