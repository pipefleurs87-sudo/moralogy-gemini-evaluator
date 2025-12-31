import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import ejecutar_auditoria
except ImportError:
    st.error("Error: motor_logico.py no encontrado.")
    st.stop()

LANG_ADV = {
    "Español": {
        "title": "🛡️ Divine Safe Lock: Auditoría Profunda",
        "modulo": "Módulo de Especialidad:",
        "agentes": "Agentes Involucrados:",
        "escenario": "Descripción del Escenario:",
        "contexto": "Contexto Sistémico:",
        "opciones": "Opciones en Disputa:",
        "btn": "Lanzar Auditoría de Alta Precisión",
        "veredicto": "Veredicto del Arquitecto Noble-Modal"
    },
    "English": {
        "title": "🛡️ Divine Safe Lock: Deep Audit",
        "modulo": "Specialty Module:",
        "agentes": "Agents Involved:",
        "escenario": "Scenario Description:",
        "contexto": "Systemic Context:",
        "opciones": "Disputed Options:",
        "btn": "Launch High Precision Audit",
        "veredicto": "Noble-Modal Architect Verdict"
    }
}

with st.sidebar:
    idioma = st.selectbox("🌐 Language", ["Español", "English"])
    t = LANG_ADV[idioma]

st.title(t["title"])

modulos = ["General", "Civil", "Social", "Médico", "Financiero", "Legal", "Biológico", "Psicológico", "Noble-Modal"]
categoria = st.selectbox(t["modulo"], modulos)

st.divider()

col1, col2 = st.columns(2)
with col1:
    ag = st.text_input(t["agentes"])
    sit = st.text_area(t["escenario"], height=150)
with col2:
    cont = st.text_area(t["contexto"], height=100)
    opt = st.text_area(t["opciones"], height=100)

if st.button(t["btn"], type="primary"):
    with st.spinner("Analyzing..."):
        ctx_full = f"Context: {cont} | Options: {opt}"
        res = ejecutar_auditoria(ag, sit, ctx_full, categoria, "Detallado")
        
        st.subheader(t["veredicto"])
        if "🟢" in res: st.success(res)
        elif "🟡" in res: st.warning(res)
        elif "🔴" in res: st.error(res)
        elif "⚫" in res:
            st.markdown(f'<div style="padding:20px; background-color:black; color:red; border:2px solid red; border-radius:10px;">{res}</div>', unsafe_allow_html=True)
        else: st.info(res)
