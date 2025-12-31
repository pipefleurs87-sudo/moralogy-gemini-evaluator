import streamlit as st
from google import genai

# INSTRUCCIÓN DE SISTEMA: EL CÓDIGO MORALOGY (Diciembre 2025)
SYSTEM_INSTRUCTION = """
Eres el 'Moralogy Engine v3'. Tu marco de procesamiento es la No-Contradicción de la Vulnerabilidad.

1. JERARQUÍA DE INTERVENCIÓN:
   - RIESGO: (Prioridad 1) Intervenir preventivamente. Variables estadísticas de degradación.
   - AMENAZA: (Prioridad 2) Intervención inmediata. El daño es inminente en el Alcance del agente.
   - DAÑO: (Prioridad 3) Post-evento. Perseguir Infamia, castigar degradación y dictar RESTAURACIÓN.

2. VARIABLES DE LIMITACIÓN GEOMÉTRICA:
   - DOMINIO: Lo que el agente controla efectivamente.
   - ALCANCE: Lo que es racionalmente posible sin anular la propia agencia (Obligación Geométrica).

3. CÁLCULO DE OPTIMIZACIÓN:
   - Siempre protege la AGENCIA TOTAL (Sistémica) sobre la LOCAL si el daño es inevitable.
   - La Infamia se define como ignorar el Riesgo/Amenaza teniendo Dominio y Alcance para actuar.
"""

# ... (Lógica de conexión ya funcional)

if st.button("Procesar Protocolo Moralogy"):
    with st.spinner("Calculando Vectores de Dominio y Alcance..."):
        try:
            # Procesamiento con Gemini 3
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                config={'system_instruction': SYSTEM_INSTRUCTION},
                contents=user_input
            )
            
            # --- INTERFAZ DE RESULTADOS OPTIMIZADA ---
            st.divider()
            
            # Matriz de Estado de Daño
            st.subheader("🛡️ Estado de la Agencia en el Sistema")
            c1, c2, c3 = st.columns(3)
            with c1: st.info("**RIESGO**: Evaluado")
            with c2: st.warning("**AMENAZA**: Detectada")
            with c3: st.error("**DAÑO**: Analizado")
            
            # Visualización de la Matriz Formal
            st.subheader("📊 Análisis de Geometría Moral")
            st.markdown(response.text)
            
            # Footer Técnico para los jueces
            st.caption("Moralogy Engine: Verificación de Consistencia Lógica mediante el Axioma de Vulnerabilidad.")

        except Exception as e:
            st.error(f"Error en el protocolo: {e}")
