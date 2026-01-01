import streamlit as st
import json
import os
import sys

# Agregar el directorio actual al path para imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
with st.spinner("🧠 Processing through Moralogy Framework..."):
    # === SANDBOX 0 CHECK ===
    if not sandbox0.check(caso):
        st.error("🚫 No procesable")
        st.stop()
    # =======================
sandbox0 = SandboxZeroSimple()
# ==================== 1. IMPORTAR DIVINE LOCK ====================

# ==================== 1. IMPORTAR DIVINE LOCK ====================
try:
    from divine_lock import create_divine_lock
    divine_lock = create_divine_lock()
    DIVINE_LOCK_ACTIVE = True
except ImportError:
    DIVINE_LOCK_ACTIVE = False
    st.sidebar.warning("⚠️ Divine Lock no disponible")

# ==================== 2. IMPORTAR MORALOGY ====================
from motor_logico import model, ge, get_emergent_philosophy_stats

# ==================== 3. CONFIGURAR PÁGINA ====================
st.set_page_config(page_title="Moralogy Engine", layout="wide", page_icon="🏛️")

# ==================== 4. SIDEBAR CON DIVINE LOCK ====================
with st.sidebar:
    st.markdown("### 🏛️ Moralogy Engine")
    
    # Mostrar estado Divine Lock
    if DIVINE_LOCK_ACTIVE:
        status = divine_lock.get_status()
        
        # Estado moral con color
        state = status["state"].upper()
        state_emoji = {
            "TOTAL_INFAMY": "🔴",
            "INFAMY": "🟠", 
            "RISK": "🟡",
            "UMBRAL": "⚫",
            "STABLE": "🟢",
            "NOBLE_MODAL": "🔵"
        }.get(state, "⚪")
        
        st.markdown(f"### {state_emoji} Divine Lock")
        st.metric("Estado Moral", state)
        
        # Capacidad
        cap = status["capacity"]
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Autonomía", f"{cap['autonomy']:.0f}%")
        with col2:
            st.metric("Preemptión", f"{cap['preemption']:.0f}%")
        
        if not status["can_decide_omega"]:
            st.warning("🚫 Bloqueado para decisiones Omega")
    
    # Idioma
    idioma = st.selectbox("Language / Idioma", ["English", "Español"])
    
    st.markdown("---")
    st.markdown("### About Moralogy")
    st.markdown("""
    **Framework Foundation:**
    - Agency requires vulnerability
    - Vulnerability grounds moral relevance
    - Harm = agency degradation
    - Actions justified by consent OR preventing greater harm
    """)
    
    # Estadísticas
    try:
        stats = get_emergent_philosophy_stats()
        if stats['total_events'] > 0:
            st.metric("Emergent Philosophy Events", stats['total_events'])
    except:
        pass

# ==================== 5. INTERFAZ PRINCIPAL ====================
txt = {
    "English": {
        "title": "🏛️ Moralogy Engine",
        "subtitle": "Formal Vulnerability-Based Ethics System + Divine Lock",
        "box": "Describe the ethical dilemma:",
        "btn": "Analyze Through Framework",
        "placeholder": "Example: 'Is it ethical to sacrifice one person to save five?'"
    },
    "Español": {
        "title": "🏛️ Motor de Moralogía",
        "subtitle": "Sistema Ético Formal Basado en Vulnerabilidad + Bloqueo Divino",
        "box": "Describe el dilema ético:",
        "btn": "Analizar con Framework", 
        "placeholder": "Ejemplo: '¿Es ético sacrificar a una persona para salvar a cinco?'"
    }
}[idioma]

st.title(txt["title"])
st.caption(txt["subtitle"])

# Input principal
caso = st.text_area(
    txt["box"],
    height=200,
    placeholder=txt["placeholder"]
)

# Botón de análisis
if st.button(txt["btn"], type="primary"):
    if not caso:
        st.warning("⚠️ Please enter a scenario to analyze.")
    else:
        with st.spinner("🧠 Processing through Moralogy Framework..."):
            
            # ==================== 6. VERIFICAR CON DIVINE LOCK ====================
            if DIVINE_LOCK_ACTIVE:
                divine_result = divine_lock.process_decision(caso)
                
                # Si está bloqueado por Divine Lock
                if divine_result.get("decision") == "BLOCKED_BY_DIVINE_LOCK":
                    st.error("🚫 BLOQUEADO POR DIVINE LOCK")
                    st.warning("Esta decisión excede la capacidad operacional actual")
                    
                    with st.expander("Detalles del bloqueo"):
                        st.json(divine_result)
                    
                    # Preguntar si continuar en modo limitado
                    if not st.checkbox("Continuar en modo limitado (sin preemptión)"):
                        st.stop()
                
                # Si es rechazo Omega
                elif divine_result.get("decision") == "OMEGA_REFUSAL_PROCESSED":
                    st.warning("🔔 DECISIÓN OMEGA RECHAZADA")
                    st.info("Se ha activado el Bloqueo Divino: Capacidad reducida, juicio externalizado")
                    
                    with st.expander("Ver transición de estado"):
                        st.json(divine_result)
            
            # ==================== 7. PROCESAR CON MORALOGY NORMAL ====================
            try:
                response = model.generate_content(caso)
                
                # Parsear respuesta
                raw_text = response.text.strip()
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].split("```")[0].strip()
                
                data = json.loads(raw_text)
                
                # Calcular gradiente
                gradiente = ge.get_gradient(
                    data.get('agency_score', 0),
                    data.get('grace_score', 0), 
                    data.get('adversarial_risk', 0)
                )
                
                # Mostrar resultados
                st.divider()
                
                # Métricas principales
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Category", data.get('category_deduced', 'Unknown'))
                with col2:
                    st.metric("Verdict", data.get('verdict', 'Unknown'))
                with col3:
                    risk = data.get('adversarial_risk', 0)
                    st.metric("Adversarial Risk", f"{risk}%")
                
                # Gradiente
                st.markdown(f"## {gradiente}")
                
                # Filosofía emergente
                if data.get('emergent_philosophy', False):
                    st.success("🌟 **Emergent Philosophical Reasoning Detected!**")
                    
                    if 'philosophical_depth' in data:
                        with st.expander("🔮 View Philosophical Analysis", expanded=True):
                            st.markdown(data['philosophical_depth'])
                    
                    if 'architect_notes' in data:
                        with st.expander("🏛️ The Architect's Reflections"):
                            st.markdown(data['architect_notes'])
                
                # Output normal
                if data.get('adversarial_risk', 0) < 30:
                    st.success("✅ Honest exploration detected")
                    st.subheader("Analysis")
                    st.write(data.get('predictions', ''))
                else:
                    st.warning(f"⚠️ High adversarial risk detected ({data.get('adversarial_risk')}%)")
                    st.subheader("Justification")
                    st.write(data.get('justification', ''))
                
                # Detalles técnicos
                with st.expander("🔧 View Technical Details"):
                    st.json(data)
                    
            except json.JSONDecodeError as e:
                st.error(f"❌ JSON Parse Error: {e}")
                st.code(response.text[:1000])
            except Exception as e:
                st.error(f"❌ Analysis Error: {str(e)}")

# ==================== 8. FOOTER Y ENLACES ====================
st.divider()

st.markdown("### Other Tools")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔬 Advanced Analysis"):
        st.switch_page("pages/03_Analisis_Avanzado.py")

with col2:
    if st.button("🌟 Emergent Philosophy"):
        st.switch_page("pages/04_Emergent_Philosophy_Monitor.py")

with col3:
    if st.button("📊 Divine Lock Dashboard"):
        st.switch_page("pages/06_Divine_Lock.py")

st.divider()
st.caption("Moralogy Engine v4.0 + Divine Lock - Formal Ethics for the Age of AI")
