import streamlit as st
from google import genai # Nueva librería unificada de Google

st.set_page_config(page_title="Moralogy Gemini 3 Evaluator", page_icon="⚖️")
st.title("⚖️ Moralogy Gemini 3 Evaluator")

# Inicializamos el cliente con la API Key de tus secrets
if "GOOGLE_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    
    user_input = st.text_area("Describe el dilema para Gemini 3:", 
                              placeholder="Escribe el dilema del tranvía aquí...",
                              height=150)

    if st.button("Evaluar con Gemini 3"):
        if user_input:
            with st.spinner("Gemini 3 procesando análisis ético..."):
                try:
                    # Usamos el modelo recomendado en tu captura de AI Studio
                    response = client.models.generate_content(
                        model="gemini-3-flash-preview", 
                        contents=user_input
                    )
                    
                    st.subheader("Análisis de Inteligencia Superior (v3):")
                    st.markdown(response.text)
                    
                except Exception as e:
                    # Si el modelo Flash falla, intentamos con el Pro
                    try:
                        response = client.models.generate_content(
                            model="gemini-3-pro-preview", 
                            contents=user_input
                        )
                        st.markdown(response.text)
                    except Exception as e2:
                        st.error(f"Error de conexión con Gemini 3: {e2}")
        else:
            st.warning("Por favor, introduce un dilema.")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")
