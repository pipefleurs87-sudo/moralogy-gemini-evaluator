import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moralogy Gemini 3", page_icon="⚖️")
st.title("⚖️ Moralogy Gemini 3 Evaluator")

# Configuración simplificada y directa
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    user_input = st.text_area("Describe el dilema ético:", 
                              placeholder="Escribe aquí el dilema del tranvía...",
                              height=150)

    if st.button("Evaluar con Gemini"):
        if user_input:
            with st.spinner("Conectando con el motor de Gemini 3..."):
                try:
                    # Probamos con el nombre de modelo más compatible de la API
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_input)
                    
                    st.subheader("Análisis de Inteligencia v3:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error de red o modelo: {e}")
                    st.info("Nota: Si el error persiste, verifica que tu API Key sea de un proyecto con Gemini habilitado.")
        else:
            st.warning("Por favor, introduce un dilema para analizar.")
else:
    st.error("⚠️ Falta la API Key en los Secrets de Streamlit.")
