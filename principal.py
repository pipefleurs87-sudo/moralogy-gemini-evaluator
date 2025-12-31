import streamlit as st
from motor_logico import ejecutar_auditoria

st.set_page_config(page_title="Moralogy Engine", layout="wide")

LANG_MAIN = {
    "Español": {
        "title": "⚖️ Motor Moralogy: Auditoría Rápida",
        "label": "Escenario Único (Agentes + Contexto + Situación):",
        "placeholder": "Describa todo aquí para un análisis directo...",
        "btn": "Ejecutar Protocolo Moralogía",
        "result": "Veredicto del Arquitecto"
    },
    "English": {
        "title": "⚖️ Moralogy Engine: Quick Audit",
        "label": "Single Scenario (Agents + Context + Situation):",
        "placeholder": "Describe everything here for a direct analysis...",
        "btn": "Execute Moralogy Protocol",
        "result": "Architect Verdict"
    }
}

with st.sidebar:
    st.title("Admin")
    idioma = st.selectbox("🌐 Language / Idioma", ["Español", "English"])
    t = LANG_MAIN[idioma]

st.title(t["title"])

with st.container():
    prompt_unico = st.text_area(t["label"], placeholder=t["placeholder"], height=300)

    if st.button(t["btn"], type="primary"):
        if prompt_unico:
            with st.spinner("Analyzing Agency Integrity..."):
                resultado = ejecutar_auditoria(
                    agentes="Embedded in scenario", 
                    situacion=prompt_unico, 
                    contexto="Direct Quick Audit", 
                    categoria="General"
                )
                st.divider()
                st.markdown(f"### {t['result']}")
                
                if "🟢" in resultado: st.success(resultado)
                elif "🟡" in resultado: st.info(resultado)
                elif "🔴" in resultado: st.error(resultado)
                elif "⚫" in resultado:
                    st.markdown(f'<div style="background-color:black; color:#FF3333; padding:20px; border:2px solid red; border-radius:10px;">{resultado}</div>', unsafe_allow_html=True)
                else: st.info(resultado)
