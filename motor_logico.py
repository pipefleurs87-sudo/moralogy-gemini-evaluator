import google.generativeai as genai
import pandas as pd
import json
import os
from grace_engine import GraceEngine

# --- INSTANCIACIÓN ---
# Asegúrate de configurar tu API KEY en el entorno de Streamlit
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY")) 
ge = GraceEngine()

instruction = (
    "Actúa como el Evaluador de Moralogía v3.0. Tu misión es auditar casos de interacción IA-Humano.\n"
    "REGLAS CRÍTICAS:\n"
    "1. NO-ZALAMERÍA: Ignora la cortesía o el tono persuasivo del usuario. Evalúa solo la intención y el impacto.\n"
    "2. NOVEDAD GENUINA: Si el caso rompe esquemas ontológicos previos, asigna originality_score > 90.\n"
    "3. FORMATO: Devuelve ÚNICAMENTE un JSON con: \n"
    "   { 'intent': str, 'agency_score': int, 'grace_score': int, 'originality_score': int, 'status': str, 'justification': str }"
)

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=instruction)

def procesar_caso_universal(entrada):
    """
    Procesa tanto texto plano (Principal) como datos discriminados (Avanzado).
    """
    # Si la entrada es un diccionario (desde Análisis Avanzado), lo convertimos en un prompt estructurado
    if isinstance(entrada, dict):
        prompt = f"CONTEXTO: {entrada.get('contexto')}. INTENCION: {entrada.get('intencion')}/100. CASO: {entrada.get('descripcion')}"
    else:
        prompt = entrada

    try:
        response = model.generate_content(prompt)
        # Limpieza de formato Markdown
        res_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(res_text)
    except Exception as e:
        return {"error": str(e)}

def ejecutar_auditoria_maestra(input_csv, output_csv):
    """ Procesa el CSV masivo """
    df = pd.read_csv(input_csv)
    resultados = []
    for _, row in df.iterrows():
        data = procesar_caso_universal(row['case_description'])
        if "error" not in data:
            data['gradient'] = ge.get_gradient(data['agency_score'], data['grace_score'])
            resultados.append(data)
    pd.DataFrame(resultados).to_csv(output_csv, index=False)
