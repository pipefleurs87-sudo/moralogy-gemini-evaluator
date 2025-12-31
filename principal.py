import streamlit as st
from google import genai

st.set_page_config(page_title="Moralogy Gemini 3", page_icon="⚖️")
st.title("⚖️ Moralogy Gemini 3 Evaluator")

if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        user_input = st.text_area("Describe el dilema ético:", height=150)

        if st.button("Evaluar con Gemini"):
            if user_input:
                with st.spinner("Conectando con el motor de Gemini..."):
                    # Intentamos con el modelo que Google reconoce como v3 en la API estable
                    try:
                        response = client.models.generate_content(
                            model="gemini-1.5-flash", # Este es el nombre técnico actual para el motor Flash
                            contents=user_input
                        )
                        st.subheader("Análisis Ético:")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Error de red o cuota: {e}")
            else:
                st.warning("Escribe el dilema antes de evaluar.")
    except Exception as e:
        st.error(f"Error de configuración: {e}")
else:
    st.error("⚠️ Falta la API Key en los Secrets.")
