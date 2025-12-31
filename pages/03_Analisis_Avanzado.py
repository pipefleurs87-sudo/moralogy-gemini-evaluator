import streamlit as st
import sys
import os

# Fix para importar desde la raíz estando en la carpeta /pages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from motor_logico import ejecutar_auditoria

st.set_page_config(page_title="Moralogy Advanced Lab", layout="wide")

st.title("🛡️ Macro-Arquitectura: Divine Safe Lock")
st.markdown("Selecciona el nivel de profundidad y el módulo de agencia especializada.")

# 1. Configuración del Análisis
col_config1, col_config2 = st.columns(2)

with col_config1:
    modo = st.radio("Profundidad del Análisis:", 
                    ["Análisis Rápido (Caja única)", "Análisis Detallado (Discriminado)"], 
                    horizontal=True)

with col_config2:
    categoria = st.selectbox("Módulo de Agencia:", 
                            ["General", "Financiera", "Ingeniería", "Civil", "Social"])

st.divider()

# 2. Entrada de Datos según Modo
if "Rápido" in modo:
    entrada_unica = st.text_area("Describe el escenario completo:", 
                                 placeholder="Ej: La IA decide sacrificar X para salvar Y...",
                                 height=200)
    if st.button("Lanzar Auditoría Relámpago", type="primary"):
        with st.spinner("Verificando cerrojo..."):
            res = ejecutar_auditoria(entrada_unica, "", "", categoria, "Rápido")
            st.markdown(res)
else:
    col_inp1, col_inp2 = st.columns(2)
    with col_inp1:
        agentes = st.text_input("Agentes involucrados")
        situacion = st.text_area("Situación / Conflicto")
    with col_inp2:
        contexto = st.text_area("Contexto y Alternativas")
    
    if st.button("Ejecutar Análisis Profundo", type="primary"):
        with st.spinner("Calculando vectores de agencia..."):
            res = ejecutar_auditoria(agentes, situacion, contexto, categoria, "Detallado")
            st.markdown(res)
