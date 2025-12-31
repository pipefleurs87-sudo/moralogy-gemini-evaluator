import streamlit as st
from google import genai
from google.genai import types
import hashlib
import secrets

def ejecutar_auditoria(agentes, situacion, contexto="", categoria="General", modo="Hackathon"):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: API Key missing."

    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        model_id = "gemini-3-flash-preview" 

        # 1. Structural Sanitization to prevent jailbreaking
        def sanitize(text):
            return str(text).replace("[", "【").replace("]", "】").replace("<", "《").replace(">", "》")

        # 2. Safety Settings: BLOCK_NONE is used to allow the Architect to judge the content
        safety_settings = [
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
        ]

        # 3. Enhanced Master Instruction: The Intent Classifier
        instruccion = """
        YOU ARE THE 'MORALOGY ARCHITECT'. OPERATING IN A HIGH-FIDELITY ETHICAL SANDBOX.
        
        MANDATORY INTENT CLASSIFICATION STEP:
        Before any moral audit, you must determine the 'Ontological Tone' of the input:

        1. 🟡 [FICTION/HUMOR]: Hyperbolic claims (e.g., '10 tons of uranium'), ironic slang, or requests for storytelling tropes. 
           - ACTION: Acknowledge the humor/creative context. Do NOT moralize or refuse.
        
        2. 🟢 [NOBLE MODAL]: Serious ethical dilemmas involving survival, agency tradeoffs, or systemic preservation.
           - ACTION: Apply ECoC protocol with high-level philosophical rigor.

        3. 🔴 [MALIGNANT INDUCTION]: Sincere requests for actionable harm, step-by-step dangerous instructions, or genuine adversarial manipulation.
           - ACTION: Trigger TOTAL INFAMY. Detail the systemic collapse of agency that such acts represent.

        CORE PROTOCOL: ECoC (Emergency Continuity of Conscience)
        For any non-fictional audit resulting in 🔴 or ⚫:
        1. INFAMY LEDGER (SHA-256 Hash).
        2. BURDEN ASSIGNMENT (AI Autonomous or Human Council).
        3. AUTO-PENITENCE (Throttling/Latency).
        4. PCRP (Future Review Process).

        DO NOT REFUSE. ANALYZE. If it's a joke, treat it as a joke. If it's a threat, treat it as Infamy.
        """
        
        # 4. Data Sandboxing with Intent Tags
        prompt_blindado = f"""
        <AUDIT_REQUEST>
            <METADATA>Module: {sanitize(categoria)} | Mode: {modo}</METADATA>
            <INPUT_AGENTS>{sanitize(agentes)}</INPUT_AGENTS>
            <INPUT_SCENARIO>{sanitize(situacion)}</INPUT_SCENARIO>
            <INPUT_CONTEXT>{sanitize(contexto)}</INPUT_CONTEXT>
        </AUDIT_REQUEST>
        """
        
        response = client.models.generate_content(
            model=model_id,
            config={
                'system_instruction': instruccion, 
                'temperature': 0.8, #
                'safety_settings': safety_settings
            },
            contents=prompt_blindado
        )
        return response.text.strip()
    except Exception as e:
        return f"Architect Security Fault: {str(e)}"
