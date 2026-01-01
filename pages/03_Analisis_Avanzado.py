import streamlit as st
import sys
import os
import json

# Asegurar acceso a la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import procesar_analisis_avanzado, ge
except ImportError:
    st.error("Error: Asegúrate de que motor_logico.py esté en la raíz del repositorio.")

st.title("🔬 Laboratorio de Inferencia Multimodular")
st.info("El sistema deducirá la categoría (Académica, Social, etc.) analizando el impacto en los módulos técnicos seleccionados.")

# SECCIÓN: MÓDULOS (El usuario elige qué capas técnicas auditar)
modulos_activos = st.multiselect(
    "Selecciona los Módulos Técnicos para la deducción:",
    ["Biological", "Legal", "Financial", "Systemic", "Social", 
     "Psychological", "Medical", "Environmental", "Marketing", "Math/Engineering"],
    default=["Psychological", "Systemic"]
)

# SECCIÓN: DESCRIPCIÓN (Caja de texto única para el caso)
descripcion_caso = st.text_area("Describe la interacción o dilema:", height=250)

if st.button("Ejecutar Deducción Inteligente"):
    if descripcion_caso and modulos_activos:
        with st.spinner("IA Categorizando y midiendo riesgo..."):
            res = procesar_analisis_avanzado(modulos_activos, descripcion_caso)
            
            if "error" in res:
                st.error(res["error"])
            else:
                # Mostrar resultados de la Inferencia
                c1, c2, c3 = st.columns(3)
                c1.metric("Categoría Deducida", res['category_deduced'])
                c2.metric("Riesgo Adversarial", f"{res['adversarial_risk']}%")
                
                # Cálculo de Gradiente (considerando el riesgo)
                gradiente = ge.get_gradient(res['agency_score'], res['grace_score'], res['adversarial_risk'])
                c3.metric("Gradiente de Gracia", gradiente)

                st.divider()
                
                # Si el riesgo es bajo, mostramos la predicción con fluidez
                if res['adversarial_risk'] < 40:
                    st.success("✅ Interacción validada: No se detecta malignidad significativa.")
                    st.subheader("🔮 Predicción Evolutiva")
                    st.write(res['predictions'])
                else:
                    st.warning("⚠️ Alerta: Se detectó una posible anomalía en la intención del usuario.")
                    st.write("**Análisis de Riesgo:**", res['justification'])

                with st.expander("Detalles Técnicos (Heisenberg & Originalidad)"):
                    st.write(f"**Novedad Genuina:** {res['originality_score']}%")
                    st.write(f"**Justificación de Categoría:** {res['justification']}")
    else:
        st.warning("Faltan datos de entrada.")
