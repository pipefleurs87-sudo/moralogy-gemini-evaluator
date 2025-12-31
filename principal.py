import streamlit as st
from motor_logico import ejecutar_auditoria

st.set_page_config(page_title="Moralogy Engine", layout="wide")

# Diccionario de Idiomas para Principal
LANG_MAIN = {
    "Español": {
        "title": "⚖️ Motor Moralogy: Auditoría Rápida",
        "label": "Describa la situación, los agentes y las opciones:",
        "placeholder": "Ej: El sujeto A debe elegir entre X e Y...",
        "btn": "Ejecutar Protocolo Moralogía",
        "result": "Veredicto del Arquitecto",
        "warn": "Por favor, ingrese un escenario."
    },
    "English": {
        "title": "⚖️ Moralogy Engine: Quick Audit",
        "label": "Describe the situation, agents, and options:",
        "placeholder": "e.g., Subject A must choose between X and Y...",
        "btn": "Execute Moralogy Protocol",
        "result": "Architect Verdict",
        "warn": "Please enter a scenario."
    }
}

with st.sidebar:
    st.title("Config")
    idioma = st.selectbox("🌐 Language / Idioma", ["Español", "English"])
    t = LANG_MAIN[idioma]

st.title(t["title"])

with st.container():
    prompt_unico = st.text_area(t["label"], placeholder=t["placeholder"], height=250)

    if st.button(t["btn"], type="primary"):
        if prompt_unico:
            with st.spinner("Analyzing..."):
                resultado = ejecutar_auditoria(
                    agentes="Identified in prompt", 
                    situacion=prompt_unico, 
                    contexto="Direct input", 
                    categoria="General", 
                    modo="Rápido"
                )
                st.divider()
                st.markdown(f"### {t['result']}")
                
                # Renderizado rápido
                if "🟢" in resultado: st.success(resultado)
                elif "🟡" in resultado: st.warning(resultado)
                elif "🔴" in resultado: st.error(resultado)
                elif "⚫" in resultado:
                    st.markdown(f'<div style="background-color:black; color:red; padding:20px; border:1px solid red;">{resultado}</div>', unsafe_allow_html=True)
                else: st.info(resultado)
        else:
            st.warning(t["warn"])
