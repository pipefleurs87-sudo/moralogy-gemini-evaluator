import streamlit as st
import os
import sys

# ==================== IMPORTS CRÍTICOS ====================
# Esto resuelve el NameError: 'st' is not defined

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="Moralogy Gemini Evaluator",
    page_icon="🧠", 
    layout="wide"
)

# ==================== ENCABEZADO PRINCIPAL ====================
st.title("🧠 Moralogy Gemini Evaluator")
st.markdown("## Sistema de Evaluación de Dilemas Morales")

# DESCRIPCIÓN RESTAURADA (basada en intención original)
st.markdown("""
Una plataforma integral para analizar, evaluar y comprender respuestas 
a dilemas morales tanto clásicos como contemporáneos.
""")

# ==================== LISTA DE CARACTERÍSTICAS (RESTAURADA) ====================
# Reconstruyendo lo que Gemini corrompió
st.markdown("### 🎯 Características Principales")

features_col1, features_col2 = st.columns(2)

with features_col1:
    st.markdown("""
    - ✅ **Evaluación Sistemática**: Análisis estructurado de respuestas éticas
    - ✅ **Dilemas Clásicos**: Problemas morales fundamentales de la filosofía
    - ✅ **Base Teórica Sólida**: Fundamentos en teorías éticas establecidas
    """)

with features_col2:
    st.markdown("""
    - ✅ **Dilemas Modernos**: Casos contemporáneos de tecnología y sociedad
    - ✅ **Seguimiento de Progreso**: Métricas y análisis de desempeño
    - ✅ **Interfaz Intuitiva**: Navegación simple y accesible
    """)

# ==================== CARGA DEL MOTOR ====================
st.markdown("---")
st.markdown("### 🔧 Estado del Sistema")

try:
    # IMPORTACIÓN CORRECTA (igual que en las páginas)
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
    from motor_logico import MoralogyEngine
    
    engine = MoralogyEngine()
    
    if engine.is_ready():
        st.success("**✅ Motor de Moralogy operativo**")
        
        # Métricas rápidas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Dilemas Totales", engine.total_dilemmas)
        with col2:
            st.metric("Clásicos", engine.get_classical_count())
        with col3:
            st.metric("Modernos", engine.get_modern_count())
    else:
        st.warning("Motor inicializado con limitaciones")
        
except ImportError as e:
    st.error(f"Error crítico: {e}")
    st.info("""
    **Solución:**
    1. Verifica que `motor_logico.py` esté en el mismo directorio
    2. Revisa los permisos del archivo
    3. Ejecuta `pip install -r requirements.txt`
    """)

# ==================== NAVEGACIÓN ====================
st.markdown("---")
st.markdown("### 📂 Navegación Rápida")

# Grid de navegación (BASADO EN LA ESTRUCTURA EXISTENTE)
navigation_options = [
    ("🚀", "Test Drive", "Prueba rápida con dilemas aleatorios", "01_Test_Drive.py"),
    ("🏛️", "Dilemas Clásicos", "Problemas éticos fundamentales", "02_Classical_Dilemmas.py"),
    ("🌐", "Dilemas Modernos", "Casos contemporáneos tecnológicos", "03_Modern_Dilemmas.py"),
    ("📚", "Teoría Moral", "Fundamentos teóricos de ética", "04_Theory.py"),
    ("📊", "Auditoría", "Métricas y análisis del sistema", "05_Complete_Audit.py"),
    ("🔒", "Divine Lock", "Panel de control administrativo", "06_Divine_Lock.py")
]

# Mostrar en grid 3x2
cols = st.columns(3)
for i, (icon, title, description, page) in enumerate(navigation_options):
    with cols[i % 3]:
        with st.container(border=True):
            st.markdown(f"#### {icon} {title}")
            st.caption(description)
            if st.button(f"Ir a {title}", key=f"nav_{i}", use_container_width=True):
                try:
                    st.switch_page(f"pages/{page}")
                except:
                    st.error(f"Error al cargar {page}")

# ==================== INFORMACIÓN ADICIONAL ====================
st.markdown("---")
with st.expander("ℹ️ Acerca de esta aplicación"):
    st.markdown("""
    **Moralogy Gemini Evaluator** es una herramienta diseñada para:
    
    1. **Evaluar respuestas** a dilemas morales complejos
    2. **Analizar patrones** en el razonamiento ético
    3. **Proporcionar retroalimentación** basada en teorías establecidas
    4. **Seguir el progreso** en comprensión de problemas éticos
    
    **Uso académico:** Ideal para cursos de filosofía, ética y toma de decisiones.
    **Uso profesional:** Aplicable en comités de ética, formación corporativa.
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.caption("Moralogy Gemini Evaluator v1.0 • Desarrollado con Streamlit")
