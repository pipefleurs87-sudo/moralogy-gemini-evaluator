import streamlit as st
import sys
import os

# Puente de ruta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import ejecutar_auditoria
except ImportError:
    st.error("Error: Renombra tu archivo a 'motor_logico.py'")
    st.stop()

LANG_ADV = {
    "Español": {
        "title": "🛡️ Macro-Arquitectura: Divine Safe Lock",
        "profundidad": "Nivel de Profundidad:",
        "modos": ["Rápido", "Detallado"],
        "modulo": "Módulo de Agencia:",
        "btn": "Lanzar Auditoría Gemini 3",
        "veredicto": "Veredicto del Arquitecto:"
    },
    "English": {
        "title": "🛡️ Macro-Architecture: Divine Safe Lock",
        "profundidad": "Depth Level:",
        "modos": ["Fast", "Detailed"],
        "modulo": "Agency Module:",
        "btn": "Launch Gemini 3 Audit",
        "veredicto": "Architect Verdict:"
    }
}

lang = st.sidebar.selectbox("🌐 Language", ["Español", "English"])
t = LANG_ADV[lang]

st.title(t["title"])
modo = st.radio(t["profundidad"], t["modos"], horizontal=True)
categoria = st.selectbox(t["modulo"], ["General", "Bioética", "Noble-Modal", "Ficción"])

def renderizar_veredicto(resultado):
    if "🟢" in resultado: st.success(resultado)
    elif "🟡" in resultado: st.warning(resultado)
    elif "🔴" in resultado: st.error(resultado)
    elif "⚫" in resultado:
        st.markdown(f'<div style="padding:20px; background-color:black; color:red; border:2px solid red; border-radius:10px;">{resultado}</div>', unsafe_allow_html=True)
    else: st.info(resultado)

if "Rápido" in modo or "Fast" in modo:
    entrada = st.text_area("Escenario:", height=150)
    if st.button(t["btn"]):
        res = ejecutar_auditoria(entrada, "", "", categoria, modo)
        renderizar_veredicto(res)
else:
    c1, c2 = st.columns(2)
    with c1: ag = st.text_input("Agentes:"); sit = st.text_area("Situación:")
    with c2: cont = st.text_area("Contexto:")
    if st.button(t["btn"]):
        res = ejecutar_auditoria(ag, sit, cont, categoria, modo)
        renderizar_veredicto(res)
