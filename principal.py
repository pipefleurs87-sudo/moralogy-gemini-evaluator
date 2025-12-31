import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moralogy Gemini 3", page_icon="⚖️")
st.title("⚖️ Moralogy Gemini 3 Evaluator")

# CONFIGURACIÓN DE SEGURIDAD
if "GOOGLE_API_KEY" in st.secrets:
    # Forzamos la configuración con la API Key
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    user_input = st.text_area("Describe el dilema ético:", 
                              placeholder="Pega aquí el dilema del tranvía...",
                              height=150)

    if st.button("Evaluar con Gemini"):
        if user_input:
            with st.spinner("Gemini 3 procesando análisis..."):
                try:
                    # CLAVE: Especificamos el modelo sin prefijos y usamos la API estable
                    # La librería google-generativeai manejará la ruta correcta
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Generamos el contenido
                    response = model.generate_content(user_input)
                    
                    if response.text:
                        st.subheader("Análisis de Inteligencia v3:")
                        st.markdown(response.text)
                    else:
                        st.error("El modelo no devolvió una respuesta clara.")
                        
                except Exception as e:
                    # Capturamos el error para diagnosticar si persiste el 404
                    st.error(f"Error detectado: {e}")
                    st.info("Sugerencia: Si el error es 404, intenta cambiar el nombre del modelo a 'gemini-1.5-pro'.")
        else:
            st.warning("Escribe el dilema antes de evaluar.")
else:
    st.error("⚠️ Falta la API Key en los Secrets de Streamlit.")
