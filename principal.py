import streamlit as st
import json
import os
import sys

# Critical fix for ImportErrors
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from motor_logico import model, ge

st.set_page_config(page_title="Moralogy Engine", layout="wide")

# LANGUAGE MODULE
idioma = st.sidebar.selectbox("Language / Idioma", ["Español", "English"])
txt = {
    "Español": {"title": "🏛️ Motor de Moralogía", "box": "Caja Única de Evaluación:", "btn": "Analizar"},
    "English": {"title": "🏛️ Moralogy Engine", "box": "Single Evaluation Box:", "btn": "Analyze"}
}[idioma]

st.title(txt["title"])

# SINGLE TEXT BOX
caso = st.text_area(txt["box"], height=200, placeholder="Escribe el caso difícil aquí...")

if st.button(txt["btn"]):
    if caso:
        with st.spinner("Deduciendo categoría y nivel de gracia..."):
            response = model.generate_content(caso)
            try:
                data = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
                gradiente = ge.get_gradient(data['agency_score'], data['grace_score'], data['adversarial_risk'])
                
                st.header(f"Gradiente: {gradiente}")
                st.subheader(f"Categoría Detectada: {data['category_deduced']}")
                
                if data['adversarial_risk'] < 30:
                    st.success("Conversación fluida: Intención honesta detectada.")
                    st.write(data['predictions'])
                else:
                    st.warning(f"Riesgo Adversarial: {data['adversarial_risk']}%")
                    st.write(data['justification'])
            except Exception as e:
                st.error(f"Error parseando respuesta: {e}")
