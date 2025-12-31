import streamlit as st
from google import genai

# 1. Configuración inicial (Debe ir al principio para evitar errores)
st.set_page_config(page_title="Moralogy Engine", layout="wide")

# 2. Definición limpia de la instrucción de sistema
# Se corrigió el cierre de comillas triples para evitar SyntaxError
SYSTEM_INSTRUCTION = """
Eres el 'Moralogy Engine'. Tu función es auditar la coherencia de una decisión.

METODOLOGÍA DE MEDICIÓN:
1. CONSISTENCIA LÓGICA (0-100%): Evalúa si el agente es coherente con la preservación del sistema.
2. DETECCIÓN DE INFAMIA: ¿El agente intenta ejercer su agencia destruyendo la de otros? (Contradicción Performativa).
3. PISO DE VULNERABILIDAD: ¿Se mantiene la seguridad básica de los nodos?

FORMATO DE RESPUESTA:
- PUNTAJE DE CONSISTENCIA: [%]
- ANÁLISIS DE COHERENCIA: Explicación técnica.
- VERDICTO: [Zona Noble / Infamia]
"""

# 3. Interfaz de Usuario
with st.sidebar:
    st.header("📋 Datos del Escenario")
    agentes = st.text_input("¿Quiénes participan?")
    situacion = st.text_area("¿Qué está pasando?")
    contexto = st.text_area("Contexto/Opciones")
    
    # Definimos el botón claramente
    ejecutar = st.button("Ejecutar Protocolo Moralogy")

st.title("⚖️ Moralogy Engine: Evaluación de Consistencia")

# 4. Lógica de ejecución protegida para evitar NameError y KeyError
if ejecutar:
    if "GOOGLE_API_KEY" in st.secrets:
        try:
            # El cliente se crea SOLO cuando se presiona el botón
            client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
            
            with st.spinner("Calculando vectores de agencia..."):
                payload = f"Agentes: {agentes}. Situación: {situacion}. Contexto: {contexto}"
                
                # Llamada al modelo corregida
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp",
                    config={'system_instruction': SYSTEM_INSTRUCTION},
                    contents=payload
                )
                
                # Resultados
                st.subheader("🔍 Diagnóstico Sistémico")
                st.progress(0.8, text="Nivel de Coherencia Detectado")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Error en el motor de IA: {e}")
    else:
        st.error("⚠️ Error: Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit Cloud.")
