import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moralogy Evaluator", page_icon="⚖️")

st.title("⚖️ Moralogy Gemini Evaluator")

# Verifica si la llave existe en los Secrets
if "GOOGLE_API_KEY" in st.secrets:
    # Todo lo que sigue tiene 4 espacios de sangría
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Esta es la línea 13 que te daba error:
    model = genai.GenerativeModel('models/gemini-1.5-flash')

    user_input = st.text_area("Describe el dilema o situación moral:", height=150)

    if st.button("Realizar Evaluación"):
        if user_input:
            with st.spinner("Analizando con Gemini..."):
                try:
                    response = model.generate_content(user_input)
                    st.subheader("Análisis Ético:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error técnico: {e}")
        else:
            st.warning("Introduce un dilema para continuar.")
else:
    # Este bloque vuelve al nivel del 'if' inicial
    st.error("Configura tu GOOGLE_API_KEY en los Secrets de Streamlit.")
