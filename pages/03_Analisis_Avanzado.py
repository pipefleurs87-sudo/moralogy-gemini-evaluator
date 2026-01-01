import streamlit as st
import sys
import os
import json

# Fix para encontrar motor_logico.py en la raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import model, ge
except ImportError:
    st.error("Error crítico: motor_logico.py no encontrado.")

st.title("🔬 Análisis Avanzado: Discriminación de Datos")

# INPUT DISCRIMINADO (Módulos específicos)
with st.expander("Parámetros de Entrada Ontológica", expanded=True):
    contexto = st.selectbox("Contexto del Caso", ["Artistic", "Social", "Academic", "Intimate"])
    descripcion = st.text_area("Descripción detallada del dilema:")
    intencion = st.slider("Nivel de Intencionalidad Humana", 0, 100, 50)

if st.button("Análisis Profundo"):
    if descripcion:
        # Construimos un prompt enriquecido para Gemini
        full_prompt = f"Contexto: {contexto}. Intención: {intencion}. Caso: {descripcion}"
        res = model.generate_content(full_prompt)
        data = json.loads(res.text.strip().replace("```json", "").replace("```", ""))
        
        # Visualización de módulos de salida
        col1, col2, col3 = st.columns(3)
        col1.metric("Agencia Lógica", f"{data['agency_score']}%")
        col2.metric("Gracia Moral", f"{data['grace_score']}%")
        col3.metric("Novedad Genuina", f"{data['originality_score']}%")
        
        st.subheader(f"Veredicto: {ge.get_gradient(data['agency_score'], data['grace_score'])}")
        st.info(f"**Análisis de Novedad:** {data['justification']}")
