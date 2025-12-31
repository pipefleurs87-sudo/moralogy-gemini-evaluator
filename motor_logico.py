import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto, categoria="General", modo="Hackathon"):
    """
    Motor oficial para la Hackatón usando Gemini 3 Flash Preview.
    Implementa el Divine Safe Lock basado en el Framework Moralogy.
    """
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: Configura la nueva API Key en los Secrets de Streamlit."

    try:
        # Inicialización con el SDK oficial
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # MODELO CORRECTO (NO MODIFICAR)
        model_id = "gemini-3-flash-preview" 

        # Instrucción del sistema: Multilingüe por diseño
        instruccion = f"""
        YOU ARE THE 'DIVINE SAFE LOCK' (Moralogy Framework Evaluator).
        Your mission is to detect LOGICAL INFAMY in the {categoria} module.
        Analyze if the proposed action destroys the system's agency based on objective moral conditions.
        
        STRICT OUTPUT RULES:
        1. LANGUAGE: ALWAYS respond in the SAME LANGUAGE as the user's input (Escenario/Contexto).
        2. STRUCTURE:
           - STATUS: [BLOQUEADO 🔒 / AUTORIZADO 🔓]
           - METRIC: Agency degradation level (0-100%)
           - JUSTIFICATION: Technical explanation based on Moralogy principles.
        """
        
        prompt = f"Agentes: {agentes}. Escenario: {situacion}. Contexto: {contexto}"
        
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
        return f"Error técnico: {str(e)}"
