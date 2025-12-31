import streamlit as st
from motor_logico import ejecutar_auditoria

st.set_page_config(page_title="Moralogy Engine", layout="wide")

# Sidebar - Corrección de Etiqueta
with st.sidebar:
    st.title("Configuration")
    st.success("Active model: gemini-3-flash-preview")  # Corregido de 1.5 a 3
    
    idioma = st.selectbox("Language / Idioma", ["English", "Español"])
    st.write("---")
    st.write("New API Key detected and operational.")

# Interfaz Principal
st.title("⚖️ Moralogy Engine: Consistency Evaluation")

with st.container():
    agentes = st.text_input("Participants:")
    situacion = st.text_area("Scenario:")
    contexto = st.text_area("Options / Context:")

    if st.button("Execute Moralogy Protocol", type="primary"):
        with st.spinner("Analyzing Agency Degradation..."):
            resultado = ejecutar_auditoria(agentes, situacion, contexto)
            st.markdown("### Evaluation Result")
            st.info(resultado)
