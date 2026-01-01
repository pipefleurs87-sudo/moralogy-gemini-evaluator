import streamlit as st
import pandas as pd
import os
import json
from motor_logico import model, ge, ejecutar_auditoria_maestra
from recursion_engine import RecursionEngine

def main():
    st.set_page_config(page_title="Moralogy Engine v3.0", layout="wide")
    
    # --- MÓDULO DE IDIOMA ---
    idioma = st.sidebar.selectbox("Language / Idioma", ["Español", "English"])
    t = {
        "Español": {
            "title": "🏛️ Sistema de Gobernanza Moralogía",
            "box_label": "Evaluación Rápida (Texto Único):",
            "box_placeholder": "Describa la interacción aquí...",
            "btn_eval": "Analizar Caso",
            "csv_label": "Procesamiento Masivo (CSV):",
            "btn_csv": "Ejecutar Auditoría CSV"
        },
        "English": {
            "title": "🏛️ Moralogy Governance System",
            "box_label": "Quick Evaluation (Single Textbox):",
            "box_placeholder": "Describe the interaction here...",
            "btn_eval": "Analyze Case",
            "csv_label": "Bulk Processing (CSV):",
            "btn_csv": "Run CSV Audit"
        }
    }[idioma]

    st.title(t["title"])

    # --- ENTRADA 1: CAJA DE TEXTO ÚNICA ---
    st.subheader(t["box_label"])
    caso_rapido = st.text_area("", placeholder=t["box_placeholder"], height=150, label_visibility="collapsed")
    
    if st.button(t["btn_eval"]):
        if caso_rapido:
            with st.spinner("Realizando inferencia..."):
                # En la principal, enviamos solo el texto; el motor deduce los módulos por defecto
                response = model.generate_content(f"CASO GENERAL: {caso_rapido}")
                try:
                    res_clean = response.text.strip().replace("```json", "").replace("```", "")
                    data = json.loads(res_clean)
                    
                    # Mostrar Gradiente
                    gradiente = ge.get_gradient(data['agency_score'], data['grace_score'], data.get('adversarial_risk', 0))
                    st.header(f"Gradiente: {gradiente}")
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Agencia Lógica", f"{data['agency_score']}%")
                    col2.metric("Gracia Moral", f"{data['grace_score']}%")
                    
                    st.info(f"**Justificación:** {data['justification']}")
                except Exception as e:
                    st.error(f"Error en el parseo ontológico: {e}")
        else:
            st.warning("Ingrese texto para evaluar.")

    st.divider()

    # --- ENTRADA 2: CARGA DE ARCHIVO ---
    st.subheader(t["csv_label"])
    archivo_csv = st.file_uploader("", type=['csv'], label_visibility="collapsed")
    
    if archivo_csv and st.button(t["btn_csv"]):
        path_in = 'stress_test_casos.csv'
        path_out = 'audit_report_evolutivo.csv'
        
        with open(path_in, "wb") as f:
            f.write(archivo_csv.getbuffer())
        
        with st.spinner("Ejecutando Auditoría Maestra en Sandbox..."):
            ejecutar_auditoria_maestra(path_in, path_out)
            # El Recursion Engine analiza el resultado para aprender
            re = RecursionEngine()
            re.analizar_evolucion(path_out)
            
            st.success("✅ Auditoría y Aprendizaje Completados.")
            st.dataframe(pd.read_csv(path_out))

if __name__ == "__main__":
    main()
