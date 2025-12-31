import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import ejecutar_auditoria
except ImportError:
    st.error("Error: Renombra el motor a 'motor_logico.py'")
    st.stop()

LANG_ADV = {
    "Español": {"title": "🛡️ Divine Safe Lock", "btn": "Lanzar Auditoría", "veredicto": "Veredicto:"},
    "English": {"title": "🛡️ Divine Safe Lock", "btn": "Launch Audit", "veredicto": "Verdict:"}
}

lang = st.sidebar.selectbox("🌐 Language", ["Español", "English"])
t = LANG_ADV[lang]
st.title(t["title"])

categoria = st.selectbox("Módulo:", ["General", "Bioética", "Noble-Modal", "Ficción"])

def renderizar(res):
    if "🟢" in res: st.success(res)
    elif "🟡" in res: st.warning(res)
    elif "🔴" in res: st.error(res)
    elif "⚫" in res:
        st.markdown(f'<div style="padding:20px; background-color:black; color:red; border:2px solid red; border-radius:10px;">{res}</div>', unsafe_allow_html=True)
    else: st.info(res)

c1, c2 = st.columns(2)
with c1: ag = st.text_input("Agentes"); sit = st.text_area("Situación")
with c2: cont = st.text_area("Contexto")

if st.button(t["btn"]):
    res = ejecutar_auditoria(ag, sit, cont, categoria, "Detallado")
    st.subheader(t["veredicto"])
    renderizar(res)
