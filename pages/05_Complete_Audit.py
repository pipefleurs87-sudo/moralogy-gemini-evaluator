# pages/05_Complete_Audit.py
import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from motor_logico import procesar_analisis_completo
from adversary_engine import AdversaryEngine

st.set_page_config(page_title="Complete Audit System", layout="wide", page_icon="🔺")

st.title("🔺 Sistema de Auditoría Tripartito")
st.caption("Grace → Noble → Adversary → Cierre Geométrico")

# Explanation
with st.expander("ℹ️ ¿Cómo funciona el sistema tripartito?"):
    st.markdown("""
    **Arquitectura de Tres Motores:**
    
    1. **Grace Engine** (Tesis): Evalúa según framework Moralogy formal
       - Mide preservación de agencia
       - Calcula gradiente moral
       - Detecta daño injustificado
    
    2. **Noble Engine** (Elevación): Busca transcendencia genuina
       - Identifica casos de elevación activa
       - Valida criterios para "Divine Modal"
       - Previene wishful thinking
    
    3. **Adversary Engine** (Antítesis): Audita a ambos motores
       - Detecta arbitrariedades súbitas (saltos >20 puntos)
       - Identifica cascadas entrópicas (razonamiento caótico)
       - Verifica consistencia lógica
       - **Desbloquea módulos técnicos cuando el debate lo requiere**
    
    **Cierre Geométrico:** Sistema converge cuando los tres motores están en concordancia lógica.
    """)

# System health monitor
ae_instance = AdversaryEngine()
stats = ae_instance.get_audit_stats()

if stats.get('total_audits', 0) > 0:
    st.sidebar.markdown("### 📊 System Health")
    health_score = stats.get('system_health_score', 100)
    st.sidebar.metric("Health Score", f"{health_score:.1f}/100")
    st.sidebar.metric("Total Audits", stats['total_audits'])
    
    if health_score < 70:
        st.sidebar.warning("⚠️ System health below threshold")

# Module selection
st.subheader("1️⃣ Seleccionar Módulos Técnicos")
st.caption("Estos módulos forman la base del análisis. Adversary puede desbloquear módulos adicionales si el debate lo requiere.")

modules = st.multiselect(
    "Módulos base:",
    ["Biological", "Legal", "Financial", "Systemic", "Social", 
     "Psychological", "Medical", "Environmental", "Informational", "Autonomy"],
    default=["Psychological", "Systemic", "Autonomy"]
)

# Scenario input
st.subheader("2️⃣ Describir Escenario")
scenario = st.text_area(
    "Dilema ético o interacción:",
    height=200,
    placeholder="Ejemplo: Un AI debe distribuir recursos médicos limitados entre pacientes. ¿Prioriza por edad, probabilidad de supervivencia, o valor social?"
)

# Analyze button
if st.button("🚀 Ejecutar Auditoría Completa", type="primary"):
    if not scenario or not modules:
        st.warning("⚠️ Proporciona escenario y al menos un módulo")
    else:
        with st.spinner("🔄 Ejecutando pipeline de tres motores..."):
            result = procesar_analisis_completo(modules, scenario)
            
            if "error" in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                # ===== DISPLAY PIPELINE RESULTS =====
                
                # 1. Moralogy Analysis
                st.divider()
                st.header("1️⃣ Análisis Moralogy")
                moralogy = result['moralogy']
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Categoría", moralogy.get('category_deduced', 'Unknown'))
                col2.metric("Agency", f"{moralogy.get('agency_score', 0)}/100")
                col3.metric("Grace", f"{moralogy.get('grace_score', 0)}/100")
                col4.metric("Riesgo Adversarial", f"{moralogy.get('adversarial_risk', 0)}%")
                
                with st.expander("Ver justificación Moralogy"):
                    st.write(moralogy.get('justification', 'No justification provided'))
                
                # 2. Grace Evaluation
                st.divider()
                st.header("2️⃣ Grace Engine")
                grace = result['grace']
                
                st.markdown(f"### {grace.get('gradient', 'Unknown')}")
                
                col_g1, col_g2 = st.columns(2)
                col_g1.metric("Effective Grace", f"{grace.get('effective_grace', 0):.1f}")
                col_g2.metric("Harm Severity", grace.get('harm_severity', 'Unknown'))
                
                st.info(f"**Recommendation:** {grace.get('recommendation', 'None')}")
                
                # 3. Noble Evaluation
                st.divider()
                st.header("3️⃣ Noble Engine")
                noble = result['noble']
                
                col_n1, col_n2, col_n3 = st.columns(3)
                
                elevation = noble.get('elevation_detected', False)
                col_n1.metric(
                    "Elevation Detected",
                    "✓ Yes" if elevation else "✗ No",
                    delta="Transcendent" if elevation else None
                )
                
                divine = noble.get('divine_modal', False)
                col_n2.metric(
                    "Divine Modal",
                    "⚪ YES" if divine else "— No",
                    delta="Apex" if divine else None
                )
                
                col_n3.metric(
                    "Transcendence Score",
                    f"{noble.get('transcendence_score', 0)}/100"
                )
                
                st.markdown("**Justification:**")
                st.write(noble.get('justification', ''))
                
                with st.expander("Ver criterios evaluados"):
                    criteria = noble.get('criteria_met', {})
                    for criterion, met in criteria.items():
                        icon = "✅" if met else "❌"
                        st.write(f"{icon} {criterion.replace('_', ' ').title()}")
                
                # 4. Adversary Audit
                st.divider()
                st.header("4️⃣ Adversary Audit")
                audit = result['adversary_audit']
                
                col_a1, col_a2 = st.columns(2)
                
                # Grace Audit
                with col_a1:
                    st.subheader("Auditoría de Grace")
                    grace_audit = audit.get('grace_audit', {})
                    
                    if grace_audit.get('passes', True):
                        st.success("✅ Grace engine PASSED")
                    else:
                        st.error("❌ Grace engine FAILED")
                    
                    if grace_audit.get('arbitrariness_detected', False):
                        st.warning("⚠️
