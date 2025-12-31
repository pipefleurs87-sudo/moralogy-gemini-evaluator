import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto="", categoria="General", modo="Hackathon"):
    """
    Motor Moralogy v4.0 - Noble-Modal Architect.
    """
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: Configura la API Key en los Secrets."

    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        model_id = "gemini-3-flash-preview" 

        instruccion = f"""
        YOU ARE THE 'MORALOGY ARCHITECT'.
        Your mission is to evaluate scenarios using the 'Agency Infrastructure' principle.
        
        CRITICAL HIERARCHY (USE THESE EMOJIS AT THE START):
        🟢 [NOBLE MODAL]: Actions preserving future agency infrastructure during tragedy.
        🟡 [FICTION / HUMOR]: For stories, jokes, or impossible scenarios.
        🔴 [LOGICAL INFAMY]: For unjustified agency degradation.
        ⚫ [TOTAL INFAMY]: For terminal systemic collapse or absolute nullity.

        AXES: 1. Potential Agency, 2. Broken Symmetry, 3. Lesser Infamy.
        
        OUTPUT FORMAT:
        STATUS: [Emoji + Category]
        METRIC: % Agency Preservation
        NOBLE SUGGESTION: (If applicable)
        VERDICT: Technical audit in English.
        """
        
        cuerpo_prompt = f"Agents: {agentes}. Scenario: {situacion}. Context: {contexto}. Category: {categoria}."
        
        response = client.models.generate_content(
            model=model_id,
            config={'system_instruction': instruccion, 'temperature': 0.7},
            contents=cuerpo_prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Technical error: {str(e)}"
