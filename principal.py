import streamlit as st
import google.generativeai as genai

# Configuración visual
st.set_page_config(page_title="Moralogy Evaluator", page_icon="⚖️")

st.title("⚖️ Moralogy Gemini Evaluator")
st.write("Bienvenido al evaluador de dilemas éticos.")

# Conexión segura con la API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
   model = genai.GenerativeModel('models/gemini-1.5-flash')

    # Interfaz de entrada
    user_input = st.text_area("Describe el dilema o situación moral:", 
                              placeholder="Ejemplo: ¿Es ético usar IA para tomar decisiones médicas?",
                              height=150)

    if st.button("Realizar Evaluación"):
        if user_input:
            with st.spinner("Gemini está analizando la situación..."):
                try:
                    # El prompt que le enviamos a la IA
                    prompt = f"Actúa como un experto en ética y filosofía. Evalúa el siguiente dilema: {user_input}"
                    response = model.generate_content(prompt)
                    
                    st.subheader("Análisis de la IA:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error técnico: {e}")
        else:
            st.warning("Por favor, escribe algo antes de evaluar.")
else:
    st.warning("⚠️ La API Key no está configurada en los Secrets de Streamlit.")
    st.info("Para arreglarlo: Ve a Manage App > Settings > Secrets y añade GOOGLE_API_KEY = 'tu_clave'")
