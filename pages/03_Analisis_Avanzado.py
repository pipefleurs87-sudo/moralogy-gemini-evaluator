import streamlit as st
import sys
import os

# Puente de ruta para encontrar el motor en la raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import ejecutar_auditoria
except ImportError:
    st.error("No se encontró 'motor_logico.py' en la raíz del proyecto.")
    st.stop()

st.set_page_config(page_title="Análisis Avanzado", layout="wide")
st.title("🛡️ Macro-Arquitectura: Divine Safe Lock")

modo = st.radio("Profundidad:", ["Rápido", "Detallado"], horizontal=True)
categoria = st.selectbox("Módulo:", ["General", "Financiera", "Social", "Civil"])

st.divider()

if modo == "Rápido":
    entrada = st.text_area("Escenario completo:", height=200)
    if st.button("Lanzar Auditoría"):
        with st.spinner("Analizando..."):
            res = ejecutar_auditoria(entrada, "", "", categoria, "Rápido")
            st.write(res)
else:
    c1, c2 = st.columns(2)
    with c1:
        agentes = st.text_input("Agentes")
        situacion = st.text_area("Situación")
    with c2:
        contexto = st.text_area("Contexto")
    
    if st.button("Ejecutar Análisis Profundo"):
        with st.spinner("Calculando..."):
            res = ejecutar_auditoria(agentes, situacion, contexto, categoria, "Detallado")
            st.write(res)
