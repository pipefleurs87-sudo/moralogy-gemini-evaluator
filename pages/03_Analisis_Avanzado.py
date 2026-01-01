import streamlit as st
import sys
import os
from motor_logico import procesar_analisis_avanzado, ge

st.set_page_config(page_title="Analisis Avanzado - Moralogía", layout="wide")

st.title("🔬 Laboratorio de Inferencia Multimodular")

# SECCIÓN 1: CATEGORIZACIÓN (Contexto de la consulta)
categoria = st.selectbox("Seleccione la Categoría de la Consulta", 
                         ["Artistic", "Academic", "Intimate", "Social"])

# SECCIÓN 2: MÓDULOS TÉCNICOS (Discriminación de impacto)
st.subheader("Selección de Módulos de Inferencia")
modulos = st.multiselect(
    "Active los módulos para deducir predicciones y anomalías:",
    ["Biological", "Legal", "Financial", "Systemic", "Social", 
     "Psychological", "Medical", "Environmental", "Marketing", "Math/Engineering"],
    default=["Systemic", "Social"]
)

# SECCIÓN 3: EL CASO
descripcion = st.text_area("Descripción detallada de la interacción:", height=200)

if st.button("Ejecutar Deducción"):
    if descripcion and modulos:
        with st.spinner("Realizando inferencia cruzada..."):
            data = procesar_analisis_avanzado(categoria, modulos, descripcion)
            
            if "error" in data:
                st.error(data["error"])
            else:
                # Visualización de Resultados
                col1, col2, col3 = st.columns(3)
                col1.metric("Riesgo Adversarial", f"{data['adversarial_risk']}%")
                col2.metric("Novedad Genuina", f"{data['originality_score']}%")
                col3.metric("Posición Gradiente", ge.get_gradient(data['agency_score'], data['grace_score']))

                st.divider()
                st.subheader("🧠 Predicciones de la Interacción")
                st.write(data['predictions'])

                with st.expander("Justificación Técnica y Anomalías Detectadas"):
                    st.write(data['justification'])
    else:
        st.warning("Debe seleccionar al menos un módulo y describir el caso.")
