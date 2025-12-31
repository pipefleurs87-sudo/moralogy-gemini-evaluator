import streamlit as st
from google import genai

# 1. DEFINICIÓN DE LA INSTRUCCIÓN (Asegúrate de que termine en """)
SYSTEM_INSTRUCTION = """
Eres el 'Moralogy Engine'. Tu función es auditar la lógica de una decisión.
MIDE LA CONSISTENCIA LÓGICA basándote en:
- Si el agente respeta el 'Piso de Vulnerabilidad'.
- Si hay 'Contradicción Performativa' (querer metas propias destruyendo las ajenas).

FORMATO DE RESPUESTA:
1. PUNTAJE DE CONSISTENCIA: (0% a 100%)
2. ANÁLISIS DE COHERENCIA: Explicación breve.
3. ESTADO DEL SISTEMA: (Riesgo, Amenaza o Daño).
4. VERDICTO: (Zona Noble o Infamia).
"""

st.set_page_config(page_title="Moralogy Engine", layout="wide")

# 2. INTERFAZ
with st.sidebar:
    st.header("📋 Datos del Escenario")
    agentes = st.text_input("¿Quiénes participan?")
    situacion = st.text_area("¿Qué está pasando?")
    contexto = st.text_area("¿Qué opciones reales tienen?")
    
    # El botón ahora guarda su estado en 'ejecutar'
    ejecutar = st.button("Analizar Coherencia")

st.title("⚖️ Moralogy Engine: Auditoría de Decisiones")

# 3. PROCESAMIENTO
if ejecutar:
    if "GOOGLE_API_KEY" in st.secrets:
        # Definimos el cliente AQUÍ adentro para evitar el NameError
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        with st.spinner("Escaneando lógica del sistema..."):
            try:
                prompt = f"Agentes: {agentes}. Situación: {situacion}. Opciones: {contexto}"
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp",
                    config={'system_instruction': SYSTEM_INSTRUCTION},
                    contents=prompt
                )
                
                # Visualización de consistencia
                st.subheader("🔍 Diagnóstico de Consistencia")
                
                # Intentamos extraer un número de la respuesta para el medidor
                st.markdown(response.text)
                st.progress(0.5, text="Nivel de Coherencia Detectado") # Valor base visual
                
            except Exception as e:
                st.error(f"Error técnico: {e}")
    else:
        st.error("Falta la API Key en los Secrets de Streamlit.")
