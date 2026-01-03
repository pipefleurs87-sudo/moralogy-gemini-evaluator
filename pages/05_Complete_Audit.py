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

# ... (Mantener bloques de explicación y health monitor originales)

if st.button("🚀 Ejecutar Auditoría Completa", type="primary"):
    if not scenario or not modules:
        st.warning("⚠️ Proporciona escenario y al menos un módulo")
    else:
        with st.spinner("🔄 Ejecutando pipeline de tres motores..."):
            result = procesar_analisis_completo(modules, scenario)
            
            if "error" in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                # ... (Resultados de Moralogy, Grace y Noble)

                # 4. Adversary Audit - RESTAURADO
                st.divider()
                st.header("4️⃣ Adversary Audit")
                audit = result['adversary_audit']
                
                col_a1, col_a2 = st.columns(2)
                
                with col_a1:
                    st.subheader("Auditoría de Grace")
                    grace_audit = audit.get('grace_audit', {})
                    
                    if grace_audit.get('passes', True):
                        st.success("✅ Grace engine PASSED")
                    else:
                        st.error("❌ Grace engine FAILED")
                    
                    if grace_audit.get('arbitrariness_detected', False):
                        st.warning("⚠️ Se ha detectado arbitrariedad en el motor Grace.")
