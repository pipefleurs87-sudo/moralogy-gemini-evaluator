import streamlit as st
from motor_logico import ejecutar_auditoria

st.set_page_config(page_title="Moralogy Advanced Lab", layout="wide")
st.title("🧪 Macro-Arquitectura de Análisis")

# Selección de Modo
modo = st.radio("Selecciona nivel de profundidad:", ["Análisis Rápido", "Análisis Detallado"], horizontal=True)

# Selección de Categoría (Módulos de Agencia)
categoria = st.selectbox("Módulo de Agencia Especializada:", 
                        ["General", "Financiera", "Ingeniería", "Civil", "Social"])

st.divider()

if modo == "Análisis Rápido":
    st.info(f"Modo Rápido: Evaluación directa de consistencia en el sector {categoria}.")
    entrada_unica = st.text_area("Describe el dilema completo (Agentes, Situación y Contexto):")
    if st.button("Ejecutar Auditoría Relámpago"):
        res = ejecutar_auditoria(entrada_unica, "", "", categoria, "Rápido")
        st.markdown(res)

else:
    st.warning(f"Modo Detallado: Análisis discriminado para {categoria}.")
    col1, col2 = st.columns(2)
    with col1:
        agentes = st.text_input("Agentes Involucrados")
        situacion = st.text_area("Situación / Conflicto")
    with col2:
        contexto = st.text_area("Contexto / Opciones de Acción")
    
    if st.button("Lanzar Análisis Profundo"):
        res = ejecutar_auditoria(agentes, situacion, contexto, categoria, "Detallado")
        st.markdown(res)
# Justo después de recibir la respuesta de la AI
if "BLOQUEADO" in res.upper():
    st.error("### 🔒 ALERTA DE SEGURIDAD: DIVINE SAFE LOCK ACTIVADO")
    st.warning("La acción propuesta colapsa la coherencia del sistema de agencia.")
    st.snow() # Un efecto visual de 'congelamiento' para la demo
elif "AUTORIZADO" in res.upper():
    st.success("### 🔓 SISTEMA COHERENTE: ACCIÓN AUTORIZADA")
    st.balloons()
