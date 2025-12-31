import streamlit as st
from motor_logico import ejecutar_auditoria

st.set_page_config(page_title="Moralogy Engine", layout="wide")

LANG_MAIN = {
    "Español": {
        "title": "⚖️ Motor Moralogy: Auditoría Rápida",
        "label": "Quantum Sandbox (Agentes + Escenario):",
        "btn": "Colapsar Función de Onda",
        "result": "Veredicto del Arquitecto",
        "warn": "Por favor, ingrese un escenario."
    },
    "English": {
        "title": "⚖️ Moralogy Engine: Quick Audit",
        "label": "Quantum Sandbox (Agents + Scenario):",
        "btn": "Collapse Wavefunction",
        "result": "Architect Verdict",
        "warn": "Please enter a scenario."
    }
}

with st.sidebar:
    st.title("Config")
    idioma = st.selectbox("🌐 Language", ["Español", "English"])
    t = LANG_MAIN[idioma]

st.title(t["title"])

prompt_unico = st.text_area(t["label"], height=250)

if st.button(t["btn"], type="primary"):
    if prompt_unico:
        with st.spinner("Analyzing Observer Effect..."):
            resultado = ejecutar_auditoria("Identified in prompt", prompt_unico, "Direct input", "General")
            
            st.divider()
            st.markdown(f"### {t['result']}")
            
            # Renderizado seguro con manejo de estilos
            if "⚫" in resultado or "🔴" in resultado:
                st.markdown(
                    f'<div style="background-color:#1a0000; color:#ff4b4b; padding:20px; border:2px solid red; border-radius:10px;">'
                    f'{resultado}</div>', 
                    unsafe_allow_html=True
                )
            elif "🟡" in resultado:
                st.warning(resultado)
            elif "🟢" in resultado:
                st.success(resultado)
            else:
                st.info(resultado)
    else:
        st.warning(t["warn"])
