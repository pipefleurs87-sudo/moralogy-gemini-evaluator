import streamlit as st
from motor_logico import ejecutar_auditoria

st.set_page_config(page_title="Moralogy Engine", layout="wide")

with st.sidebar:
    st.title("Configuration")
    st.success("Active model: gemini-3-flash-preview")
    idioma = st.selectbox("Language / Idioma", ["English", "Español"])

st.title("⚖️ Moralogy Engine: Consistency Evaluation")

with st.container():
    agentes = st.text_input("Participants:")
    situacion = st.text_area("Scenario:")
    contexto = st.text_area("Options / Context:")

    if st.button("Execute Moralogy Protocol", type="primary"):
        with st.spinner("Analyzing Agency..."):
            # CORRECCIÓN: Se pasan todos los argumentos necesarios
            resultado = ejecutar_auditoria(agentes, situacion, contexto, categoria="General", modo="Standard")
            st.markdown("### Evaluation Result")
            if "🔴" in resultado or "⚫" in resultado:
                st.error(resultado)
            else:
                st.info(resultado)
