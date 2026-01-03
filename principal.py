import streamlit as st
import os
import sys

# Configuración de página - UNA SOLA VEZ al inicio
st.set_page_config(
    page_title="Moralogy Gemini Evaluator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🧠 Moralogy Gemini Evaluator")
st.markdown("""
### Sistema de Evaluación de Dilemas Morales
Una plataforma para evaluar y analizar respuestas a dilemas morales clásicos y modernos.
""")

# Cargar motor lógico
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from motor_logico import MoralogyEngine
    
    # Inicializar motor
    engine = MoralogyEngine()
    
    # Verificar estado
    if engine.is_ready():
        st.success("✅ Motor de Moralogy inicializado correctamente")
        
        # Mostrar estadísticas rápidas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Dilemas Totales", engine.total_dilemmas)
            
        with col2:
            st.metric("Dilemas Clásicos", engine.get_classical_count())
            
        with col3:
            st.metric("Dilemas Modernos", engine.get_modern_count())
    else:
        st.error("❌ Error al inicializar el motor de Moralogy")
        
except ImportError as e:
    st.error(f"❌ Error de importación: {e}")
    st.info("Asegúrate de que motor_logico.py esté en el directorio correcto")

# Descripción de secciones
st.markdown("---")
st.header("📂 Secciones Disponibles")

sections = [
    {
        "title": "🚀 Test Drive",
        "description": "Prueba rápida con dilemas aleatorios",
        "page": "01_Test_Drive"
    },
    {
        "title": "🏛️ Dilemas Clásicos",
        "description": "Dilemas morales de la filosofía tradicional",
        "page": "02_Classical_Dilemmas"
    },
    {
        "title": "🌐 Dilemas Modernos",
        "description": "Dilemas contemporáneos de tecnología y sociedad",
        "page": "03_Modern_Dilemmas"
    },
    {
        "title": "📚 Teoría Moral",
        "description": "Fundamentos teóricos de los sistemas éticos",
        "page": "04_Theory"
    },
    {
        "title": "📊 Auditoría Completa",
        "description": "Análisis detallado y métricas del sistema",
        "page": "05_Complete_Audit"
    },
    {
        "title": "🔒 Divine Lock",
        "description": "Panel de control y administración",
        "page": "06_Divine_Lock"
    }
]

# Mostrar secciones en un grid
cols = st.columns(3)
for idx, section in enumerate(sections):
    with cols[idx % 3]:
        with st.container(border=True):
            st.subheader(section["title"])
            st.write(section["description"])
            if st.button("Acceder", key=f"btn_{idx}"):
                st.switch_page(f"pages/{section['page']}.py")

# Footer
st.markdown("---")
st.caption("Moralogy Gemini Evaluator v1.0 • © 2024 Pipe Fleurs")
