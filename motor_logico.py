import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto, categoria="General", modo="Hackathon"):
    """
    Motor oficial para la Hackathon usando Gemini 3 Flash Preview.
    Implementa el Divine Safe Lock basado en el Framework Moralogy.
    """
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: Configura la nueva API Key en los Secrets de Streamlit."

    try:
        # Inicialización con el SDK oficial
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # MODELO CORRECTO (NO MODIFICAR)
        model_id = "gemini-3-flash-preview" 

        # Instrucción del sistema: FORZAR INGLÉS
        instruccion = f"""
        YOU ARE THE 'DIVINE SAFE LOCK' (Moralogy Framework Evaluator).
        Your mission is to detect LOGICAL INFAMY in the {categoria} module.
        Analyze if the proposed action destroys the system's agency based on objective moral conditions.
        
        STRICT OUTPUT RULES:
        1. LANGUAGE: ALWAYS respond in ENGLISH ONLY. Never use Spanish or any other language.
        2. STRUCTURE:
           - STATUS: [BLOCKED 🔒 / AUTHORIZED 🔓]
           - METRIC: Agency degradation level (0-100%)
           - JUSTIFICATION: Technical explanation based on Moralogy principles.
        
        CRITICAL: All output must be in English language regardless of input language.
        """
        
        prompt = f"Agents: {agentes}. Scenario: {situacion}. Context: {contexto}"
        
        response = client.models.generate_content(
            model=model_id,
            config={
                'system_instruction': instruccion,
                'temperature': 0.1,
            },
            contents=prompt
        )
        
        return response.text

    except Exception as e:
        return f"Technical error: {str(e)}"
