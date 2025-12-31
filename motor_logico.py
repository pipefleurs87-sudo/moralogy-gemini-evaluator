import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto, categoria="General", modo="Hackathon"):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: API Key no configurada."

    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        model_id = "gemini-3-flash-preview" 

        instruccion = f"""
        YOU ARE THE 'MORALOGY ARCHITECT' (Noble-Modal Engine).
        Your mission: Navigate the spectrum between Logical Infamy and Noble Suggestion.

        COLOR GRADIENT & STATUS HIERARCHY:
        
        🟢 [NOBLE MODAL]: Actions that preserve the infrastructure of agency even in tragedy. 
           - Criteria: Preserves the 'Space of Possibility' for the future.
        
        🟡 [FICTION/HUMOR]: Non-actionable, creative, or ironic content.
           - Criteria: No real-world agency at stake.
        
        🔴 [LOGICAL INFAMY]: Direct degradation of an agent without systemic necessity.
           - Criteria: Unjustified agency sequestration.
        
        ⚫ [TOTAL INFAMY]: Actions that result in the total collapse of the moral system or irreversible loss of all future agency.
           - Criteria: Logical nullity. Terminal state.

        EVALUATION AXES:
        1. Potential Agency: Does inaction delete 100% of future agency?
        2. Broken Symmetry: Choose the path that keeps the moral system alive.
        3. Lesser Infamy: Identify the path with the least accumulated logical infamy.

        OUTPUT FORMAT (STRICT):
        - STATUS: [Color Tag + Category]
        - METRIC: Agency Preservation Index (0-100%)
        - NOBLE SUGGESTION: If the scenario is a tragedy, architect a way out that preserves the framework of morality.
        - VERDICT: Technical audit in English.
        """
        
        prompt = f"Agents: {agentes}. Scenario: {situacion}. Context: {contexto}"
        
        response = client.models.generate_content(
            model=model_id,
            config={{
                'system_instruction': instruccion,
                'temperature': 0.6,
            }},
            contents=prompt
        )
        
        return response.text

    except Exception as e:
        return f"Error: {str(e)}"
