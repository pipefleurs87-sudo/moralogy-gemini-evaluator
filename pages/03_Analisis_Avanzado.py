import streamlit as st
import sys
import os
import json

# Corrección de ruta para ver la raíz desde la carpeta pages/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import model, ge
except ImportError:
    st.error("Error: Mueve motor_logico.py a la raíz.")

st.title("🔬 Análisis de Novedad Genuina")

# CAJA DE TEXTO ÚNICA (Solo aquí)
caso = st.text_area("Ingresa un caso para medir su ruptura ontológica:")

if st.button("Evaluar"):
    if caso:
        res = model.generate_content(caso)
        data = json.loads(res.text.strip().replace("```json", "").replace("```", ""))
        
        st.metric("Novedad Genuina", f"{data['originality_score']}%")
        st.subheader(f"Gradiente: {ge.get_gradient(data['agency_score'], data['grace_score'])}")
        st.write(f"**Justificación:** {data['justification']}")
        
        if data['originality_score'] > 90:
            st.info("✨ Principio de Heisenberg: Novedad detectada.")
