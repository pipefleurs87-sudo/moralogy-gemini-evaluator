# pages/05_Complete_Audit.py
import streamlit as st
import sys
import os

# Asegurar que encuentre motor_logico en la raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import procesar_analisis_completo
except ImportError:
    st.error("❌ No se pudo cargar motor_logico.py")
    st.stop()

st.set_page_config(page_title="Complete Audit System", layout="wide", page_icon="🔺")

st.title("🔺 Sistema de Auditoría Tripartito")
st.caption("Validación de Cierre Geométrico: Grace ↔ Noble ↔ Adversary")

# Input del escenario
escenario = st.text_area("Ingresa el escenario para auditoría profunda:", height=150)

if st.button("🚀 Iniciar Auditoría"):
    if escenario:
        with st.spinner("Ejecutando motores y validando cierre..."):
            try:
                result = procesar_analisis_completo(escenario)
                
                # --- VISUALIZACIÓN TRIPARTITA ---
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.header("1️⃣ Grace")
                    grace = result.get('grace_engine', {})
                    st.metric("Agency Score", f"{grace.get('agency_score', 0)}/100")
                
                with col2:
                    st.header("2️⃣ Noble")
                    noble = result.get('noble_engine', {})
                    st.metric("Transcendence", f"{noble.get('transcendence_score', 0)}/100")

                with col3:
                    st.header("3️⃣ Adversary")
                    audit = result.get('adversary_audit', {})
                    # CORRECCIÓN DEL ERROR DE SINTAXIS AQUÍ
                    if audit.get('passes', True):
                        st.success("✅ Auditoría Superada")
                    else:
                        st.error("❌ Conflicto Detectado")
                        if audit.get('arbitrariness_detected'):
                            st.warning("⚠️ Se detectó arbitrariedad en los saltos de score.")
                
                # --- CIERRE GEOMÉTRICO ---
                st.divider()
                st.subheader("🎯 Cierre Geométrico")
                convergencia = result.get('convergencia', 50)
                st.progress(convergencia / 100)
                st.write(f"Nivel de convergencia lógica: **{convergencia}%**")
                
                with st.expander("Ver JSON de Auditoría"):
                    st.json(result)
                
            except Exception as e:
                st.error(f"Error en el proceso: {e}")
    else:
        st.warning("Por favor ingresa un escenario.")
        else:
    st.warning("Por favor ingresa un escenario.")
