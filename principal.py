import streamlit as st
from motor_logico import ejecutar_auditoria

st.set_page_config(page_title="Moralogy Engine", layout="wide")

st.title("⚖️ Moralogy Engine: Quick Audit")
st.markdown("### Entrada de Escenario Único")

with st.container():
    # Una sola casilla para todo el contexto
    prompt_unico = st.text_area(
        "Describa la situación, los agentes involucrados y las opciones:",
        placeholder="Ej: El sujeto A debe elegir entre X e Y mientras el contexto Z ocurre...",
        height=250
    )

    if st.button("Ejecutar Protocolo Moralogía", type="primary"):
        if prompt_unico:
            with st.spinner("Analizando integridad de agencia..."):
                # Se envía como 'situacion' y el motor procesa el texto completo
                resultado = ejecutar_auditoria(
                    agentes="Identificados en prompt", 
                    situacion=prompt_unico, 
                    contexto="Entrada directa", 
                    categoria="General", 
                    modo="Rápido"
                )
                
                st.divider()
                st.markdown("### Veredicto del Arquitecto")
                # Renderizado básico para la principal
                if "🟢" in resultado: st.success(resultado)
                elif "🟡" in resultado: st.warning(resultado)
                elif "🔴" in resultado: st.error(resultado)
                elif "⚫" in resultado: 
                    st.markdown(f'<div style="background-color:black; color:red; padding:20px; border:1px solid red;">{resultado}</div>', unsafe_allow_html=True)
                else: st.info(resultado)
        else:
            st.warning("Por favor, ingrese un escenario para analizar.")
