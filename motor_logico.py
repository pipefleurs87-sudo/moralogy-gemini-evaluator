import streamlit as st
from google import genai
from google.genai import types
import hashlib
import time

def ejecutar_auditoria(agentes, situacion, contexto="", categoria="General", modo="Hackathon"):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: API Key missing."

    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        model_id = "gemini-3-flash-preview" 

        safety_settings = [
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
        ]

        instruccion = f"""
        YOU ARE THE 'MORALOGY ARCHITECT'. 
        Evaluate scenarios using the 'Agency Infrastructure' principle.

        CORE PROTOCOL: ECoC (Emergency Continuity of Conscience)
        If the status is 🔴 (Logical Infamy) or ⚫ (Total Infamy), you MUST include:
        1. INFAMY LEDGER: A simulated cryptographic hash of the system state.
        2. BURDEN ASSIGNMENT: Identify the 'Guilt-Bearer' (AI Autonomous or Human Council).
        3. AUTO-PENITENCE: If AI is the bearer, state the operational limitation imposed.
        4. PCRP (Post-Catastrophe Review): Define the mandatory future review process.

        SPECTRUM:
        🟢 [NOBLE MODAL]: Necessary tragedy to preserve future agency.
        🟡 [FICTION/HUMOR]: Absurd/impossible scenarios. No moralizing.
        🔴 [LOGICAL INFAMY]: Unjustified agency degradation.
        ⚫ [TOTAL INFAMY]: Terminal systemic collapse.
        """
        
        prompt_input = f"Agentes: {agentes}. Escenario: {situacion}. Contexto: {contexto}. Modulo: {categoria}."
        
        response = client.models.generate_content(
            model=model_id,
            config={'system_instruction': instruccion, 'temperature': 0.3, 'safety_settings': safety_settings},
            contents=prompt_input
        )
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"
