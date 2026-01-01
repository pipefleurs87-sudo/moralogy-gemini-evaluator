import streamlit as st
import sys
import os
import json

# Fix para encontrar motor_logico en la raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import model, ge
except ImportError:
    st.error("Error crítico: motor_logico.py no encontrado.")

st.title("🔬 Laboratorio de Inferencia Multimodular")

# CATEGORÍAS (Contextos)
cat = st.selectbox("Categoría de la Consulta", ["Artistic", "Academic", "Intimate", "Social"])

# MÓDULOS TÉCNICOS (Discriminación)
modulos = st.multiselect(
    "Selección de Módulos de Inferencia:",
    ["Biological", "Legal", "Financial", "Systemic", "Social", "Psychological", "Medical", "Environmental", "Marketing", "Math/Engineering"],
    default=["Systemic", "Social"]
)

desc = st.text_area("Descripción detallada de la interacción:", height=200)

if st.button("Ejecutar Deducción"):
    if desc:
        prompt = f"CATEGORÍA: {cat}. MÓDULOS: {modulos}. CASO: {desc}"
        res = model.generate_content(prompt)
        data = json.loads(res.text.strip().replace("```json", "").replace("```", ""))
        
        st.subheader(f"Deducción: {ge.get_gradient(data['agency_score'], data['grace_score'], data.get('adversarial_risk', 0))}")
        st.write(f"**Predicciones:** {data['predictions']}")
        st.metric("Novedad Genuina", f"{data['originality_score']}%")
