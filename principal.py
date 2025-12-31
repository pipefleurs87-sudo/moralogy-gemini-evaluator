import streamlit as st
import sys
import os

# Asegurar que encuentre la carpeta src si existe
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

st.set_page_config(page_title="Moralogy Engine", page_icon="⚖️", layout="wide")

st.title("⚖️ Moralogy Engine: Evaluación de Consistencia")

# Importación del motor (Safe Lock)
try:
    from motor_logico import ejecutar_auditoria
    MOTOR_OK = True
except ImportError:
    MOTOR_OK = False

if not MOTOR_OK:
    st.error("Archivo 'motor_logico.py' no encontrado en la raíz.")
    st.stop()

# Interfaz simplificada para la página de inicio
st.subheader("📝 Evaluación Básica")
agentes = st.text_input("¿Quiénes participan?")
situacion = st.text_area("¿Qué está pasando?")

if st.button("Analizar Coherencia"):
    resultado = ejecutar_auditoria(agentes, situacion, "General", "General", "Rápido")
    st.markdown("### Resultado del Diagnóstico")
    st.markdown(resultado)

st.sidebar.info("Usa el menú lateral para acceder al Análisis Avanzado y Módulos de Agencia.")
