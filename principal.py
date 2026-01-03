"""
Moralogy Gemini Evaluator - Aplicación Principal
Evaluación ética objetiva usando Moralogy Framework + Google Gemini API
"""

import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Moralogy Gemini Evaluator",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🧭 Moralogy Gemini Evaluator")
st.markdown("### Evaluación Ética Objetiva usando IA")

# Introducción
st.markdown("""
Bienvenido al **Moralogy Gemini Evaluator** - una herramienta que combina la comprensión 
del lenguaje natural de Google Gemini con el Framework Moralogy (filosofía moral revisada 
por pares) para proporcionar análisis éticos objetivos y medibles.
""")

# Características principales
st.markdown("---")
st.subheader("✨ Características")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🌟 Filosofía Emergente")
    st.write("Análisis interactivo de dilemas éticos usando Gemini API")

with col2:
    st.markdown("#### 📊 Cuadros Morales")
    st.write("Visualización comparativa de escenarios éticos")

with col3:
    st.markdown("#### 🎯 Escenarios Éticos")
    st.write("Explora casos pre-definidos clásicos")

# Framework Moralogy
st.markdown("---")
st.subheader("🔬 El Framework Moralogy")

st.info("""
**Principios Clave:**
1. **Restricción Negativa**: No causar daño innecesario
2. **Deber Positivo**: Prevenir daño evitable dentro de tu capacidad
3. **Medición Objetiva**: Evaluar daño usando criterios verificables

**Paper**: [DOI: 10.5281/zenodo.18091340](https://doi.org/10.5281/zenodo.18091340)
""")

# Arquitectura
st.markdown("---")
st.subheader("🏗️ Arquitectura")

st.code("""
Usuario ingresa dilema (lenguaje natural)
    ↓
Gemini API (procesa escenario)
    ↓
Framework Moralogy (calcula daño)
    ↓
Gemini API (genera explicación)
    ↓
Resultado formateado + visualización
""", language="text")

# Navegación
st.markdown("---")
st.subheader("📱 Navegación")

st.markdown("""
Usa el **menú lateral** (←) para navegar entre secciones:

- 🌟 **Filosofía Emergente**: Análisis interactivo de dilemas
- 📊 **Cuadros Morales**: Comparación visual de escenarios  
- 🎯 **Escenarios Éticos**: Casos pre-definidos para explorar

Cada sección ofrece diferentes perspectivas de análisis ético.
""")

# Información adicional
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>Desarrollado para Google Gemini API Developer Competition 2024</strong></p>
    <p>
        <a href='https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator' target='_blank'>GitHub</a> | 
        <a href='https://doi.org/10.5281/zenodo.18091340' target='_blank'>Paper</a>
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📚 Recursos")
    st.markdown("""
    - [Framework Paper](https://doi.org/10.5281/zenodo.18091340)
    - [GitHub Repo](https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator)
    - [Documentación](https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator/tree/main/docs)
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ Estado")
    st.success("✅ Sistema operativo")
    st.info("💡 Configura tu API key de Gemini en .env")
