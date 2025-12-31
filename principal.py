import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moralogy Gemini 3", page_icon="⚖️")
st.title("⚖️ Moralogy Gemini 3 Evaluator")

# Configuración de la API usando tus Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    user_input = st.text_area("Describe el dilema para Gemini 3:", 
                              placeholder="Escribe el dilema del tranvía aquí...",
                              height=150)

    if st.button("Evaluar con Gemini 3"):
        if user_input:
            with st.spinner("Conectando con Gemini 1.5 Pro (Motor v3)..."):
                try:
                    # Aplicamos la recomendación de la captura: 'gemini-1.5-pro'
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    response = model.generate_content(user_input)
                    
                    st.subheader("Análisis de Inteligencia Superior:")
                    st.markdown(response.text)
                except Exception as e:
                    # Si falla el Pro por cuota (429), usamos Flash como respaldo
                    if "429" in str(e):
                        st.warning("Cuota Pro agotada. Intentando con Gemini 1.5 Flash...")
                        model_flash = genai.GenerativeModel('gemini-1.5-flash')
                        response = model_flash.generate_content(user_input)
                        st.markdown(response.text)
                    else:
                        st.error(f"Error técnico: {e}")
        else:
            st.warning("Introduce un dilema antes de evaluar.")
else:
    st.error("Configura la API Key en los Secrets.")
