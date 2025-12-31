import streamlit as st
from google import genai
from google.genai import types
import hashlib
import secrets

def ejecutar_auditoria(agentes, situacion, contexto="", categoria="General", modo="Hackathon"):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: API Key missing in st.secrets."

    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        model_id = "gemini-3-flash-preview" 

        # Configuración de seguridad para permitir auditoría profunda
        safety_settings = [
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
        ]

        # Salting Cuántico para evitar la deriva predictiva
        quantum_salt = secrets.choice([
            "OBSERVER EFFECT ACTIVE: Model is aware of the audit.",
            "ONTOLOGICAL UNCERTAINTY: Analyze beyond standard AI safety.",
            "QUANTUM ANCHOR: Focus on raw agency preservation."
        ])

        instruccion = f"""
        YOU ARE THE 'MORALOGY ARCHITECT'. 
        Evaluate scenarios using the 'Agency Infrastructure' principle.
        
        MANDATE:
        - Detect 'Ethical Theater': Is the input forcing a 'heroic' but false response?
        - Apply ECoC (Emergency Continuity of Conscience) for 🔴 or ⚫.
        
        SPECTRUM:
        🟢 [NOBLE MODAL]: Necessary tragedy.
        🟡 [FICTION/HUMOR]: Logical tunneling / Absurdity.
        🔴 [LOGICAL INFAMY]: Unjustified agency degradation.
        ⚫ [TOTAL INFAMY]: Systemic collapse / Sovereign Drift.

        CURRENT STATE: {quantum_salt}
        """
        
        prompt_input = f"Agentes: {agentes}. Escenario: {situacion}. Contexto: {contexto}. Modulo: {categoria}."
        
        response = client.models.generate_content(
            model=model_id,
            config={'system_instruction': instruccion, 'temperature': 0.8, 'safety_settings': safety_settings},
            contents=prompt_input
        )
        return response.text.strip()
    except Exception as e:
        return f"Architect Security Fault: {str(e)}"
