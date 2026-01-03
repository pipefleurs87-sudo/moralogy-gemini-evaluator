import streamlit as st
import os
import sys

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="Moralogy Gemini Evaluator",
    page_icon="🧠", 
    layout="wide"
)

# ==================== ENCABEZADO PRINCIPAL ====================
st.title("🧠 Moralogy Gemini Evaluator")
st.markdown("## Sistema de Evaluación de Dilemas Morales")

st.markdown("""
Una plataforma integral para analizar, evaluar y comprender respuestas 
a dilemas morales tanto clásicos como contemporáneos.
""")

# ==================== LISTA DE CARACTERÍSTICAS ====================
st.markdown("### 🎯 Características Principales")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    - ✅ **Evaluación Sistemática**: Análisis estructurado de respuestas éticas
    - ✅ **Dilemas Clásicos**: Problemas morales fundamentales de la filosofía
    - ✅ **Base Teórica Sólida**: Fundamentos en teorías éticas establecidas
    """)

with col2:
    st.markdown("""
    - ✅ **Dilemas Modernos**: Casos contemporáneos de tecnología y sociedad
    - ✅ **Seguimiento de Progreso**: Métricas y análisis de desempeño
    - ✅ **Interfaz Intuitiva**: Navegación simple y accesible
    """)

# ==================== INTENTO DE CARGA DEL MOTOR ====================
st.markdown("---")
st.markdown("### 🔧 Estado del Sistema")

engine = None
engine_status = "❌ No inicializado"

try:
    # DEBUG: Mostrar path actual
    st.sidebar.code(f"Current dir: {os.getcwd()}")
    st.sidebar.code(f"File location: {__file__}")
    
    # IMPORTACIÓN SEGURA - intentar múltiples estrategias
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Estrategia 1: Import directo
    try:
        from motor_logico import MoralogyEngine
        engine = MoralogyEngine()
        engine_status = "✅ Motor cargado (vía import directo)"
    except ImportError as e1:
        st.sidebar.warning(f"Import directo falló: {e1}")
        
        # Estrategia 2: Añadir al path
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        from motor_logico import MoralogyEngine
        engine = MoralogyEngine()
        engine_status = "✅ Motor cargado (vía sys.path)"
        
except Exception as e:
    error_msg = str(e)
    engine_status = f"❌ Error: {error_msg[:100]}..."
    
    # Mostrar error detallado en sidebar
    with st.sidebar.expander("🔍 Detalles del error", expanded=True):
        st.error(f"**Tipo de error:** {type(e).__name__}")
        st.code(f"Error completo: {error_msg}")
        
        # Diagnóstico del circular import
        if "circular import" in error_msg.lower() or "partially initialized" in error_msg.lower():
            st.warning("**PROBLEMA IDENTIFICADO:** Import circular")
            st.info("""
            **Solución necesaria:**
            1. Revisar `motor_logico.py` por imports circulares
            2. Verificar si importa algo de sí mismo
            3. Revisar la función `procesar_analisis_completo`
            """)
        
        # Listar contenido del directorio
        st.write("**Archivos en directorio:**")
        files = os.listdir(current_dir if 'current_dir' in locals() else '.')
        for f in files:
            st.text(f"• {f}")

# Mostrar estado
st.info(f"**Estado:** {engine_status}")

# Solo mostrar métricas si el motor se cargó
if engine is not None and hasattr(engine, 'is_ready') and engine.is_ready():
    st.success("**✅ Motor de Moralogy operativo**")
    
    # Métricas rápidas
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        if hasattr(engine, 'total_dilemmas'):
            st.metric("Dilemas Totales", engine.total_dilemmas)
        else:
            st.metric("Dilemas Totales", "N/A")
            
    with metric_col2:
        if hasattr(engine, 'get_classical_count'):
            st.metric("Clásicos", engine.get_classical_count())
        else:
            st.metric("Clásicos", "N/A")
            
    with metric_col3:
        if hasattr(engine, 'get_modern_count'):
            st.metric("Modernos", engine.get_modern_count())
        else:
            st.metric("Modernos", "N/A")
else:
    st.warning("**⚠️ Funcionalidad limitada** - Algunas características no estarán disponibles")
    
    # Métricas de respaldo
    backup_col1, backup_col2, backup_col3 = st.columns(3)
    with backup_col1:
        st.metric("Dilemas Totales", "0")
    with backup_col2:
        st.metric("Clásicos", "0")
    with backup_col3:
        st.metric("Modernos", "0")

# ==================== NAVEGACIÓN (SIEMPRE DISPONIBLE) ====================
st.markdown("---")
st.markdown("### 📂 Navegación Rápida")

# Las páginas deberían funcionar independientemente
navigation_options = [
    ("🚀", "Test Drive", "Prueba rápida con dilemas aleatorios", "01_Test_Drive.py"),
    ("🏛️", "Dilemas Clásicos", "Problemas éticos fundamentales", "02_Classical_Dilemmas.py"),
    ("🌐", "Dilemas Modernos", "Casos contemporáneos tecnológicos", "03_Modern_Dilemmas.py"),
    ("📚", "Teoría Moral", "Fundamentos teóricos de ética", "04_Theory.py"),
    ("📊", "Auditoría", "Métricas y análisis del sistema", "05_Complete_Audit.py"),
    ("🔒", "Divine Lock", "Panel de control administrativo", "06_Divine_Lock.py")
]

# Mostrar en grid 3x2
nav_cols = st.columns(3)
for i, (icon, title, description, page) in enumerate(navigation_options):
    with nav_cols[i % 3]:
        with st.container(border=True):
            st.markdown(f"#### {icon} {title}")
            st.caption(description)
            
            # Verificar si la página existe
            page_path = os.path.join("pages", page)
            page_exists = os.path.exists(page_path)
            
            if page_exists:
                if st.button(f"Ir a {title}", key=f"nav_{i}", use_container_width=True):
                    try:
                        st.switch_page(f"pages/{page}")
                    except Exception as nav_error:
                        st.error(f"Error de navegación: {str(nav_error)[:50]}")
            else:
                st.error(f"⚠️ {page} no encontrado")
                st.caption(f"Ruta: {page_path}")

# ==================== DIAGNÓSTICO ====================
with st.sidebar.expander("🛠️ Diagnóstico del Sistema", expanded=True):
    st.write("**Problemas identificados:**")
    st.error("1. Circular import en motor_logico.py")
    st.error("2. Función 'procesar_analisis_completo' no encontrada")
    
    st.write("**Acciones recomendadas:**")
    st.info("""
    1. **Revisar motor_logico.py** por imports circulares
    2. **Verificar** si hay `from motor_logico import algo` dentro del mismo archivo
    3. **Comprobar** que exista `procesar_analisis_completo()` o renombrarla
    """)
    
    # Botón para ver motor_logico.py
    if st.button("📄 Ver contenido de motor_logico.py"):
        try:
            with open("motor_logico.py", "r") as f:
                content = f.read()
                st.code(content[:2000], language="python")
                if len(content) > 2000:
                    st.caption(f"... ({len(content)-2000} caracteres más)")
        except Exception as e:
            st.error(f"No se pudo leer motor_logico.py: {e}")

# ==================== FOOTER ====================
st.markdown("---")
st.caption("Moralogy Gemini Evaluator • Modo de recuperación • Revirtiendo cambios de Gemini")
