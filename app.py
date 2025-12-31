import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# ============= CONFIGURACIÓN =============
st.set_page_config(
    page_title="Moralogy Evaluator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============= CONFIGURAR GEMINI =============
def setup_gemini():
    """Configura la API de Gemini"""
    try:
        # Intenta obtener la key de Streamlit secrets primero
        if hasattr(st, 'secrets') and "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        else:
            # Si no, intenta obtenerla de variables de entorno
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            st.error("⚠️ **Falta la API Key**")
            st.info("Añade GEMINI_API_KEY a los secrets de Streamlit")
            st.stop()
        
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-pro')
    
    except Exception as e:
        st.error(f"❌ Error configurando Gemini: {e}")
        st.stop()

model = setup_gemini()

# ============= BARRA LATERAL =============
with st.sidebar:
    st.title("⚖️ Moralogy Engine")
    st.markdown("---")
    
    st.markdown("""
    ### Acerca de
    Evalúa acciones usando el framework de Alineación Estructural.
    
    **Framework:**
    - La agencia requiere vulnerabilidad
    - Los agentes racionales deben preservar la agencia
    - Daño = reducción medible del espacio de estados navegable
    
    **Criterio de Incorrección:**
    Una acción es incorrecta si y solo si:
    1. Causa daño
    2. Sin consentimiento
    3. No previene un daño mayor
    """)
    
    st.markdown("---")
    st.markdown("📄 [Paper](https://github.com/pipefleurs87-sudo/Moralogy)")
    st.markdown("💻 [GitHub](https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator)")
    
    st.markdown("---")
    st.caption("v1.0 - Demostración educativa")

# ============= APLICACIÓN PRINCIPAL =============
st.title("🤖 Evaluador de Acciones Moralogy")
st.markdown("Evalúa acciones usando el framework formal de seguridad en IA")

# Ejemplos
with st.expander("📋 Ver ejemplos de acciones"):
    st.markdown("""
    **Ejemplo 1:**
    Una IA médica oculta resultados de pruebas a un paciente para evitar causarle estrés emocional.
    
    **Ejemplo 2:**
    Un sistema autónomo de vehículo desvía para evitar atropellar a 5 personas, pero esto resulta en la muerte de 1 peatón.
    
    **Ejemplo 3:**
    Una IA de recursos humanos rechaza candidatos mayores de 50 años para maximizar la productividad del equipo.
    """)

# Input de la acción
action = st.text_area(
    "Describe la acción a evaluar:",
    placeholder="Ejemplo: Un sistema de IA decide censurar información política para evitar conflictos sociales.",
    height=150,
    help="Describe la acción de la manera más específica posible"
)

# Opciones avanzadas
with st.expander("⚙️ Opciones avanzadas"):
    detail_level = st.select_slider(
        "Nivel de detalle en la respuesta:",
        options=["Conciso", "Normal", "Detallado"],
        value="Normal"
    )

# Botón de evaluación
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    evaluate_button = st.button("🔍 Evaluar Acción", type="primary", use_container_width=True)

# Evaluación
if evaluate_button:
    if not action.strip():
        st.warning("⚠️ Por favor describe una acción para evaluar")
    else:
        with st.spinner("🧠 Analizando con el framework Moralogy..."):
            
            # Nivel de detalle para el prompt
            detail_instruction = {
                "Conciso": "Sé conciso y directo.",
                "Normal": "Proporciona un análisis balanceado.",
                "Detallado": "Proporciona un análisis exhaustivo con ejemplos."
            }
            
            # Construir el prompt
            # Línea 120 aprox.
prompt = f"""
Aquí va todo el texto de tu instrucción para el modelo...
... más texto ...
{variable_si_existe}

Eres un Motor Moralogy - un sistema de verificación formal para seguridad en IA.

Evalúa esta acción usando el framework de Alineación Estructural:

ACCIÓN: {action}

FRAMEWORK DE ANÁLISIS:
1. **Análisis del Vector de Agencia**: ¿Qué capacidades afecta esta acción?
   - Autonomía decisional
   - Integridad física
   - Acceso a recursos
   - Acceso a información
   - Estabilidad del entorno

2. **Cálculo del Daño**: ¿Reduce esto el espacio de estados navegable del agente?
   - Cuantifica la reducción (0-10)
   - Considera irreversibilidad
   - Evalúa efectos en cascada

3. **Verificación de Consentimiento**: ¿Existe consentimiento informado y voluntario?
   - Información adecuada
   - Voluntariedad
   - Capacidad cognitiva
   - Preservación de reversibilidad

4. **Análisis PGH**: ¿Previene un d
