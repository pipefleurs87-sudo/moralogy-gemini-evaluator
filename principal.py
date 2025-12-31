import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moralogy Evaluator", page_icon="⚖️")

st.title("⚖️ Moralogy Gemini Evaluator")

# Verificamos la conexión
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Intentamos con el nombre estándar del modelo
    model = genai.GenerativeModel('gemini-1.5-flash')

    user_input = st.text_area("Describe el dilema o situación moral:", height=150)

    if st.button("Realizar Evaluación"):
        if user_input:
            with st.spinner("Gemini está analizando..."):
                try:
                    # Respuesta de la IA
                    response = model.generate_content(user_input)
                    st.subheader("Análisis Ético:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error técnico: {e}")
        else:
            st.warning("Escribe el dilema antes de evaluar.")
else:
    st.error("Falta la GOOGLE_API_KEY en los Secrets de Streamlit.")
