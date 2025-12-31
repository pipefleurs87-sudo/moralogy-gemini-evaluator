import streamlit as st
import google.generativeai as genai
import os

# Configuración de la página
st.set_page_config(page_title="Moralogy Gemini Evaluator", layout="centered")

# --- Configuración de la API Key ---
# Puedes usar secretos de Streamlit o una variable de entorno
api_key = st.sidebar.text_input("Introduce tu Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("Por favor, introduce tu API Key de Google en la barra lateral para comenzar.")

# --- Interfaz de Usuario ---
st.title("🧠 Moralogy Gemini Evaluator")
st.write("Evalúa dilemas morales y éticos utilizando inteligencia artificial.")

# Área de entrada del usuario
user_input = st.text_area("Describe el dilema o situación moral:", placeholder="Ej: ¿Es ético el uso de IA para tomar decisiones judiciales?")

if st.button("Evaluar Escenario"):
    if not api_key:
        st.error("Falta la API Key.")
    elif not user_input:
        st.info("Por favor, escribe un escenario.")
    else:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # --- El Prompt (Corregido y seguro) ---
            prompt = f"""
            Actúa como un experto en ética y moralidad profesional. 
            Analiza el siguiente escenario desde diversas perspectivas éticas 
            (utilitarismo, deontología y ética de la virtud):
            
            Escenario: {user_input}
            
            Proporciona una evaluación detallada y una conclusión sugerida.
            """ 
            
            with st.spinner("Analizando dilema..."):
                response = model.generate_content(prompt)
                
                st.subheader("Análisis Ético")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Hubo un error con la API: {e}")

# --- Pie de página ---
st.divider()
st.caption("Herramienta de evaluación moral basada en modelos generativos de Google.")
