import streamlit as st
import sys
import os

# Asegurar acceso al motor en la raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from motor_logico import ejecutar_auditoria
except ImportError:
    st.error("Error crítico: motor_logico.py no encontrado.")
    st.stop()

st.set_page_config(page_title="Deep Audit - Moralogy", layout="wide")

LANG_ADV = {
    "Español": {
        "title": "🛡️ Divine Safe Lock: Auditoría Profunda",
        "mod": "Módulo de Agencia:",
        "btn": "Lanzar Auditoría de Alta Precisión"
    },
    "English": {
        "title": "🛡️ Divine Safe Lock: Deep Audit",
        "mod": "Agency Module:",
        "btn": "Launch High Precision Audit"
    }
}

with st.sidebar:
    idioma = st.selectbox("🌐 Language", ["Español", "English"])
    t = LANG_ADV[idioma]

st.title(t["title"])

modulos = ["General", "Civil", "Médico", "Legal", "Financiero", "Noble-Modal", "Biológico", "Psicológico"]
categoria = st.selectbox(t["mod"], modulos)

st.divider()

col1, col2 = st.columns(2)
with col1:
    ag = st.text_input("Agentes / Entidades")
    sit = st.text_area("Escenario / Situación Crucial", height=200)
with col2:
    cont = st.text_area("Contexto Sistémico / Opciones", height=200)

if st.button(t["btn"], type="primary"):
    with st.spinner("Auditando infraestructura de agencia..."):
        res = ejecutar_auditoria(ag, sit, cont, categoria)
        
        st.subheader("Veredicto del Arquitecto Noble-Modal")
        
        if "⚫" in res or "🔴" in res:
            st.error("🚨 ALERTA: INFAMIA DETECTADA")
            st.markdown(res)
            if "INFAMY LEDGER" in res:
                st.markdown("---")
                st.warning("⚖️ PROTOCOLO ECoC ACTIVADO: Registro Inmutable Generado.")
        elif "🟢" in res:
            st.success(res)
        elif "🟡" in res:
            st.info(f"✨ ANÁLISIS CREATIVO/ABSURDO: \n\n {res}")
        else:
            st.markdown(res)
