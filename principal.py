"""
Moralogy Gemini Evaluator - Principal Application
Main entry point for Streamlit multi-page application
"""

import streamlit as st
from pathlib import Path

# Configure Streamlit page
st.set_page_config(
    page_title="Moralogy Gemini Evaluator",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page content
st.title("🧭 Moralogy Gemini Evaluator")
st.markdown("### Evaluación ética objetiva usando Moralogy Framework + Google Gemini API")

# Introduction
st.markdown("""
Bienvenido al **Moralogy Gemini Evaluator** - una herramienta que combina la comprensión 
del lenguaje natural de Google Gemini con el Framework Moralogy (filosofía moral revisada 
por pares) para proporcionar análisis éticos objetivos y medibles de decisiones de IA.
""")

# Key features
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 🌟 Filosofía Emergente
    Analiza dilemas éticos usando Gemini y el Framework Moralogy para obtener 
    evaluaciones morales fundamentadas.
    """)
    
with col2:
    st.markdown("""
    #### 📊 Cuadros Morales
    Visualiza y compara diferentes escenarios éticos con métricas objetivas 
    de daño y beneficio.
    """)
    
with col3:
    st.markdown("""
    #### 🎯 Escenarios Éticos
    Explora casos pre-definidos como el Problema del Tranvía, vehículos 
    autónomos, y más.
    """)

# Framework explanation
st.markdown("---")
st.markdown("## 🔬 El Framework Moralogy")

st.info("""
**Principios Clave:**
1. **Restricción Negativa**: No causar daño innecesario
2. **Deber Positivo**: Prevenir daño evitable dentro de tu capacidad
3. **Medición Objetiva**: Evaluar daño usando criterios verificables

**Paper**: [DOI: 10.5281/zenodo.18091340](https://doi.org/10.5281/zenodo.18091340)
""")

# Architecture diagram
st.markdown("---")
st.markdown("## 🏗️ Arquitectura del Sistema")

st.code("""
Usuario Ingresa Dilema (lenguaje natural)
    ↓
Gemini API (procesa y comprende escenario)
    ↓
Framework Moralogy (calcula daño objetivo)
    ↓
Gemini API (genera explicación fundamentada)
    ↓
Salida Formateada + Visualización
""", language="text")

# Navigation guide
st.markdown("---")
st.markdown("## 📱 Navegación")

st.markdown("""
Usa el menú lateral para navegar entre las diferentes secciones:

- **Filosofía Emergente**: Análisis interactivo de dilemas éticos
- **Cuadros Morales**: Comparación visual de escenarios
- **Escenarios Éticos**: Casos pre-definidos para explorar

Cada sección está diseñada para diferentes tipos de análisis ético.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>Desarrollado para Google Gemini API Developer Competition 2024</strong></p>
    <p>
        <a href='https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator'>GitHub</a> | 
        <a href='https://doi.org/10.5281/zenodo.18091340'>Paper</a> |
        <a href='https://ergoprotego.substack.com'>Substack</a>
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar info
with st.sidebar:
    st.markdown("### 📚 Recursos")
    st.markdown("""
    - [Framework Paper](https://doi.org/10.5281/zenodo.18091340)
    - [Repositorio GitHub](https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator)
    - [Documentación](https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator/tree/main/docs)
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ Configuración")
    st.info("Asegúrate de tener tu API key de Gemini configurada en el archivo .env")
