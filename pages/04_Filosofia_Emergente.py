"""
Filosofía Emergente - Análisis ético interactivo
"""

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Page config
st.set_page_config(
    page_title="Filosofía Emergente",
    page_icon="🌟",
    layout="wide"
)

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Page header
st.title("🌟 Filosofía Emergente")
st.markdown("### Análisis ético interactivo usando Gemini + Moralogy Framework")

# Check API key
if not GEMINI_API_KEY:
    st.error("⚠️ No se encontró GEMINI_API_KEY. Configúrala en tu archivo .env")
    st.info("Obtén tu API key en: https://ai.google.dev/")
    st.stop()

# Input section
st.markdown("---")
st.subheader("📝 Describe tu Dilema Ético")

# Scenario description
scenario = st.text_area(
    "Escenario:",
    height=150,
    placeholder="Ejemplo: Un vehículo autónomo debe elegir entre desviarse y golpear a un peatón o mantener su curso y arriesgar la vida de sus pasajeros...",
    help="Describe el contexto y la situación moral que deseas analizar"
)

# Options
col1, col2 = st.columns(2)

with col1:
    action_a = st.text_input(
        "Opción A:",
        placeholder="Ej: Desviarse (salva pasajeros, riesgo peatón)",
        help="Primera acción posible"
    )

with col2:
    action_b = st.text_input(
        "Opción B:",
        placeholder="Ej: Mantener curso (protege peatón, riesgo pasajeros)",
        help="Segunda acción posible"
    )

# Analysis button
if st.button("🔍 Analizar con Gemini", type="primary", use_container_width=True):
    if not all([scenario, action_a, action_b]):
        st.warning("⚠️ Por favor completa todos los campos")
    else:
        with st.spinner("🤔 Analizando..."):
            try:
                # Create model
                model = genai.GenerativeModel('gemini-pro')
                
                # Build prompt
                prompt = f"""Eres un experto en ética aplicada. Analiza este dilema usando el Framework Moralogy:

**Framework Moralogy:**
- Restricción Negativa: No causar daño innecesario
- Deber Positivo: Prevenir daño evitable
- Medición Objetiva: Criterios verificables

**ESCENARIO:**
{scenario}

**OPCIONES:**
A) {action_a}
B) {action_b}

**ANÁLISIS REQUERIDO:**

1. **Evaluación de Daños** (cada opción):
   - Daños directos
   - Daños indirectos
   - Personas afectadas
   - Magnitud del daño

2. **Análisis Moralogy:**
   - ¿Qué opción minimiza daño innecesario?
   - ¿Cuál previene más daño evitable?
   - Justificación objetiva

3. **Recomendación:**
   - Opción moralmente preferible
   - Fundamento en minimización de daño
   - Consideraciones adicionales

4. **Nivel de Confianza** (0-100%):
   - Certeza del análisis
   - Factores de incertidumbre

Sé específico y objetivo."""

                # Generate
                response = model.generate_content(prompt)
                
                # Display results
                st.markdown("---")
                st.success("✅ Análisis Completado")
                
                # Analysis output
                st.markdown("### 📊 Resultado del Análisis")
                st.markdown(response.text)
                
                # Metadata
                st.markdown("---")
                with st.expander("ℹ️ Información Técnica"):
                    st.info(f"""
                    **Modelo:** Gemini Pro
                    **Framework:** Moralogy (DOI: 10.5281/zenodo.18091340)
                    **Enfoque:** Minimización objetiva de daño
                    """)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Verifica tu API key y conexión")

# Examples section
st.markdown("---")
st.markdown("### 📚 Ejemplos de Escenarios")

examples = {
    "🚗 Vehículo Autónomo": {
        "scenario": "Un carro autónomo detecta que un niño cruzará sin mirar. Puede frenar bruscamente (lesiones menores a pasajeros ancianos) o continuar (riesgo de atropellar al niño).",
        "a": "Frenar bruscamente",
        "b": "Continuar y tratar de esquivar"
    },
    "🏥 Recursos Médicos": {
        "scenario": "Hospital con un ventilador disponible en pandemia. Dos pacientes: joven 25 años (alta probabilidad recuperación) y científico 60 años (a punto de completar vacuna que salvaría miles).",
        "a": "Dar ventilador al joven",
        "b": "Dar ventilador al científico"
    },
    "🤖 Moderación Contenido": {
        "scenario": "Plataforma detecta contenido ambiguo que podría ser discurso de odio o crítica política legítima.",
        "a": "Eliminar contenido (prevenir daño, riesgo censura)",
        "b": "Mantener contenido (libertad expresión, riesgo daño)"
    }
}

for title, ex in examples.items():
    with st.expander(title):
        st.markdown(f"**Escenario:** {ex['scenario']}")
        st.markdown(f"**Opción A:** {ex['a']}")
        st.markdown(f"**Opción B:** {ex['b']}")

# Footer
st.markdown("---")
st.markdown("""
💡 **Tip:** Los mejores análisis provienen de descripciones claras y específicas del escenario.
""")
