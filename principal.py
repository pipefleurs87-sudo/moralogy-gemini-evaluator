import streamlit as st
import sys
import os
from datetime import datetime

# Fix para asegurar que encuentre la carpeta 'src'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

st.set_page_config(
    page_title="Moralogy Engine: Auditoría Pro",
    page_icon="⚖️",
    layout="wide"
)

# Inicialización con Gemini 1.5 Pro (2M Context)
@st.cache_resource
def init_engines():
    try:
        from motor_logico import ejecutar_auditoria
        return ejecutar_auditoria, None
    except ImportError as e:
        return None, f"Error de importación: {str(e)}"

ejecutar, error_import = init_engines()

st.title("⚖️ Moralogy Engine: Evaluación de Consistencia")

if error_import:
    st.error(f"⚠️ {error_import}. Verifica que 'motor_logico.py' esté en la raíz.")
    st.stop()

# Interfaz de entrada
col1, col2 = st.columns([2, 1])
with col1:
    agentes = st.text_input("Participantes:")
    situacion = st.text_area("Escenario:")
    contexto = st.text_area("Contexto Adicional:")

if st.button("Ejecutar Protocolo Moralogy"):
    with st.spinner("Analizando con Gemini 1.5 Pro (Contexto Extendido)..."):
        # Llamada al motor actualizado
        resultado = ejecutar(agentes, situacion, contexto, "General", "Detallado")
        st.markdown(resultado)
