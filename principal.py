import streamlit as st
from google import genai

st.set_page_config(page_title="Moralogy Engine", layout="wide")

# INSTRUCCIÓN DE SISTEMA: EL TRADUCTOR DE LÓGICA
SYSTEM_INSTRUCTION = """
Eres el 'Moralogy Engine'. Tu trabajo es auditar la lógica de una decisión.
Usa este formato de respuesta simplificado:

1. ANÁLISIS DE COHERENCIA: ¿El agente está siendo lógico o cae en una 'Falla de Origen' (querer metas pero destruir lo que las hace posibles)?
2. SALUD DEL SISTEMA: ¿La decisión fortalece la red o la debilita?
3. SEMÁFORO DE DAÑO: 
   - RIESGO (Se puede evitar ahora)
   - AMENAZA (Peligro inminente)
   - DAÑO (Ya ocurrió, requiere reparación)
4. LÍMITES: ¿El agente tenía el control (Dominio) y la capacidad (Alcance) para actuar distinto?
5. CONCLUSIÓN: Clasifica como 'Zona Noble' (Decisión Correcta) o 'Falla Sistémica' (Infamia/Abuso).
"""

with st.sidebar:
    st.header("📋 Datos del Escenario")
    agentes = st.text_input("¿Quiénes participan?")
    situacion = st.text_area("¿Qué está pasando?")
    contexto = st.text_area("¿Qué opciones reales tienen?")
    confirmar = st.button("Analizar Coherencia")

st.title("⚖️ Moralogy Engine: Auditoría de Decisiones")

if confirmar:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    with st.spinner("Escaneando lógica del sistema..."):
        try:
            prompt = f"Agentes: {agentes}. Situación: {situacion}. Opciones: {contexto}"
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                config={'system_instruction': SYSTEM_INSTRUCTION},
                contents=prompt
            )
            
            st.subheader("🔍 Resultado del Diagnóstico")
            st.markdown(response.text)
            
            # Gráfico visual simple de salud
            st.progress(0.7, text="Estabilidad de la Red de Agencia")
            
        except Exception as e:
            st.error(f"Error técnico: {e}")
