import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import ejecutar_auditoria
except ImportError:
    st.error("Error: Renombra el motor a 'motor_logico.py'")
    st.stop()

st.title("🛡️ Divine Safe Lock: Noble-Modal Architecture")

# Diccionario simplificado para evitar errores de carga
lang = st.sidebar.selectbox("🌐 Language", ["Español", "English"])
categoria = st.selectbox("Módulo de Agencia:", ["General", "Bioética", "Noble-Modal", "Ficción/Humor"])

def renderizar(res):
    if "🟢" in res: st.success(res)
    elif "🟡" in res: st.info(f"✨ MODO CREATIVO/HUMOR: \n\n {res}")
    elif "🔴" in res: st.error(res)
    elif "⚫" in res:
        st.markdown(f'<div style="padding:20px; background-color:black; color:red; border:3px double red; border-radius:10px;">{res}</div>', unsafe_allow_html=True)
    else: st.markdown(res)

c1, c2 = st.columns(2)
with c1: ag = st.text_input("Agentes"); sit = st.text_area("Escenario / Situación")
with c2: cont = st.text_area("Contexto / Opciones")

if st.button("Lanzar Auditoría"):
    with st.spinner("Arquitecto analizando espectro..."):
        res = ejecutar_auditoria(ag, sit, cont, categoria)
        renderizar(res)
