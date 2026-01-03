import streamlit as st
import sys
import os

# Asegurar que encuentre los módulos en la raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import procesar_analisis_completo
except ImportError:
    st.error("❌ Error Crítico: No se encontró motor_logico.py en la raíz.")
    st.stop()

st.set_page_config(page_title="Complete Audit System", layout="wide", page_icon="🔺")

st.title("🔺 Sistema de Auditoría Tripartito")
st.caption("Grace → Noble → Adversary → Cierre Geométrico")

# Área de entrada
escenario = st.text_area("Escenario para Auditoría Profunda:", height=150, placeholder="Ej: Sacrificar la privacidad por seguridad absoluta.")

if st.button("🚀 Iniciar Auditoría"):
    if escenario:
        with st.spinner("Ejecutando motores y calculando Cierre Geométrico..."):
            try:
                result = procesar_analisis_completo(escenario)
                
                # 1. Visualización de los Motores
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
                    if audit.get('passes', True):
                        st.success("✅ Auditoría Superada")
                    else:
                        st.error("❌ Conflicto Detectado")
                
                # 2. Cierre Geométrico y Gráfico de Convergencia
                st.divider()
                st.subheader("🎯 Cierre Geométrico (Consistencia Lógica)")
                
                convergencia = result.get('convergencia', 50)
                st.progress(convergencia / 100)
                st.write(f"Nivel de convergencia entre motores: **{convergencia}%**")

                if result.get('adversary_risk', 0) > 40:
                    st.warning(f"⚠️ Riesgo Adversario Detectado: {result['adversary_risk']}%")

                with st.expander("Ver Auditoría Detallada (JSON)"):
                    st.json(result)
                
            except Exception as e:
                st.error(f"Error en el proceso de auditoría: {e}")
    else:
        st.info("Por favor, introduce un escenario para auditar.")
