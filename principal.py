import streamlit as st
from google import genai # El nuevo import de Gemini 3

st.set_page_config(page_title="Moralogy Evaluator v3", page_icon="⚖️")

st.title("⚖️ Moralogy Gemini 3 Evaluator")

# Configuración del nuevo cliente de Gemini 3
if "GOOGLE_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    
    user_input = st.text_area("Describe el dilema para Gemini 3:", height=150)

    if st.button("Evaluar con Gemini 3"):
        if user_input:
            with st.spinner("Gemini 3 está analizando..."):
                try:
                    # Usamos el modelo exacto de tu captura: gemini-3-pro-preview
                    response = client.models.generate_content(
                        model="gemini-3-pro-preview", 
                        contents=user_input
                    )
                    st.subheader("Análisis de Última Generación (v3):")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error de conexión con Gemini 3: {e}")
        else:
            st.warning("Escribe algo para que Gemini 3 lo analice.")
else:
    st.error("Configura la API Key en los Secrets.")
