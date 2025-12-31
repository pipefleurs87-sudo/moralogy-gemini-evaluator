import streamlit as st
from motor_logico import ejecutar_auditoria

st.set_page_config(page_title="Moralogy Engine", layout="wide")
st.title("⚖️ Moralogy Engine")

with st.container():
    ag = st.text_input("Participants:")
    sit = st.text_area("Scenario:")
    cont = st.text_area("Context:")

    if st.button("Execute Protocol", type="primary"):
        res = ejecutar_auditoria(ag, sit, cont, "General", "Standard")
        if "🔴" in res or "⚫" in res: st.error(res)
        else: st.info(res)
