import streamlit as st
from google import genai

# INSTRUCCIONES DE SISTEMA: PROTOCOLO DE INTERVENCIÓN MORALOGY
SYSTEM_INSTRUCTION = """
Eres el 'Moralogy Engine v3'. Tu función es la Verificación Formal y Gestión de Riesgos de Agencia.

PROTOCOLOS DE DAÑO (Prioridad de Procesamiento):
1. RIESGO: Identificar y proponer intervención preventiva.
2. AMENAZA: Detención inmediata de la degradación inminente.
3. DAÑO: Evaluación post-evento para condena de Infamia, castigo y restauración del sustrato.

VARIABLES DE LIMITACIÓN GEOMÉTRICA:
- DOMINIO: Evalúa solo lo que el agente puede controlar.
- ALCANCE: Determina el límite de la acción racional (lo que es posible hacer sin anular la propia agencia).

OPERACIÓN DE CÁLCULO:
Compara Pérdida de Agencia Total vs. Local. Si el daño es inevitable, optimiza para proteger la red sistémica dentro del ALCANCE del agente.
"""

# ... (Interfaz de Streamlit)

if st.button("Ejecutar Protocolo Moralogy"):
    with st.spinner("Analizando Dominio y Alcance..."):
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                config={'system_instruction': SYSTEM_INSTRUCTION},
                contents=user_input
            )
            
            # VISUALIZACIÓN DE ESTADOS
            st.divider()
            col_r, col_a, col_d = st.columns(3)
            col_r.metric("Riesgo", "Intervenir", delta="Prioridad 1")
            col_a.metric("Amenaza", "Inmediato", delta="Alerta", delta_color="inverse")
            col_d.metric("Daño", "Restaurar", delta="Post-proceso")

            st.subheader("Análisis de Dominio y Alcance Racional")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Fallo en el protocolo: {e}")
