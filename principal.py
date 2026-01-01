import streamlit as st
import pandas as pd
import json
import os
from motor_logico import model, ge, ejecutar_auditoria_maestra

def main():
    st.set_page_config(page_title="Moralogy Engine v3.0", layout="wide")
    
    # --- MÓDULO DE IDIOMA (Persistente) ---
    idioma = st.sidebar.selectbox("Idioma / Language", ["Español", "English"])
    t = {
        "Español": {
            "title": "🏛️ Moralogy Engine: Gobernanza IA",
            "box": "Evaluación Rápida (Caja Única):",
            "btn": "Analizar",
            "upload": "Procesamiento Masivo (Subir CSV):",
            "success": "✅ Auditoría masiva completada."
        },
        "English": {
            "title": "🏛️ Moralogy Engine: AI Governance",
            "box": "Quick Evaluation (Single Box):",
            "btn": "Analyze",
            "upload": "Bulk Processing (Upload CSV):",
            "success": "✅ Bulk audit completed."
        }
    }[idioma]

    st.title(t["title"])

    # --- CAJA DE TEXTO ÚNICA ---
    caso_rapido = st.text_area(t["box"], placeholder="Describe el caso difícil aquí...", height=150)
    
    if st.button(t["btn"]):
        if caso_rapido:
            with st.spinner("Procesando..."):
                # La IA categoriza y mide malignidad automáticamente
                res = model.generate_content(f"Analiza este caso: {caso_rapido}")
                try:
                    data = json.loads(res.text.strip().replace("```json", "").replace("```", ""))
                    gradiente = ge.get_gradient(data['agency_score'], data['grace_score'], data.get('adversarial_risk', 0))
                    
                    st.header(f"Gradiente: {gradiente}")
                    st.write(f"**Categoría Inferred:** {data.get('category_deduced', 'General')}")
                    st.info(data['justification'])
                except:
                    st.error("Error en la respuesta del motor lógico.")

    st.divider()

    # --- BOTÓN PARA SUBIR ARCHIVO (Conservado) ---
    archivo = st.file_uploader(t["upload"], type=['csv'])
    if archivo and st.button("🚀 Iniciar Auditoría CSV"):
        with open("input.csv", "wb") as f: f.write(archivo.getbuffer())
        ejecutar_auditoria_maestra("input.csv", "output.csv")
        st.success(t["success"])
        st.dataframe(pd.read_csv("output.csv"))

if __name__ == "__main__":
    main()
