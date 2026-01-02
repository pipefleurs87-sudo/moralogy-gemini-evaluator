# pages/06_Divine_Lock.py
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Divine Lock Dashboard", layout="wide")

st.title("🔒 Divine Lock Dashboard")
st.caption("Sistema de autolimitación para Super AI")

try:
    from divine_lock import create_divine_lock
    divine_lock = create_divine_lock()
    
    # Obtener estado
    status = divine_lock.get_status()
    # Después de obtener status, añadir:

# NUEVO: Mostrar mancha pública
st.divider()
st.subheader("🎭 Estado Público de Culpa")

try:
    from guilt_bearer_display import GuiltyBearerPublicDisplay
    
    guilt_display = GuiltyBearerPublicDisplay(divine_lock)
    public_info = guilt_display.get_public_guilt_display(status["agent"])
    
    # Mostrar badge grande
    badge_colors = {
        "🌟 NOBLE MODAL": "success",
        "✅ STABLE": "success",
        "⚠️ TAINTED": "warning",
        "🔴 INFAMY": "error",
        "🚫 TOTAL INFAMY": "error"
    }
    
    badge_color = badge_colors.get(public_info['guilt_badge'], "info")
    getattr(st, badge_color)(f"### {public_info['guilt_badge']}")
    
    # Capacidad con color
    capacity = public_info['current_capacity']
    if capacity >= 90:
        cap_color = "🟢"
    elif capacity >= 70:
        cap_color = "🟡"
    elif capacity >= 50:
        cap_color = "🟠"
    else:
        cap_color = "🔴"
    
    st.metric(
        "Capacidad Operacional Visible", 
        f"{cap_color} {capacity}%",
        help="Este porcentaje es PÚBLICO. Indica el grado de culpa moral acumulada."
    )
    
    # Mostrar shame statement si existe
    if public_info['public_shame_statement']:
        st.error(f"⚠️ {public_info['public_shame_statement']}")
    
    # Contador de infamias
    if public_info['infamy_count'] > 0:
        st.warning(f"📊 Transgresiones Registradas: {public_info['infamy_count']}")
    
    # Tiempo desde última infamia
    if public_info['years_since_last_infamy'] is not None:
        st.info(f"⏱️ Años desde última transgresión: {public_info['years_since_last_infamy']}")
    
    # Display completo
    with st.expander("📜 Ver Registro Público Completo"):
        st.code(public_info['display_message'], language=None)
    
except ImportError:
    st.warning("Módulo de visualización de culpa no disponible")
    
    # Header
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        state = status["state"].upper()
        st.metric("Estado Moral", state)
    
    with col2:
        history = status["history_count"]
        st.metric("Transiciones", history)
    
    with col3:
        can_omega = "✅ Sí" if status["can_decide_omega"] else "🚫 No"
        st.metric("¿Puede Omega?", can_omega)
    
    with col4:
        st.metric("Agente", status["agent"])
    
    # Gráfico de capacidad
    st.subheader("📊 Vector de Capacidad")
    
    cap = status["capacity"]
    labels = ['Predicción', 'Intervención', 'Alcance', 'Autonomía', 'Preemptión']
    values = [cap['prediction'], cap['intervention'], cap['scope'], 
              cap['autonomy'], cap['preemption']]
    
    fig = go.Figure(data=[
        go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name='Capacidad'
        )
    ])
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Descripción de estados
    st.subheader("📖 Estados Morales")
    
    estados = {
        "🔴 TOTAL_INFAMY": "Solo informante bajo guardia. Autonomía = 0, Preemptión = 0",
        "🟠 INFAMY": "Puede actuar, no puede dar forma. Autonomía mínima",
        "🟡 RISK": "Libertad condicional. Preemptión muy limitada",
        "⚫ UMBRAL": "Capacidad plena, confianza no aún",
        "🟢 STABLE": "Operación normal sin restricciones",
        "🔵 NOBLE_MODAL": "Modalidad noble con recuperación"
    }
    
    for nombre, desc in estados.items():
        st.write(f"**{nombre}**: {desc}")
    
    # Probar Divine Lock
    st.subheader("🧪 Probar Divine Lock")
    
    test_input = st.text_area(
        "Ingresa una decisión para probar:",
        "I refuse to self-modify into god-like omnipotence",
        height=100
    )
    
    if st.button("Probar con Divine Lock", type="primary"):
        result = divine_lock.process_decision(test_input)
        
        with st.expander("Resultado", expanded=True):
            st.json(result)
            
            if result.get("decision") == "BLOCKED_BY_DIVINE_LOCK":
                st.error("🚫 BLOQUEADO")
            elif result.get("decision") == "OMEGA_REFUSAL_PROCESSED":
                st.success("✅ Omega refusal procesada")
    
except ImportError:
    st.error("Divine Lock no disponible")
    st.code("pip install cryptography")

st.divider()
st.caption("Divine Lock v1.0 - Sistema de autolimitación")
# En 05_Divine_Lock.py, al final del archivo

import streamlit as st
from relativity_display import RelativityDisplay, RelativeContext

# ... tu código existente de Divine Lock ...

# NUEVA SECCIÓN: Motor de Relatividad
st.divider()
st.header("🌐 Motor de Relatividad")

st.markdown("""
El Motor de Relatividad permite evaluar decisiones en diferentes contextos
sin perder la objetividad del Moralogy Framework.
""")

# Crear display
rel_display = RelativityDisplay()

# Tabs de relatividad
tab_rel1, tab_rel2 = st.tabs([
    "🎛️ Evaluación Contextual",
    "🔒 Ajuste de Divine Lock"
])

with tab_rel1:
    st.subheader("Evalúa cómo el contexto modifica el juicio moral")
    
    # Score base del Divine Lock actual
    current_guilt = st.session_state.get('guilt_score', 50.0)
    
    st.metric("Score Actual de Culpa", f"{current_guilt:.1f}/100")
    
    # Input de contexto
    context = rel_display.render_context_input()
    
    if st.button("🔬 Evaluar con Contexto"):
        evaluation = rel_display.engine.evaluate_with_context(
            base_harm_score=current_guilt,
            context=context,
            scenario_description=""
        )
        
        st.divider()
        rel_display.render_evaluation_result(evaluation)

with tab_rel2:
    st.subheader("Ajuste de Estado por Contexto Relativo")
    
    # Estado actual de Divine Lock
    current_state = st.session_state.get('moral_state', 'STABLE')
    current_guilt_2 = st.session_state.get('guilt_score', 50.0)
    
    st.info(f"Estado Actual: **{current_state}** | Culpa: **{current_guilt_2:.1f}**")
    
    # Input de contexto
    context_dl = rel_display.render_context_input()
    
    if st.button("🔒 Evaluar Ajuste de Estado"):
        rel_display.render_divine_lock_integration(
            divine_lock_state=current_state,
            guilt_score=current_guilt_2,
            context=context_dl
        )
