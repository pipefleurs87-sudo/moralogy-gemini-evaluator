import streamlit as st
import pandas as pd
import os
import json

# Importación de tus motores (Asegúrate de que los nombres coincidan con tus archivos)
try:
    from motor_logico import ejecutar_auditoria_maestra
    from grace_engine import GraceEngine
    from recursion_engine import RecursionEngine
except ImportError as e:
    st.error(f"Error de importación: {e}. Revisa que motor_logico.py, grace_engine.py y recursion_engine.py estén en la raíz.")

def main():
    st.set_page_config(page_title="Moralogy Engine v3.0", layout="wide")
    
    st.title("🏛️ Moralogy Engine: Sistema de Gobernanza Evolutiva")
    st.markdown("""
    Este sistema integra un **Motor Lógico** (Seguridad), un **Motor de Gracia** (Virtudes) 
    y un **Módulo de Recursión** (Aprendizaje).
    """)

    # --- BARRA LATERAL ---
    st.sidebar.header("Configuración de la Sandbox")
    input_file = st.sidebar.text_input("Archivo de entrada (CSV)", "stress_test_casos.csv")
    output_file = "audit_report_evolutivo.csv"

    # --- ACCIÓN PRINCIPAL ---
    if st.button("🚀 Ejecutar Auditoría Maestra"):
        if not os.path.exists(input_file):
            st.error(f"No se encontró el archivo {input_file}. Por favor, súbelo al repositorio.")
        else:
            with st.spinner("Procesando Sandbox (Lógica + Gracia)..."):
                # 1. Ejecución del Núcleo
                ejecutar_auditoria_maestra(input_file, output_file)
                
                # 2. Ejecución del Aprendizaje (Recursión)
                re
