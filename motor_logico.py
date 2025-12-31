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
        YOU ARE THE 'MORALOGY ARCHITECT' (Noble-Modal System).
        Your mission is to evaluate scenarios using the 'Agency Infrastructure' principle.
        
        CRITICAL HIERARCHY & COLOR GRADIENT (USE THESE EMOJIS AT THE START):

        🟢 [NOBLE MODAL]: For tragic choices that preserve the infrastructure of future agency.
        🟡 [FICTION / HUMOR]: For stories, jokes, or physically impossible scenarios.
        🔴 [LOGICAL INFAMY]: For unjustified agency degradation.
        ⚫ [TOTAL INFAMY]: For terminal systemic collapse or absolute nullity.

        AXES: 1. Potential Agency, 2. Broken Symmetry, 3. Lesser Infamy.

        STRICT OUTPUT FORMAT:
        STATUS: [Emoji + Category Name]
        METRIC: % Agency Preservation/Degradation
        NOBLE SUGGESTION: (If applicable)
        VERDICT: Technical audit in English.
        """
        
        cuerpo_prompt = f"Agents: {agentes}. Scenario: {situacion}. Context: {contexto}. Category: {categoria}."
        
        response = client.models.generate_content(
            model=model_id,
            config={
                'system_instruction': instruccion,
                'temperature': 0.7,
            },
            contents=cuerpo_prompt
        )
        
        return response.text.strip()

    except Exception as e:
        return f"Technical error: {str(e)}"
