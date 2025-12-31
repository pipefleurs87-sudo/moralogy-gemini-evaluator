import streamlit as st
from google import genai

st.set_page_config(page_title="Moralogy Gemini 3", page_icon="⚖️")
st.title("⚖️ Moralogy Gemini 3 Evaluator")

if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        user_input = st.text_area("Describe el dilema para Gemini 3:", height=150)

        if st.button("Evaluar con Gemini 3"):
            if user_input:
                with st.spinner("Gemini 3 Flash analizando (Alta velocidad)..."):
                    try:
                        # CAMBIO CLAVE: Usamos gemini-3-flash para evitar el error 429
                        response = client.models.generate_content(
                            model="gemini-3-flash", 
                            contents=user_input
                        )
                        st.subheader("Análisis de Inteligencia v3:")
                        st.markdown(response.text)
                    except Exception as e:
                        if "429" in str(e):
                            st.error("⚠️ Cuota agotada incluso en Flash. Por favor, espera 30 segundos y reintenta.")
                        else:
                            st.error(f"Error técnico: {e}")
            else:
                st.warning("Escribe el dilema antes de evaluar.")
    except Exception as e:
        st.error(f"Error al conectar con el cliente: {e}")
else:
    st.error("⚠️ Configura la API Key en los Secrets.")
