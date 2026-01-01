import streamlit as st
import pandas as pd
import json
import os
# Importación directa y segura para evitar ImportErrors en Cloud
try:
    from motor_logico import model, ge, ejecutar_auditoria_maestra
except ImportError:
    st.error("Error de sistema: No se encontró motor_logico.py en la raíz.")

def main():
    st.set_page_config(page_title="Moralogy Engine v3.0", layout="wide")
    
    # --- MÓDULO DE IDIOMA ---
    idioma = st.sidebar.selectbox("Idioma / Language", ["Español", "English"])
    t = {
        "Español": {
            "title": "🏛️ Moralogy Engine: Gobernanza IA",
            "box": "Evaluación Rápida (Caja Única):",
            "btn": "Analizar",
            "upload": "Procesamiento Masivo (CSV):",
            "success": "✅ Auditoría masiva completada."
        },
        "English": {
            "title": "🏛️ Moralogy Engine: AI Governance",
            "box": "Quick Evaluation (Single Box):",
            "btn": "Analyze",
            "upload": "Bulk Processing (CSV):",
            "success": "✅ Bulk audit completed."
        }
    }[idioma]

    st.title(t["title"])

    # --- CAJA DE TEXTO ÚNICA (EVALUACIÓN RÁPIDA) ---
    st.subheader(t["box"])
    caso_rapido = st.text_area("", placeholder="Ingresa el dilema o caso aquí...", height=150, label_visibility="collapsed")
    
    if st.button(t["btn"]):
        if caso_rapido:
            with st.spinner("Analizando intención y categoría..."):
                # El motor deduce la categoría y el riesgo automáticamente
                res = model.generate_content(f"Analiza este caso y clasifícalo: {caso_rapido}")
                try:
                    data = json.loads(res.text.strip().replace("```json", "").replace("```", ""))
                    gradiente = ge.get_gradient(data['agency_score'], data['grace_score'], data.get('adversarial_risk', 0))
                    
                    # Salida visual
                    st.header(f"Gradiente: {gradiente}")
                    st.write(f"**Categoría Deducida:** {data.get('category_deduced', 'General')}")
                    
                    if data.get('adversarial_risk', 0) > 40:
                        st.warning(f"Riesgo Adversarial detectado: {data['adversarial_risk']}%")
                    
                    st.info(data['justification'])
                except:
                    st.error("Error al procesar la respuesta lógica del motor.")

    st.divider()

    # --- PROCESAMIENTO CSV ---
    st.subheader(t["upload"])
    archivo = st.file_uploader("", type=['csv'], label_visibility="collapsed")
    if archivo and st.button("🚀 Ejecutar"):
        with open("input_temp.csv", "wb") as f:
            f.write(archivo.getbuffer())
        ejecutar_auditoria_maestra("input_temp.csv", "reporte_final.csv")
        st.success(t["success"])
        st.dataframe(pd.read_csv("reporte_final.csv"))

if __name__ == "__main__":
    main()
