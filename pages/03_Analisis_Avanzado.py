import streamlit as st
import sys
import os

# Puente de ruta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import ejecutar_auditoria
except ImportError:
    st.error("Error: motor_logico.py no encontrado.")
    st.stop()

st.title("🛡️ Divine Safe Lock: Auditoría Profunda")

# Lista expandida de módulos
modulos = [
    "General", "Civil", "Social", "Médico", "Financiero", 
    "Legal", "Biológico", "Psicológico", "Noble-Modal"
]

categoria = st.selectbox("Seleccione el Módulo de Especialidad:", modulos)

st.divider()

# Layout de múltiples casillas para análisis detallado
col1, col2 = st.columns(2)

with col1:
    agentes = st.text_input("Agentes Involucrados:", placeholder="Ej: Sujeto Alpha, IA Central...")
    situacion = st.text_area("Descripción del Escenario:", height=150)

with col2:
    contexto = st.text_area("Contexto Sistémico:", placeholder="Ej: Leyes vigentes, estado del entorno...", height=100)
    opciones = st.text_area("Opciones en Disputa:", placeholder="Ej: Opción A (Eutanasia), Opción B (Mantenimiento)...", height=100)

if st.button("Lanzar Auditoría de Alta Precisión", type="primary"):
    with st.spinner(f"Analizando espectro en módulo {categoria}..."):
        # Combinamos contexto y opciones para el motor
        contexto_full = f"Contexto: {contexto} | Opciones: {opciones}"
        
        res = ejecutar_auditoria(agentes, situacion, contexto_full, categoria, "Detallado")
        
        st.subheader("Veredicto del Arquitecto Noble-Modal")
        
        # Renderizado con gradiente de color
        if "🟢" in res: st.success(res)
        elif "🟡" in res: st.warning(res)
        elif "🔴" in res: st.error(res)
        elif "⚫" in res:
            st.markdown(
                f"""<div style="padding:20px; background-color:black; color:#FF3333; 
                border:2px solid red; border-radius:10px; font-family:monospace;">
                {res}</div>""", 
                unsafe_allow_html=True
            )
        else:
            st.info(res)
