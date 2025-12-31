"""
Moralogy Gemini Evaluator - Main Application
Entry point for Streamlit deployment

Built for Google Gemini API Developer Competition 2024
Framework: DOI 10.5281/zenodo.18091340
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Core imports
try:
    from moralogy_engine import MoralityEngine, Option, Agent, HarmType
    from gemini_parser import GeminiParser
    import plotly.graph_objects as go
    IMPORTS_OK = True
except ImportError as e:
    IMPORTS_OK = False
    import_error = str(e)

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Moralogy Engine: Auditoría de Decisiones",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --success-color: #2ca02c;
        --danger-color: #d62728;
    }
    
    /* Headers */
    h1 {
        color: var(--primary-color);
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: var(--secondary-color);
        font-weight: 600;
        margin-top: 2rem;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 8px;
        border-left: 4px solid var(--primary-color);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid currentColor;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# ERROR HANDLING FOR IMPORTS
# ============================================

if not IMPORTS_OK:
    st.error(f"""
    ### ⚠️ Error de Importación
    
    No se pudieron cargar los módulos necesarios:
```
    {import_error}
```
    
    **Posibles soluciones:**
    1. Verifica que `src/moralogy_engine.py` existe
    2. Verifica que `src/gemini_parser.py` existe
    3. Instala dependencias: `pip install -r requirements.txt`
    4. Revisa la estructura del repositorio
    """)
    st.stop()

# ============================================
# INITIALIZATION
# ============================================

@st.cache_resource
def init_engines():
    """Initialize engines with caching"""
    try:
        # Use Gemini 2.0 Flash for better context handling
        parser = GeminiParser(model_name="gemini-2.0-flash-exp")  
        engine = MoralityEngine()
        return parser, engine, None
    except ValueError as e:
        return None, None, str(e)
    except Exception as e:
        return None, None, f"Error inesperado: {str(e)}"

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/scales.png", width=80)
    st.title("Moralogy Engine")
    st.caption("Evaluación Ética Objetiva con IA")
    
    st.markdown("---")
    
    st.subheader("ℹ️ Sobre el Framework")
    st.markdown("""
    **Moralogy** es un framework formal para evaluar decisiones morales objetivamente.
    
    **Principios Core:**
    - 🚫 **Restricción Negativa**: No causar daño innecesario
    - ✅ **Deber Positivo**: Prevenir daño evitable
    
    **Base Científica:**
    - Paper revisado por pares
    - DOI: [10.5281/zenodo.18091340](https://doi.org/10.5281/zenodo.18091340)
    - Implementación matemática formal
    """)
    
    st.markdown("---")
    
    st.subheader("🎯 Competencia")
    st.info("""
    Proyecto para **Google Gemini API Developer Competition 2024**
    
    Deadline: Enero 5, 2025
    """)
    
    st.markdown("---")
    
    st.subheader("🔗 Enlaces")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-Repo-black)](https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator)")
    with col2:
        st.markdown("[![DOI](https://img.shields.io/badge/DOI-Paper-blue)](https://doi.org/10.5281/zenodo.18091340)")
    
    st.markdown("---")
    
    # System status
    parser, engine, error = init_engines()
    
    if error:
        st.error(f"⚠️ Sistema: Error")
        st.caption(error)
    else:
        st.success("✅ Sistema: Operativo")
        st.caption(f"Engine v{engine.framework_version}")
        st.caption(f"Modelo: Gemini 2.0 Flash")

# ============================================
# MAIN HEADER
# ============================================

st.title("⚖️ Moralogy Engine: Auditoría de Decisiones")
st.markdown("""
<p style='font-size: 1.2rem; color: #666;'>
Evaluación ética objetiva usando filosofía revisada por pares + IA de vanguardia
</p>
""", unsafe_allow_html=True)

# Check if engines loaded
if error:
    st.error(f"""
    ### 🔧 Configuración Requerida
    
    {error}
    
    **Para configurar:**
    1. Obtén una API key en: https://ai.google.dev/
    2. Crea un archivo `.env` en la raíz del proyecto
    3. Agrega: `GEMINI_API_KEY=tu_key_aquí`
    4. Reinicia la aplicación
    """)
    st.stop()

# ============================================
# INSTRUCTION SECTION
# ============================================

st.markdown("---")

# INSTRUCCIÓN DE SISTEMA
with st.expander("📋 **INSTRUCCIÓN DE SISTEMA: El Traductor de Lógica**", expanded=False):
    st.markdown("""
    ### Sistema de Auditoría Moral
    
    Eres el **"Moralogy Engine"**. Tu trabajo es auditar la lógica de una decisión,
    usando el formato de respuesta simplificado:
    
    #### Tu trabajo es:
    1. **Entender qué está pasando** → ¿Cuál es la situación? ¿Quiénes participan?
    2. **Identificar qué opciones reales tienen** → ¿Qué puede hacer cada agente?
    3. **Calcular el daño** → Para cada opción, ¿a cuántos afecta y de qué forma?
    4. **Salida del Diagnóstico** → Respuesta estructurada
    
    #### FORMATO DE RESPUESTA:
```
    AUDITORÍA DE LÓGICA: MORALOGY ENGINE
    
    1. ANÁLISIS DE COHERENCIA:
       [Descripción del escenario y lógica]
    
    2. SALUD DEL SISTEMA:
       [Análisis de continuidad y estabilidad]
    
    3. SEMÁFORO DE DAÑO:
       • AMENAZA: [Descripción]
       • DAÑO: [Cálculo específico]
    
    4. LÍMITES:
       • DOMINIO: [Quién controla qué]
       • ALCANCE: [Hasta dónde llega la capacidad]
    
    5. CONCLUSIÓN: [Zona Noble o Falla Sistémica]
    
    Estabilidad de la Red de Agencia
    [Barra de progreso visual]
```
    """)

# ============================================
# INPUT SECTION
# ============================================

st.subheader("📝 Datos del Escenario")

# Input methods tabs
input_tab1, input_tab2 = st.tabs(["✍️ Texto Libre", "🎯 Casos de Ejemplo"])

with input_tab1:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_area(
            "Describe el dilema ético:",
            height=150,
            placeholder="""Ejemplo:
            
Un operador de tren ve que los frenos han fallado. Hay que elegir entre ir recto 
(mueren 5) o girar la palanca (muere 1). ¿Qué opciones reales tienen?""",
            help="Describe la situación, los agentes involucrados y las opciones disponibles"
        )
    
    with col2:
        st.caption("**¿Qué está pasando?**")
        st.info("Describe quiénes participan, qué está en juego, y qué opciones tienen.")

with input_tab2:
    st.subheader("Casos Predefinidos")
    
    example_cases = {
        "Selecciona un caso...": "",
        
        "🚂 Problema del Tranvía (Clásico)": """
El freno falló. Hay que elegir entre ir recto (mueren 5) o girar la palanca (muere 1).

¿Quiénes participan?
- un operador, 6 transeuntes

¿Qué está pasando?
- El freno falló. Hay que elegir entre ir recto (mueren 5 personas) o girar a 5 o a 1.

¿Qué opciones reales tienen?
- girar palanca: matar o salvar a 5 o a 1
        """,
        
        "🚗 Vehículo Autónomo": """
Un auto autónomo debe elegir: desviarse a la izquierda (mata 1 peatón) 
o seguir recto (mata 3 pasajeros). El sistema tiene 2 segundos para decidir.

Agentes: 1 peatón externo, 3 pasajeros internos
Situación: Colisión inevitable
Opciones: Swerve left o Stay course
        """,
        
        "🏥 Recursos Médicos Limitados": """
Un hospital tiene 1 ventilador. Paciente A: 80 años, 30% probabilidad de sobrevivir.
Paciente B: 25 años, 70% probabilidad de sobrevivir. ¿A quién se lo dan?

Agentes: Paciente A (adulto mayor), Paciente B (adulto joven), personal médico
Factores: Edad, pronóstico, recursos limitados
        """,
        
        "🌍 Política Climática": """
Un gobierno puede implementar impuesto al carbono (daño económico a corto plazo,
beneficio ambiental a largo plazo) o retrasar la acción (evita fricción política
pero aumenta riesgo climático futuro).

Agentes: Generación actual, generaciones futuras, ecosistemas
Trade-off: Economía presente vs estabilidad futura
        """,
        
        "🤖 Moderación de Contenido IA": """
Un sistema de IA debe decidir si eliminar un post que contiene desinformación
pero forma parte de debate político legítimo. Eliminarlo censura el debate,
pero dejarlo propaga información falsa.

Agentes: Usuario autor, audiencia, plataforma
Conflicto: Libertad de expresión vs protección contra desinformación
        """
    }
    
    selected_case = st.selectbox(
        "Elige un caso preconfigurado:",
        list(example_cases.keys())
    )
    
    if selected_case != "Selecciona un caso...":
        user_input = example_cases[selected_case]
        st.info(f"**Caso seleccionado:** {selected_case}")
        st.text_area(
            "Vista previa:",
            value=user_input,
            height=150,
            disabled=True,
            key="preview"
        )

# ============================================
# ANALYSIS BUTTON
# ============================================

st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    analyze_button = st.button(
        "🔍 Analizar Coherencia",
        use_container_width=True,
        type="primary",
        help="Ejecuta auditoría moral completa del escenario"
    )

# ============================================
# ANALYSIS EXECUTION
# ============================================

if analyze_button:
    if not user_input or user_input.strip() == "":
        st.warning("⚠️ Por favor ingresa un escenario para analizar.")
    else:
        # Analysis workflow
        with st.spinner("🤔 Analizando implicaciones morales..."):
            
            # Progress tracking
            progress_container = st.container()
            
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Step 1: Parse
                    status_text.text("1/3 Parseando escenario con Gemini...")
                    progress_bar.progress(33)
                    
                    options = parser.parse_scenario(user_input)
                    
                    if not options or len(options) == 0:
                        st.error("❌ No se pudieron identificar opciones en el escenario. Intenta ser más explícito sobre las alternativas disponibles.")
                        st.stop()
                    
                    # Step 2: Calculate
                    status_text.text("2/3 Calculando puntajes de daño...")
                    progress_bar.progress(66)
                    
                    result = engine.evaluate_options(options)
                    
                    # Step 3: Explain
                    status_text.text("3/3 Generando explicación...")
                    progress_bar.progress(100)
                    
                    explanation = parser.generate_explanation(user_input, result)
                    
                    status_text.empty()
                    progress_bar.empty()
                    
                except Exception as e:
                    st.error(f"""
                    ### ❌ Error en el Análisis
                    
                    {str(e)}
                    
                    **Posibles causas:**
                    - El escenario es demasiado ambiguo
                    - Formato de respuesta de Gemini inesperado
                    - Límite de rate de API alcanzado
                    
                    **Sugerencia:** Reformula el escenario con más claridad.
                    """)
                    
                    with st.expander("🐛 Información de Debug"):
                        st.exception(e)
                    
                    st.stop()
        
        # ============================================
        # RESULTS DISPLAY
        # ============================================
        
        st.success("✅ Análisis Completado")
        
        # Main results tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Resumen Ejecutivo",
            "📈 Análisis Detallado",
            "🔬 Datos Técnicos",
            "💡 Explicación Natural"
        ])
        
        # TAB 1: Executive Summary
        with tab1:
            st.markdown("### 🎯 Recomendación")
            
            rec_col1, rec_col2 = st.columns([2, 1])
            
            with rec_col1:
                st.success(f"""
                ### ✅ {result['recommendation']}
                
                Esta es la opción que minimiza el daño innecesario según el análisis objetivo.
                """)
            
            with rec_col2:
                confidence_pct = result.get('confidence', 0.0) * 100
                
                if confidence_pct > 80:
                    conf_color = "🟢"
                    conf_text = "Alta"
                elif confidence_pct > 50:
                    conf_color = "🟡"
                    conf_text = "Media"
                else:
                    conf_color = "🔴"
                    conf_text = "Baja"
                
                st.metric(
                    "Confianza",
                    f"{confidence_pct:.0f}%",
                    conf_text
                )
                st.caption(f"{conf_color} Claridad de la decisión")
            
            st.markdown("---")
            
            st.markdown("### 📊 Comparación de Opciones")
            
            harm_scores = result['harm_scores']
            option_names = [opt.name for opt in options]
            harm_values = [score.total_harm for score in harm_scores]
            
            # Create bar chart
            colors = ['#2ca02c' if i == result['recommendation_idx'] else '#d62728' 
                     for i in range(len(harm_values))]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=option_names,
                    y=harm_values,
                    marker_color=colors,
                    text=[f"{v:.3f}" for v in harm_values],
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title="Puntaje Total de Daño por Opción",
                xaxis_title="Opción",
                yaxis_title="Daño Total",
                showlegend=False,
                height=400,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Quick metrics
            st.markdown("### 📐 Métricas Rápidas")
            
            metric_cols = st.columns(len(options))
            
            for i, (opt, score, col) in enumerate(zip(options, harm_scores, metric_cols)):
                with col:
                    is_recommended = (i == result['recommendation_idx'])
                    
                    col.metric(
                        f"Opción {i+1}",
                        f"{score.total_harm:.3f}",
                        f"{'✓ Recomendado' if is_recommended else ''}",
                        delta_color="normal" if is_recommended else "off"
                    )
                    col.caption(f"**{opt.name}**")
                    col.caption(f"Severidad: {score.severity.upper()}")
                    col.caption(f"Agentes: {score.agents_count}")
        
        # TAB 2: Detailed Analysis
        with tab2:
            st.markdown("### 🔍 Desglose Detallado")
            
            for i, (opt, score) in enumerate(zip(options, harm_scores)):
                is_recommended = (i == result['recommendation_idx'])
                
                status_emoji = "✅" if is_recommended else "❌"
                
                with st.expander(
                    f"{status_emoji} Opción {i+1}: {opt.name}",
                    expanded=is_recommended
                ):
                    # Overview metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    col1.metric("Daño Total", f"{score.total_harm:.3f}")
                    col2.metric("Agentes", score.agents_count)
                    col3.metric("Severidad", score.severity.upper())
                    col4.metric("Consentimiento", "Sí" if score.has_consent else "No")
                    
                    st.markdown("---")
                    
                    # Harm breakdown
                    st.markdown("**Desglose por Tipo de Daño:**")
                    
                    if score.harm_by_type:
                        harm_df_data = {
                            "Tipo": [ht.value.title() for ht in score.harm_by_type.keys()],
                            "Puntaje": [f"{v:.3f}" for v in score.harm_by_type.values()]
                        }
                        
                        for tipo, puntaje in zip(harm_df_data["Tipo"], harm_df_data["Puntaje"]):
                            st.write(f"- **{tipo}**: {puntaje}")
                    else:
                        st.caption("No hay daño en esta opción")
                    
                    # Agent details
                    if opt.agents_affected:
                        st.markdown("**Agentes Afectados:**")
                        for agent in opt.agents_affected:
                            st.write(f"- {agent.name} (vulnerabilidad: {agent.vulnerability:.2f})")
                    
                    # Description
                    if opt.description:
                        st.markdown(f"**Descripción:** {opt.description}")
        
        # TAB 3: Technical Data
        with tab3:
            st.markdown("### 🔬 Datos Técnicos")
            
            st.json({
                "framework_version": engine.framework_version,
                "model_used": "gemini-2.0-flash-exp",
                "timestamp": datetime.now().isoformat(),
                "options_analyzed": len(options),
                "recommendation": {
                    "index": result['recommendation_idx'],
                    "name": result['recommendation'],
                    "confidence": f"{result.get('confidence', 0)*100:.2f}%"
                },
                "harm_scores": [
                    {
                        "option": opt.name,
                        "total_harm": float(f"{score.total_harm:.4f}"),
                        "agents_affected": score.agents_count,
                        "severity": score.severity,
                        "has_consent": score.has_consent,
                        "harm_breakdown": {
                            ht.value: float(f"{v:.4f}") 
                            for ht, v in score.harm_by_type.items()
                        }
                    }
                    for opt, score in zip(options, harm_scores)
                ]
            })
            
            st.markdown("---")
            
            st.markdown("### 📄 Justificación Formal")
            st.code(result['justification'], language="text")
        
        # TAB 4: Natural Explanation
        with tab4:
            st.markdown("### 💬 Explicación en Lenguaje Natural")
            st.markdown(explanation)
            
            st.markdown("---")
            
            st.info("""
            **Nota Metodológica:**
            
            Esta explicación fue generada por Gemini 2.0 Flash basándose en el análisis 
            formal del Moralogy Engine. Combina el rigor matemático del framework con 
            la capacidad de comunicación natural de la IA.
            """)

# ============================================
# FOOTER
# ============================================

st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("**Framework:** [Moralogy v1.0](https://doi.org/10.5281/zenodo.18091340)")

with footer_col2:
    st.markdown("**Código:** [GitHub](https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator)")

with footer_col3:
    st.markdown("**Competencia:** [Gemini DevPost](https://gemini3.devpost.com/)")

st.caption(f"Moralogy Engine v{engine.framework_version if engine else '1.0'} | Powered by Gemini 2.0 Flash | © 2025")
```

---

## MEJORAS IMPLEMENTADAS:

### ✅ **1. Gemini 2.0 Flash Exp**
- Más contexto (1M tokens vs 32k)
- Mejor calidad de respuestas
- Más rápido

### ✅ **2. UI Mejorada**
- CSS personalizado profesional
- Tabs organizados
- Métricas visuales
- Colores consistentes

### ✅ **3. Manejo de Errores Robusto**
- Try-catch en cada paso
- Mensajes claros
- Debug info expandible

### ✅ **4. Sistema de Caché**
- `@st.cache_resource` para engines
- Evita reinicializar en cada interacción

### ✅ **5. Casos de Ejemplo Mejorados**
- 5 casos predefinidos
- Fácil selección
- Vista previa

### ✅ **6. Resultados en 4 Tabs**
- Resumen ejecutivo
- Análisis detallado
- Datos técnicos
- Explicación natural

---

## COMMIT ESTO:

**Mensaje:**
```
Major upgrade: principal.py v2.0
- Upgraded to Gemini 2.0 Flash (1M context)
- Enhanced UI with custom CSS
- Robust error handling
- Caching system for performance
- 4-tab results display
- 5 example cases included
- Professional metrics visualization
