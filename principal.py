import streamlit as st
import sys
import os

# Asegurar que encuentre la carpeta raíz para las importaciones
sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(
    page_title="Moralogy Engine: Auditoría de Decisiones",
    page_icon="⚖️",
    layout="wide"
)

# Cargamos el motor de forma segura
try:
    from motor_logico import ejecutar_auditoria
    MOTOR_OK = True
except ImportError as e:
    MOTOR_OK = False
    import_error = str(e)

st.title("⚖️ Moralogy Engine: Evaluación de Consistencia")

if not MOTOR_OK:
    st.error(f"Falta el archivo motor_logico.py: {import_error}")
    st.stop()

# Interfaz simplificada
with st.sidebar:
    st.subheader("Configuración")
    # Cambiamos a 1.5 Flash para evitar el error 429
    modelo_seleccionado = "gemini-1.5-flash"
    st.info(f"Modelo activo: {modelo_seleccionado}")

col1, col2 = st.columns([2, 1])
with col1:
    agentes = st.text_input("Participantes:")
    situacion = st.text_area("Escenario:")
    contexto = st.text_area("Opciones:")

if st.button("Ejecutar Protocolo Moralogy"):
    with st.spinner("Analizando con Gemini 1.5 Flash..."):
        # Forzamos el uso del modelo con más cuota
        resultado = ejecutar_auditoria(agentes, situacion, contexto, "General", "Rápido")
        st.markdown(resultado)
