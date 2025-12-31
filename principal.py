import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moralogy Gemini 3", page_icon="⚖️")
st.title("⚖️ Moralogy Gemini 3 Evaluator")

# VERIFICACIÓN DE API KEY
if "GOOGLE_API_KEY" in st.secrets:
    # Configuramos la API Key
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    user_input = st.text_area("Describe el dilema para Gemini 3:", 
                              placeholder="Analiza el dilema del tranvía...",
                              height=150)

    if st.button("Evaluar con Gemini"):
        if user_input:
            with st.spinner("Analizando con el motor de Gemini 3..."):
                try:
                    # USAMOS EL MODELO ESTABLE SIN PREFIJOS
                    # Esto evita que la librería busque en 'v1beta'
                    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                    
                    response = model.generate_content(user_input)
                    
                    st.subheader("Análisis de Inteligencia v3:")
                    st.markdown(response.text)
                except Exception as e:
                    # Si hay error, mostramos el mensaje técnico para depurar
                    st.error(f"Error técnico: {e}")
        else:
            st.warning("Por favor, introduce un dilema.")
else:
    st.error("⚠️ No se encontró la API Key en los Secrets de Streamlit.")
