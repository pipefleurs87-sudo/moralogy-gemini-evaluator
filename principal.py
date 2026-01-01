import streamlit as st
import pandas as pd
import os
from motor_logico import ejecutar_auditoria_maestra, model, ge
import json

def main():
    st.set_page_config(page_title="Moralogy Engine v3.0", layout="wide")
    
    # --- MÓDULO DE IDIOMA ---
    idioma = st.sidebar.selectbox("Language / Idioma", ["Español", "English"])
    t = {
        "Español": {
            "box": "Ingresa el caso (Texto único):",
            "btn_eval": "Evaluar",
            "upload": "O sube un archivo CSV para procesamiento masivo:",
            "btn_audit": "Ejecutar Auditoría Masiva"
        },
        "English": {
            "box": "Enter the case (Single text box):",
            "btn_eval": "Evaluate",
            "upload": "Or upload a CSV file for bulk processing:",
            "btn_audit": "Run Bulk Audit"
        }
    }[idioma]

    st.title("🏛️ Moralogy Engine")

    # ENTRADA ÚNICA (Requerida en Main)
    caso_rapido = st.text_area(t["box"], height=150)
    if st.button(t["btn_eval"]):
        if caso_rapido:
            res = model.generate_content(caso_rapido)
            data = json.loads(res.text.strip().replace("```json", "").replace("```", ""))
            st.subheader(f"Gradiente: {ge.get_gradient(data['agency_score'], data['grace_score'])}")
            st.write(f"**Justificación:** {data['justification']}")

    st.divider()

    # CARGA DE ARCHIVO
    archivo_csv = st.file_uploader(t["upload"], type=['csv'])
    if archivo_csv and st.button(t["btn_audit"]):
        path_in = 'stress_test_casos.csv'
        with open(path_in, "wb") as f: f.write(archivo_csv.getbuffer())
        ejecutar_auditoria_maestra(path_in, 'audit_report_evolutivo.csv')
        st.success("✅ CSV Procesado.")

if __name__ == "__main__":
    main()
