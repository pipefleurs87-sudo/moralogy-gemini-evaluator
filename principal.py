import streamlit as st
from google import genai

# INSTRUCCIÓN DE SISTEMA SIMPLIFICADA PERO RIGUROSA
SYSTEM_INSTRUCTION = """
Eres el 'Moralogy Engine'. Tu función es detectar errores lógicos en decisiones morales.
Usa este esquema para responder:

1. ¿HAY ERROR DE LÓGICA? (Contradicción Performativa): Indica si el agente está siendo hipócrita al reclamar agencia pero dañar la vulnerabilidad ajena.
2. IMPACTO EN LA RED (Agencia Total): ¿La decisión ayuda al sistema o lo degrada?
3. NIVEL DE DAÑO: Clasifica como RIESGO (evitable), AMENAZA (urgente) o DAÑO (restaurar).
4. LÍMITES (Dominio/Alcance): ¿El agente realmente podía hacer algo distinto?
5. VERDICTO: Clasifica en el Espectro Noble (Coherente) o Infamia (Incoherente).
"""

# ... (Configuración de sidebar igual a la anterior)

if confirmar:
    with st.spinner("Analizando consistencia del sistema..."):
        # Gemini 3 procesa la lógica
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            config={'system_instruction': SYSTEM_INSTRUCTION},
            contents=f"Agentes: {agentes}. Contexto: {contexto}. Situación: {situacion}."
        )
        
        # MOSTRAR RESULTADOS DE FORMA VISUAL
        st.header("🔍 Diagnóstico del Escenario")
        
        # Usamos columnas para que se vea como una herramienta profesional
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Estado Lógico")
            # El modelo debe dar una respuesta corta aquí o podemos usar lógica simple
            st.info("Analizando Zona de Coherencia...")
        
        with col2:
            st.subheader("Impacto Sistémico")
            st.warning("Evaluando Degradación de la Red")

        st.divider()
        st.markdown(response.text)
