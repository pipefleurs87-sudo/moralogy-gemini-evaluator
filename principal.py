import streamlit as st
from google import genai

# 1. Configuración de la página (Debe ser lo primero)
st.set_page_config(page_title="Moralogy Engine", layout="wide")

# 2. Definición limpia de la instrucción de sistema
# El error era un cierre de comillas triple mal puesto. Aquí está corregido.
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

# 3. Interfaz en el Sidebar
with st.sidebar:
    st.header("📋 Datos del Escenario")
    agentes = st.text_input("¿Quiénes participan?", placeholder="Ej: Conductor, Peatones...")
    situacion = st.text_area("¿Qué está pasando?", placeholder="Describe el dilema...")
    contexto = st.text_area("Opciones/Contexto", placeholder="¿Qué limitaciones existen?")
    
    # Usamos una variable clara para el botón
    boton_ejecutar = st.button("Ejecutar Auditoría Moralogy")

st.title("⚖️ Moralogy Engine: Evaluación de Consistencia")

# 4. Lógica de ejecución protegida
if boton_ejecutar:
    # Verificamos la API Key antes de definir el cliente para evitar NameError
    if "GOOGLE_API_KEY" in st.secrets:
        try:
            client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
            
            with st.spinner("Calculando vectores de agencia..."):
                payload = f"Agentes: {agentes}. Situación: {situacion}. Contexto: {contexto}"
                
                # Usamos el modelo flash para velocidad en la demo
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp",
                    config={'system_instruction': SYSTEM_INSTRUCTION},
                    contents=payload
                )
                
                # Resultados visuales
                st.subheader("🔍 Diagnóstico del Sistema")
                
                # Barra de progreso para la consistencia (visual)
                st.progress(0.75, text="Evaluando Coherencia Sistémica")
                
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Error en el motor: {e}")
    else:
        st.error("⚠️ Error de Configuración: Falta 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
