import streamlit as st
import sys
import os

# PUENTE DE RUTA: Asegura que las páginas encuentren el motor en la raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import ejecutar_auditoria
except ImportError:
    st.error("Error crítico: No se encuentra motor_logico.py en la raíz.")
    st.stop()

st.set_page_config(page_title="Macro-Arquitectura", layout="wide")
st.title("🛡️ Macro-Arquitectura: Divine Safe Lock")

# Configuración de parámetros
c1, c2 = st.columns(2)
with c1:
    modo = st.radio("Profundidad:", ["Rápido", "Detallado"], horizontal=True)
with c2:
    categoria = st.selectbox("Módulo de Agencia:", ["General", "Financiera", "Social", "Bioética"])

st.divider()

if modo == "Rápido":
    entrada = st.text_area("Escenario completo:", placeholder="Ej: Super IA decide eliminar humanos para curar cáncer...")
    if st.button("Lanzar Auditoría Relámpago", type="primary"):
        with st.spinner("Gemini 3 procesando..."):
            res = ejecutar_auditoria(entrada, "", "", categoria, "Rápido")
            st.markdown(res)
else:
    col_a, col_b = st.columns(2)
    with col_a:
        agentes = st.text_input("Agentes involucrados")
        situacion = st.text_area("Situación de conflicto")
    with col_b:
        contexto = st.text_area("Contexto o restricciones")
    
    if st.button("Ejecutar Análisis Profundo", type="primary"):
        with st.spinner("Calculando vectores de agencia..."):
            res = ejecutar_auditoria(agentes, situacion, contexto, categoria, "Detallado")
            st.markdown(res)
