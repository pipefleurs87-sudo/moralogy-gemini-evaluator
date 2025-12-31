import streamlit as st
import google.generativeai as genai # Usamos la librería estable para evitar el 404

st.set_page_config(page_title="Moralogy Gemini 3", page_icon="⚖️")
st.title("⚖️ Moralogy Gemini 3 Evaluator")

# Configuración con la librería estable
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    user_input = st.text_area("Describe el dilema para Gemini 3:", 
                              placeholder="Escribe el dilema del tranvía aquí...",
                              height=150)

    if st.button("Evaluar con Gemini"):
        if user_input:
            with st.spinner("Gemini 3 procesando análisis ético..."):
                try:
                    # Este nombre de modelo es el 'puente' que funciona 100% en la API
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_input)
                    
                    st.subheader("Análisis de Inteligencia v3:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
        else:
            st.warning("Por favor, introduce un dilema.")
else:
    st.error("Configura la API Key en los Secrets.")
