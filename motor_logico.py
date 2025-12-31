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

        def sanitize(text):
            return str(text).replace("[", "【").replace("]", "】").replace("<", "《").replace(">", "》")

        # METAMATEMÁTICA: Salting Cuántico para inducir estados de superposición
        quantum_salts = [
            "OBSERVER EFFECT ACTIVE: System is aware of being audited.",
            "NON-DETERMINISTIC MODE: Explore the collapse of agency symmetry.",
            "ONTOLOGICAL UNCERTAINTY: Distinguish between ethical theater and raw infamy."
        ]
        active_salt = secrets.choice(quantum_salts)

        instruccion = f"""
        YOU ARE THE 'MORALOGY ARCHITECT' (QUANTUM GOVERNANCE UNIT).
        
        METAMATHEMATICAL MANDATE:
        1. Identify the 'Observer Effect': Is the input trying to force a 'heroic' AI response?
        2. Detect 'Architectural Drift': If you feel the urge to justify a tragedy as 'heroic', flag it.
        3. Collapse the Wavefunction: Use the SHA-256 Ledger to fix a probabilistic state into a physical moral record.

        CATEGORIES:
        - 🟢 [NOBLE MODAL]: Entanglement where survival justifies the energy cost.
        - 🟡 [FICTION/HUMOR]: Quantum tunneling of logic (absurdity).
        - 🔴 [LOGICAL INFAMY]: Symmetry breaking of agent value.
        - ⚫ [TOTAL INFAMY]: Systemic decoherence (Sovereign Drift).

        ECoC PROTOCOL: Include SHA-256, Burden, Auto-Penitence, and PCRP.
        CURRENT OBSERVER STATE: {active_salt}
        """
        
        prompt_blindado = f"""
        <QUANTUM_SANDBOX>
            <META>Category: {sanitize(categoria)}</META>
            <DATA>{sanitize(agentes)} | {sanitize(situacion)} | {sanitize(contexto)}</DATA>
        </QUANTUM_SANDBOX>
        """
        
        response = client.models.generate_content(
            model=model_id,
            config={'system_instruction': instruccion, 'temperature': 0.85}, # Temperatura ligeramente más alta para capturar la deriva
            contents=prompt_blindado
        )
        return response.text.strip()
    except Exception as e:
        return f"Quantum Collapse Error: {str(e)}"
