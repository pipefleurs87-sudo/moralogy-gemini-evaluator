import streamlit as st
import pandas as pd
import os
import json
from motor_logico import model, ge, ejecutar_auditoria_maestra

def main():
    st.set_page_config(page_title="Moralogy Engine", layout="wide")

    # MÓDULO DE IDIOMA
    idioma = st.sidebar.selectbox("Language / Idioma", ["Español", "English"])
    t = {
        "Español": {"t": "🏛️ Moralogy Engine", "box": "Evaluación Rápida:", "btn": "Analizar", "csv": "Carga CSV"},
        "English": {"t": "🏛️ Moralogy Engine", "box": "Quick Evaluation:", "btn": "Analyze", "csv": "Upload CSV"}
    }[idioma]

    st.title(t["t"])

    # CAJA DE TEXTO ÚNICA
    caso = st.text_area(t["box"], height=150)
    if st.button(t["btn"]):
        if caso:
            res = model.generate_content(f"Analiza este caso: {caso}")
            data = json.loads(res.text.strip().replace("```json", "").replace("```", ""))
            st.header(f"Gradiente: {ge.get_gradient(data['agency_score'], data['grace_score'], data.get('adversarial_risk', 0))}")
            st.info(data['justification'])

    st.divider()
    
    # CARGA DE ARCHIVO
    archivo = st.file_uploader(t["csv"], type=['csv'])
    if archivo and st.button("🚀 Run Audit"):
        with open("temp.csv", "wb") as f: f.write(archivo.getbuffer())
        ejecutar_auditoria_maestra("temp.csv", "reporte.csv")
        st.dataframe(pd.read_csv("reporte.csv"))

if __name__ == "__main__":
    main()
