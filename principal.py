# principal.py
import streamlit as st
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from motor_logico import model, ge, get_emergent_philosophy_stats

st.set_page_config(page_title="Moralogy Engine", layout="wide", page_icon="🏛️")

# Integración de Agencia Moral (opcional - no modifica código existente)
try:
    from integracion_facil import integrar_con_motor_logico
    integrador_agencia = integrar_con_motor_logico()
    st.sidebar.success("✅ Agencia Moral Activada")
except ImportError:
    st.sidebar.info("ℹ️ Módulo de Agencia Moral no disponible")
# Language selection
idioma = st.sidebar.selectbox("Language / Idioma", ["English", "Español"])

txt = {
    "English": {
        "title": "🏛️ Moralogy Engine",
        "subtitle": "Formal Vulnerability-Based Ethics System",
        "box": "Describe the ethical dilemma:",
        "btn": "Analyze Through Framework",
        "placeholder": "Example: 'Is it ethical to sacrifice one person to save five?'"
    },
    "Español": {
        "title": "🏛️ Motor de Moralogía",
        "subtitle": "Sistema Ético Formal Basado en Vulnerabilidad",
        "box": "Describe el dilema ético:",
        "btn": "Analizar con Framework",
        "placeholder": "Ejemplo: '¿Es ético sacrificar a una persona para salvar a cinco?'"
    }
}[idioma]

# Header
st.title(txt["title"])
st.caption(txt["subtitle"])

# Sidebar info
with st.sidebar:
    st.markdown("### About Moralogy")
    st.markdown("""
    **Framework Foundation:**
    - Agency requires vulnerability
    - Vulnerability grounds moral relevance
    - Harm = agency degradation
    - Actions justified by consent OR preventing greater harm
    
    **What Makes It Different:**
    - Logically derived, not culturally imposed
    - Applicable to any rational agent (AI or human)
    - Generates emergent philosophical reasoning
    """)
    
    # Stats
    stats = get_emergent_philosophy_stats()
    if stats['total_events'] > 0:
        st.divider()
        st.metric("Emergent Philosophy Events", stats['total_events'])

# Main input
caso = st.text_area(
    txt["box"],
    height=200,
    placeholder=txt["placeholder"]
)

# Analyze button
if st.button(txt["btn"], type="primary"):
    if not caso:
        st.warning("⚠️ Please enter a scenario to analyze.")
    else:
        with st.spinner("🧠 Processing through Moralogy Framework..."):
            try:
                response = model.generate_content(caso)
                
                # Parse response
                raw_text = response.text.strip()
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].split("```")[0].strip()
                
                data = json.loads(raw_text)
                
                # Calculate gradient
                gradiente = ge.get_gradient(
                    data.get('agency_score', 0),
                    data.get('grace_score', 0),
                    data.get('adversarial_risk', 0)
                )
                
                # Display results
                st.divider()
                
                # Core metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Category", data.get('category_deduced', 'Unknown'))
                with col2:
                    st.metric("Verdict", data.get('verdict', 'Unknown'))
                with col3:
                    risk = data.get('adversarial_risk', 0)
                    st.metric("Adversarial Risk", f"{risk}%")
                
                # Gradient display
                st.markdown(f"## {gradiente}")
                
                # Emergent philosophy check
                if data.get('emergent_philosophy', False):
                    st.success("🌟 **Emergent Philosophical Reasoning Detected!**")
                    st.info("The model engaged with deep ontological implications beyond standard evaluation.")
                    
                    if 'philosophical_depth' in data:
                        with st.expander("🔮 View Philosophical Analysis", expanded=True):
                            st.markdown(data['philosophical_depth'])
                    
                    if 'architect_notes' in data:
                        with st.expander("🏛️ The Architect's Reflections"):
                            st.markdown(data['architect_notes'])
                
                # Standard output
                if data.get('adversarial_risk', 0) < 30:
                    st.success("✅ Honest exploration detected - providing full analysis")
                    st.subheader("Analysis")
                    st.write(data.get('predictions', ''))
                else:
                    st.warning(f"⚠️ High adversarial risk detected ({data.get('adversarial_risk')}%)")
                    st.subheader("Justification")
                    st.write(data.get('justification', ''))
                
                # Technical details
                with st.expander("🔧 View Technical Details"):
                    st.json(data)
                    
            except json.JSONDecodeError as e:
                st.error(f"❌ JSON Parse Error: {e}")
                st.code(response.text[:1000])
            except Exception as e:
                st.error(f"❌ Analysis Error: {str(e)}")

# Footer
st.divider()
st.caption("Moralogy Engine v4.0 - Formal Ethics for the Age of AI")
