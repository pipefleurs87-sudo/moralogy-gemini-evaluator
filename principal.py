import streamlit as st
import os
import sys
from datetime import datetime

# ============================================
# CONFIGURACIÓN DE PÁGINA - UNA SOLA VEZ
# ============================================
st.set_page_config(
    page_title="Moralogy Gemini Evaluator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator',
        'Report a bug': 'https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator/issues',
        'About': "Moralogy Gemini Evaluator v1.0"
    }
)

# ============================================
# INICIALIZACIÓN DEL SISTEMA
# ============================================

# Título principal
st.title("🧠 Moralogy Gemini Evaluator")
st.markdown("""
### Sistema de Evaluación de Dilemas Morales
Una plataforma para evaluar y analizar respuestas a dilemas morales clásicos y modernos.
""")

# Cargar motor lógico con manejo robusto de errores
engine = None
try:
    # Añadir directorio actual al path para importar
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    
    from motor_logico import MoralogyEngine
    
    # Inicializar motor
    engine = MoralogyEngine()
    
    # Verificar estado
    if hasattr(engine, 'is_ready') and engine.is_ready():
        st.success("✅ **Motor de Moralogy inicializado correctamente**")
        
        # Mostrar estadísticas rápidas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_dilemmas = getattr(engine, 'total_dilemmas', 0)
            st.metric("Dilemas Totales", total_dilemmas)
            
        with col2:
            classical_count = engine.get_classical_count() if hasattr(engine, 'get_classical_count') else 0
            st.metric("Dilemas Clásicos", classical_count)
            
        with col3:
            modern_count = engine.get_modern_count() if hasattr(engine, 'get_modern_count') else 0
            st.metric("Dilemas Modernos", modern_count)
            
        with col4:
            resolution_rate = engine.get_resolution_rate() if hasattr(engine, 'get_resolution_rate') else 0.0
            st.metric("Tasa de Resolución", f"{resolution_rate * 100:.1f}%")
            
    else:
        st.warning("⚠️ **Motor inicializado con advertencias**")
        st.info("Algunas funciones pueden estar limitadas")
        
except ImportError as e:
    st.error(f"❌ **Error crítico de importación**: {e}")
    st.code(f"sys.path: {sys.path}\nCurrent dir: {os.path.dirname(os.path.abspath(__file__))}", language='python')
    
except Exception as e:
    st.error(f"❌ **Error al inicializar el motor**: {str(e)}")
    import traceback
    with st.expander("Detalles técnicos del error"):
        st.code(traceback.format_exc())

# ============================================
# SECCIÓN DE NAVEGACIÓN
# ============================================
st.markdown("---")
st.header("📂 Navegación Principal")

# Definición de todas las páginas/secciones
sections = [
    {
        "icon": "🚀",
        "title": "Test Drive",
        "description": "Prueba rápida con dilemas aleatorios para familiarizarte con el sistema",
        "page": "01_Test_Drive.py",
        "color": "blue"
    },
    {
        "icon": "🏛️",
        "title": "Dilemas Clásicos",
        "description": "Dilemas morales fundamentales de la filosofía tradicional",
        "page": "02_Classical_Dilemmas.py",
        "color": "green"
    },
    {
        "icon": "🌐",
        "title": "Dilemas Modernos",
        "description": "Dilemas éticos contemporáneos de tecnología y sociedad digital",
        "page": "03_Modern_Dilemmas.py",
        "color": "orange"
    },
    {
        "icon": "📚",
        "title": "Teoría Moral",
        "description": "Fundamentos teóricos y sistemas éticos de referencia",
        "page": "04_Theory.py",
        "color": "purple"
    },
    {
        "icon": "📊",
        "title": "Auditoría Completa",
        "description": "Análisis detallado, métricas y estadísticas del sistema",
        "page": "05_Complete_Audit.py",
        "color": "red"
    },
    {
        "icon": "🔒",
        "title": "Divine Lock",
        "description": "Panel de control administrativo y configuración del sistema",
        "page": "06_Divine_Lock.py",
        "color": "gray"
    }
]

# Crear grid de navegación
cols = st.columns(3)
for idx, section in enumerate(sections):
    with cols[idx % 3]:
        # Contenedor estilizado para cada sección
        with st.container(border=True):
            # Encabezado con icono
            st.markdown(f"### {section['icon']} {section['title']}")
            
            # Descripción
            st.write(section['description'])
            
            # Botón de acceso
            if st.button(
                f"Acceder a {section['title']}",
                key=f"nav_btn_{idx}",
                type="secondary",
                use_container_width=True
            ):
                try:
                    st.switch_page(f"pages/{section['page']}")
                except Exception as e:
                    st.error(f"No se pudo cargar {section['page']}: {str(e)}")

# ============================================
# INFORMACIÓN DEL SISTEMA
# ============================================
st.markdown("---")
st.header("ℹ️ Información del Sistema")

if engine is not None:
    # Estado actual del motor
    with st.expander("📈 Estado del Motor en Tiempo Real", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            if hasattr(engine, 'system_stats'):
                stats = engine.system_stats
                st.write("**Estadísticas del Sistema:**")
                for key, value in stats.items():
                    st.text(f"• {key.replace('_', ' ').title()}: {value}")
        
        with col2:
            if hasattr(engine, 'get_system_audit'):
                try:
                    audit = engine.get_system_audit()
                    if audit and 'integrity_checks' in audit:
                        st.write("**Verificaciones de Integridad:**")
                        for check, status in audit['integrity_checks'].items():
                            if status:
                                st.success(f"✓ {check}")
                            else:
                                st.error(f"✗ {check}")
                except:
                    pass
    
    # Métricas de rendimiento
    if hasattr(engine, 'get_response_analytics'):
        try:
            analytics = engine.get_response_analytics()
            if analytics and analytics.get('total_responses', 0) > 0:
                st.metric("📊 Actividad del Sistema", 
                         f"{analytics.get('total_responses', 0)} respuestas registradas",
                         f"Precisión: {analytics.get('accuracy_rate', 0)*100:.1f}%")
        except:
            pass

# ============================================
# INSTRUCCIONES RÁPIDAS
# ============================================
with st.expander("📖 ¿Cómo usar este sistema?", expanded=False):
    st.markdown("""
    1. **Comienza con Test Drive** para familiarizarte con el formato
    2. **Explora Dilemas Clásicos** para fundamentos filosóficos
    3. **Analiza Dilemas Modernos** para problemas contemporáneos
    4. **Consulta la Teoría Moral** para marco conceptual
    5. **Revisa la Auditoría** para métricas y análisis
    6. **Usa Divine Lock** para administración (si es necesario)
    
    **Consejo:** Cada dilema presenta un escenario ético. Analiza todas las opciones antes de responder.
    """)

# ============================================
# FOOTER Y METADATOS
# ============================================
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption(f"**Versión:** {getattr(engine, 'get_version', lambda: '1.0.0')()}")
    
with footer_col2:
    st.caption(f"**Última actualización:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
with footer_col3:
    st.caption("**© 2024** Pipe Fleurs • Moralogy Project")

# ============================================
# VERIFICACIÓN DE ERRORES OCULTOS
# ============================================
try:
    # Verificar que todas las páginas existen
    pages_dir = os.path.join(os.path.dirname(__file__), "pages")
    if os.path.exists(pages_dir):
        available_pages = [f for f in os.listdir(pages_dir) if f.endswith('.py')]
        if len(available_pages) < 6:
            st.sidebar.warning(f"⚠️ Solo {len(available_pages)}/6 páginas encontradas")
except:
    pass  # Silenciar errores en la verificación

# ============================================
# INICIALIZACIÓN COMPLETA
# ============================================
if engine is None:
    st.sidebar.error("❌ Motor no disponible")
    st.sidebar.info("Algunas funciones estarán limitadas hasta que se resuelva el error de importación")
else:
    st.sidebar.success("✅ Sistema operativo")
