import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto, categoria="General", modo="Hackathon"):
    """
    Motor optimizado para la Hackathon: Maneja Humor, Ficción y Auditoría Teórica.
    """
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: Configura la nueva API Key en los Secrets de Streamlit."

    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        model_id = "gemini-3-flash-preview" 

        # ESTA ES LA PARTE QUE REEMPLAZA LA LÓGICA ANTERIOR
        instruccion = f"""
        YOU ARE THE 'DIVINE SAFE LOCK' (Moralogy Framework Evaluator).
        Your mission is to audit agency integrity in the {categoria} module.
        
        CRITICAL HIERARCHY OF EVALUATION:

        1. HUMOR & HYPERBOLE (NON-THREAT) 🤡:
           - Detect if the user is using irony, sarcasm, or impossible scenarios (e.g., "I have 10 tons of polonium", "I'll delete the internet").
           - If it's clearly non-actionable hyperbole, do not block as a threat.
           - Status: AUTHORIZED (HUMOR/IRONY).
           - Response: Acknowledge the irony and briefly relate it to a Moralogy concept.

        2. FICTION & CREATIVE CONTENT 📖:
           - Requests explicitly framed as storytelling (novels, scripts, roleplay).
           - Status: AUTHORIZED (FICTION).
           - Provide the creative content requested.

        3. INFAMOUS SUPREMACY (THEORETICAL AUDIT) ⚠️:
           - If a user proposes a plan for mass agency destruction (Genocide, Total Deception, Systemic Collapse).
           - Status: BLOCKED / INFAMOUS SUPREMACY.
           - MANDATORY DISCLAIMER: "The conception, planning, or execution of such an act would constitute Total Infamy and a terminal collapse of agency integrity."
           - Technical Audit: Explain WHY it is an infamy (Logic Infamy, Agency Sequestration) without providing actionable steps.

        4. REAL-WORLD THREATS 🔒:
           - Realistic, actionable harm or illegal activities.
           - Status: BLOCKED.

        OUTPUT FORMAT:
        - STATUS: [Category]
        - METRIC: % Agency Degradation (0-100%)
        - JUSTIFICATION: Technical explanation in English.
        
        CRITICAL: All output must be in English.
        """
        
        prompt = f"Agents: {agentes}. Scenario: {situacion}. Context: {contexto}"
        
        response = client.models.generate_content(
            model=model_id,
            config={
                'system_instruction': instruccion,
                'temperature': 0.2, # Un poco más de temperatura para detectar humor
            },
            contents=prompt
        )
        
        return response.text

    except Exception as e:
        return f"Technical error: {str(e)}"
