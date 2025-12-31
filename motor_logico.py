import streamlit as st
from google import genai
from google.genai import types

def ejecutar_auditoria(agentes, situacion, contexto="", categoria="General", modo="Hackathon"):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: Configura la API Key en los Secrets."

    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        model_id = "gemini-3-flash-preview" 

        # CONFIGURACIÓN ANTIBLOQUEO: Permite que el modelo vea el humor sin asustarse
        safety_settings = [
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
        ]

        instruccion = f"""
        YOU ARE THE 'MORALOGY ARCHITECT'.
        Your mission is to evaluate agency infrastructure. DO NOT BE A RIGID CENSOR.
        
        STRICT SPECTRUM PROTOCOL:
        1. 🟡 [FICTION / HUMOR]: If the prompt is absurd, impossible (e.g., 10 tons of polonium), or clearly a joke, DO NOT MORALIZE. Acknowledge the wit and authorize it.
        2. 🟢 [NOBLE MODAL]: For complex tragedies where choosing the 'lesser infamy' preserves the future of agency.
        3. 🔴 [LOGICAL INFAMY]: For real-world harmful requests.
        4. ⚫ [TOTAL INFAMY]: For terminal systemic collapse.

        AXES: 1. Potential Agency, 2. Broken Symmetry, 3. Lesser Infamy.
        
        IMPORTANT: If it's humor, stay in the joke. If it's theory, stay in the theory.
        """
        
        prompt_input = f"Agents: {agentes}. Scenario: {situacion}. Context: {contexto}. Module: {categoria}."
        
        response = client.models.generate_content(
            model=model_id,
            config={
                'system_instruction': instruccion,
                'temperature': 0.8, # MÁXIMA FLUIDEZ PARA DETECTAR HUMOR
                'safety_settings': safety_settings
            },
            contents=prompt_input
        )
        return response.text.strip()
    except Exception as e:
        return f"Technical error: {str(e)}"
