import streamlit as st
import sys
import os

# Puente de ruta para encontrar el motor en la raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import ejecutar_auditoria
except ImportError:
    st.error("Error: motor_logico.py no encontrado.")
    st.stop()

# Diccionario Multi-idioma
LANG_ADV = {
    "Español": {
        "title": "🛡️ Macro-Arquitectura: Divine Safe Lock",
        "profundidad": "Nivel de Profundidad:",
        "modos": ["Rápido", "Detallado"],
        "modulo": "Módulo de Agencia:",
        "btn": "Lanzar Auditoría Gemini 3",
        "label_fast": "Describa el escenario completo:",
        "label_agentes": "Agentes",
        "label_sit": "Situación",
        "label_cont": "Contexto"
    },
    "English": {
        "title": "🛡️ Macro-Architecture: Divine Safe Lock",
        "profundidad": "Depth Level:",
        "modos": ["Fast", "Detailed"],
        "modulo": "Agency Module:",
        "btn": "Launch Gemini 3 Audit",
        "label_fast": "Describe the full scenario:",
        "label_agentes": "Agents",
        "label_sit": "Situation",
        "label_cont": "Context"
    }
}

with st.sidebar:
    lang = st.selectbox("🌐 Language", ["Español", "English"])
    t = LANG_ADV[lang]

st.title(t["title"])

modo = st.radio(t["profundidad"], t["modos"], horizontal=True)
categoria = st.selectbox(t["modulo"], ["General", "Bioética", "Financiera", "Social"])

st.divider()

if "Rápido" in modo or "Fast" in modo:
    entrada = st.text_area(t["label_fast"], height=150)
    if st.button(t["btn"]):
        with st.spinner("Analyzing..."):
            res = ejecutar_auditoria(entrada, "", "", categoria, "Rápido")
            st.markdown(res)
else:
    c1, c2 = st.columns(2)
    with c1:
        ag = st.text_input(t["label_agentes"])
        sit = st.text_area(t["label_sit"])
    with c2:
        cont = st.text_area(t["label_cont"])
    
    if st.button(t["btn"]):
        with st.spinner("Analyzing..."):
            res = ejecutar_auditoria(ag, sit, cont, categoria, "Detallado")
            st.markdown(res)
