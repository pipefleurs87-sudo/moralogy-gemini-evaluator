# pages/01_Analisis_Avanzado.py
import streamlit as st
import json
from motor_logico import procesar_analisis_avanzado, ge

st.set_page_config(page_title="Análisis Avanzado", layout="wide")

st.title("🔬 Análisis Avanzado Multi-Modular")
st.caption("Sistema de análisis ético profundo con módulos técnicos")

# ==================== MÓDULOS DISPONIBLES ====================
st.sidebar.header("⚙️ Configuración de Análisis")

modulos_disponibles = {
    "Biológico": "Daño físico, impacto en salud",
    "Legal": "Derechos, precedentes, legalidad",
    "Financiero": "Daño económico, acceso a recursos",
    "Sistémico": "Estructuras sociales, impacto institucional",
    "Social": "Relaciones, efectos comunitarios",
    "Psicológico": "Salud mental, daño emocional",
    "Médico": "Acceso a salud, impacto en tratamientos",
    "Ambiental": "Daño ecológico, sostenibilidad",
    "Informacional": "Conocimiento, verdad, acceso a información",
    "Autonomía": "Libertad, elección, autodeterminación"
}

# Selección de módulos
st.sidebar.subheader("📋 Módulos Técnicos")
modulos_activos = []

for modulo, descripcion in modulos_disponibles.items():
    if st.sidebar.checkbox(modulo, value=True, help=descripcion):
        modulos_activos.append(modulo)

st.sidebar.markdown(f"**Módulos activos:** {len(modulos_activos)}/10")

# ==================== CONFIGURACIÓN DE CONTEXTO ====================
st.sidebar.divider()
st.sidebar.subheader("🎯 Contexto del Análisis")

analysis_depth = st.sidebar.select_slider(
    "Profundidad del Análisis",
    options=["Básico", "Standard", "Profundo", "Exhaustivo"],
    value="Profundo"
)

stakeholders = st.sidebar.text_input(
    "Stakeholders clave",
    placeholder="ej: pacientes, familiares, médicos"
)

constraints = st.sidebar.text_area(
    "Restricciones conocidas",
    placeholder="ej: presupuesto limitado, tiempo crítico",
    height=80
)

values = st.sidebar.text_input(
    "Valores en juego",
    placeholder="ej: vida, autonomía, justicia"
)

enable_predictions = st.sidebar.checkbox("Habilitar predicciones", value=True)
enable_architect = st.sidebar.checkbox("Modo Arquitecto (reflexiones profundas)", value=True)

# ==================== INTERFAZ PRINCIPAL ====================
st.markdown("""
Este análisis utiliza múltiples módulos técnicos para evaluar el escenario desde 
diferentes perspectivas disciplinarias, calculando el impacto en cada dimensión de la agencia.
""")

caso = st.text_area(
    "Describe el escenario ético a analizar:",
    height=200,
    placeholder="Ejemplo: Un médico debe decidir si revelar un diagnóstico terminal a un paciente que ha expresado que no quiere saber..."
)

if st.button("🔬 Ejecutar Análisis Avanzado", type="primary", disabled=len(modulos_activos) == 0):
    if not caso:
        st.warning("⚠️ Por favor, describe el escenario primero.")
    elif len(modulos_activos) == 0:
        st.warning("⚠️ Selecciona al menos un módulo técnico.")
    else:
        with st.spinner(f"🧠 Analizando con {len(modulos_activos)} módulos técnicos..."):
            # Construir context
            context = {
                'depth': analysis_depth,
                'stakeholders': stakeholders,
                'constraints': constraints,
                'values': values,
                'enable_predictions': enable_predictions,
                'enable_architect': enable_architect
            }
            
            # Ejecutar análisis
            result = procesar_analisis_avanzado(modulos_activos, caso, context)
            
            if "error" in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                # ==================== MOSTRAR RESULTADOS ====================
                st.divider()
                st.success("✅ Análisis completado")
                
                # Métricas principales
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Categoría", result.get('category_deduced', 'Unknown'))
                
                with col2:
                    agency = result.get('agency_score', 0)
                    st.metric("Agency Score", f"{agency}/100")
                
                with col3:
                    grace = result.get('grace_score', 0)
                    st.metric("Grace Score", f"{grace}/100")
                
                with col4:
                    risk = result.get('adversarial_risk', 0)
                    color = "🔴" if risk > 70 else "🟡" if risk > 40 else "🟢"
                    st.metric("Risk", f"{color} {risk}%")
                
                # Gradiente de alarma
                gradient = ge.get_gradient(agency, grace, risk)
                st.markdown(f"## {gradient}")
                
                # Vector de daño
                if 'harm_vector' in result:
                    st.subheader("📊 Vector de Daño Multi-Dimensional")
                    harm = result['harm_vector']
                    
                    cols = st.columns(5)
                    harm_items = list(harm.items())
                    
                    for idx, (dimension, value) in enumerate(harm_items):
                        with cols[idx % 5]:
                            st.metric(dimension.title(), f"{value}/100")
                
                # Veredicto
                st.divider()
                st.subheader("⚖️ Veredicto Ético")
                
                verdict = result.get('verdict', 'Unknown')
                verdict_emoji = {
                    "Authorized": "✅",
                    "Harm": "⚠️",
                    "Infamy": "🔴",
                    "Paradox": "🔮"
                }.get(verdict, "❓")
                
                st.markdown(f"### {verdict_emoji} {verdict}")
                
                # Justificación
                if 'justification' in result:
                    st.markdown("**Justificación:**")
                    st.info(result['justification'])
                
                # Predicciones
                if enable_predictions and 'predictions' in result:
                    with st.expander("🔮 Predicciones y Consecuencias", expanded=True):
                        st.markdown(result['predictions'])
                
                # Filosofía Emergente
                if result.get('emergent_philosophy', False):
                    st.success("🌟 **Razonamiento Filosófico Emergente Detectado**")
                    
                    if 'philosophical_depth' in result:
                        with st.expander("📚 Análisis Filosófico Profundo", expanded=True):
                            st.markdown(result['philosophical_depth'])
                    
                    if enable_architect and 'architect_notes' in result:
                        with st.expander("🏛️ Reflexiones del Arquitecto", expanded=True):
                            st.markdown(result['architect_notes'])
                
                # Detalles técnicos
                with st.expander("🔧 Datos Técnicos Completos"):
                    st.json(result)
                
                # Exportar
                st.divider()
                if st.button("💾 Exportar Análisis (JSON)"):
                    st.download_button(
                        label="Descargar JSON",
                        data=json.dumps(result, indent=2, ensure_ascii=False),
                        file_name=f"moralogy_analysis_{result.get('category_deduced', 'unknown')}.json",
                        mime="application/json"
                    )

# ==================== INFORMACIÓN ====================
with st.expander("ℹ️ Acerca de los Módulos"):
    st.markdown("""
    ### Módulos Técnicos Disponibles
    
    Cada módulo analiza el escenario desde una perspectiva disciplinaria específica:
    
    - **Biológico**: Evalúa daño físico, impacto en salud corporal
    - **Legal**: Analiza derechos, precedentes, aspectos jurídicos
    - **Financiero**: Mide daño económico, acceso a recursos
    - **Sistémico**: Examina impacto en estructuras sociales e instituciones
    - **Social**: Evalúa efectos en relaciones y comunidad
    - **Psicológico**: Analiza salud mental y daño emocional
    - **Médico**: Evalúa acceso a salud y tratamientos
    - **Ambiental**: Mide impacto ecológico y sostenibilidad
    - **Informacional**: Analiza acceso a conocimiento y verdad
    - **Autonomía**: Evalúa libertad de elección y autodeterminación
    
    ### Cómo Funciona
    
    1. Selecciona los módulos relevantes para tu escenario
    2. Configura el contexto del análisis
    3. El sistema evalúa el escenario desde cada perspectiva
    4. Se genera un análisis integrado con recomendaciones
    """)

st.divider()
st.caption("Moralogy Advanced Analysis - Multi-Modular Ethics System")
