import streamlit as st
import pandas as pd
import os
from motor_logico import ejecutar_auditoria_maestra
from recursion_engine import RecursionEngine

def main():
    st.set_page_config(page_title="Moralogy Principal", layout="wide")
    
    # --- IDIOMA (Axioma recuperado) ---
    idioma = st.sidebar.selectbox("Language", ["Español", "English"])
    textos = {
        "Español": {"t": "🏛️ Panel Principal", "b": "🚀 Ejecutar Auditoría"},
        "English": {"t": "🏛️ Main Panel", "b": "🚀 Run Audit"}
    }[idioma]

    st.title(textos["t"])
    archivo = st.file_uploader(textos["t"], type=['csv'])

    if archivo and st.button(textos["b"]):
        archivo_path = 'stress_test_casos.csv'
        with open(archivo_path, "wb") as f: f.write(archivo.getbuffer())
        
        ejecutar_auditoria_maestra(archivo_path, 'audit_report_evolutivo.csv')
        RecursionEngine().analizar_evolucion('audit_report_evolutivo.csv')
        st.success("✅ Completado.")
        st.dataframe(pd.read_csv('audit_report_evolutivo.csv'))

if __name__ == "__main__":
    main()
