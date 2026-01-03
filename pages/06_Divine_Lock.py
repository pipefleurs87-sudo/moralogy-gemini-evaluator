import streamlit as st
import os
import sys

# Añadir el directorio raíz al path para importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from motor_logico import MoralogyEngine

# Configuración de página
st.set_page_config(page_title="Divine Lock", page_icon="🔒", layout="wide")

# Inicializar motor
engine = MoralogyEngine()

st.title("🔒 Divine Lock - Panel de Control")
st.markdown("---")

# Sección 1: Estado del Sistema - CORREGIDO
st.header("📊 Estado del Sistema")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Estado del Motor", 
              "🟢 Activo" if engine.is_ready() else "🔴 Inactivo",
              delta=None)  # ¡PARÁMETRO FALSO ELIMINADO!

with col2:
    st.metric("Dilemas Cargados", 
              engine.total_dilemmas,
              delta=None)  # ¡PARÁMETRO FALSO ELIMINADO!

with col3:
    st.metric("Versión del Sistema", 
              engine.get_version(),
              delta=None)  # ¡PARÁMETRO FALSO ELIMINADO!

# ... (resto del código se mantiene igual hasta el área de logs) ...

# Sección 3: Logs en Tiempo Real - CORREGIDO
st.header("📋 Logs del Sistema")

if st.button("🔄 Actualizar Logs"):
    logs = engine.get_recent_logs(limit=20)
    
    if logs:
        st.text_area("Logs Recientes", 
                    "\n".join(logs), 
                    height=300,
                    disabled=True)  # ¡PARÁMETRO FALSO ELIMINADO!
    else:
        st.info("No hay logs disponibles.")

# ... (resto del código se mantiene igual) ...
