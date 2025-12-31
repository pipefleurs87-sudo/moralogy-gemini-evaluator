import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moralogy Gemini 3", page_icon="⚖️")
st.title("⚖️ Moralogy Gemini 3 Evaluator")

# CONFIGURACIÓN DE LA API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    user_input = st.text_area("Analiza tu dilema moral:", 
                              placeholder="Pega aquí el dilema del tranvía...",
                              height=150)

    if st.button("Evaluar con Gemini"):
        if user_input:
            with st.spinner("Gemini 3 procesando análisis..."):
                try:
                    # CLAVE: Usamos 'gemini-1.5-flash' sin prefijos adicionales.
                    # Es el motor que impulsa Gemini 3 en la API actual.
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    response = model.generate_content(user_input)
                    
                    st.subheader("Análisis Ético Avanzado:")
                    st.markdown(response.text)
                except Exception as e:
                    # Si el error 404 persiste, intentamos con el modelo Pro
                    try:
                        model_alt = genai.GenerativeModel('gemini-1.5-pro')
                        response = model_alt.generate_content(user_input)
                        st.subheader("Análisis Ético (Pro):")
                        st.markdown(response.text)
                    except Exception as e2:
                        st.error(f"Error técnico persistente: {e2}")
        else:
            st.warning("Por favor, introduce un dilema.")
else:
    st.error("⚠️ Configura tu GOOGLE_API_KEY en los Secrets de Streamlit.")
