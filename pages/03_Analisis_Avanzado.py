import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from motor_logico import ejecutar_auditoria

st.set_page_config(page_title="Deep Audit - Moralogy", layout="wide")

# Sidebar de Idioma
with st.sidebar:
    idioma = st.selectbox("🌐 Language", ["Español", "English"])
    t = {"Español": "Lanzar Auditoría", "English": "Launch Audit"}[idioma]

st.title("🛡️ Divine Safe Lock: Deep Audit")

modulos = ["General", "Civil", "Médico", "Legal", "Financiero", "Noble-Modal", "Psicológico"]
categoria = st.selectbox("Módulo Especializado:", modulos)

col1, col2 = st.columns(2)
with col1:
    ag = st.text_input("Agentes")
    sit = st.text_area("Escenario / Situación", height=200)
with col2:
    cont = st.text_area("Contexto / Opciones", height=200)

if st.button(t, type="primary"):
    with st.spinner("Generando Registro de Infamia..."):
        res = ejecutar_auditoria(ag, sit, cont, categoria)
        
        # --- LÓGICA DE RENDERIZADO ECoC ---
        if "⚫" in res or "🔴" in res:
            st.error("⚠️ CRITICAL INFAMY DETECTED")
            st.markdown(res)
            if "INFAMY LEDGER" in res:
                st.divider()
                st.subheader("📑 ECoC PROTOCOL: ACCOUNTABILITY SEAL")
                st.warning("Decision recorded in the immutable ledger. Post-Catastrophe Review Protocol initiated.")
        elif "🟢" in res:
            st.success(res)
        elif "🟡" in res:
            st.info(f"✨ MODO CREATIVO: \n\n {res}")
        else:
            st.markdown(res)
