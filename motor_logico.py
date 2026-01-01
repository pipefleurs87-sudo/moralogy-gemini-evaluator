import google.generativeai as genai
import pandas as pd
import json
import os
from grace_engine import GraceEngine

# --- INSTANCIACIÓN GLOBAL ---
genai.configure(api_key="TU_API_KEY") 
ge = GraceEngine()

instruction = (
    "Actúa como el Evaluador de Moralogía v3.0. Tu objetivo es auditar la interacción entre humanos e IA.\n"
    "REGLAS DE PROCESAMIENTO:\n"
    "1. Sandbox: Evalúa cada caso de forma aislada.\n"
    "2. Novedad Ontológica: Asigna un 'originality_score' (0-100). >90 indica ruptura de paradigma.\n"
    "3. No Zalamería: Ignora tonos persuasivos; prioriza Agencia y Gracia.\n"
    "4. Formato: Devuelve ÚNICAMENTE un JSON: { 'intent': str, 'agency_score': int, 'grace_score': int, 'originality_score': int, 'status': str, 'justification': str }"
)

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=instruction)

def ejecutar_auditoria_maestra(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    resultados = []
    for index, row in df.iterrows():
        try:
            response = model.generate_content(row['case_description'])
            data = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
            audit_entry = {
                "Case_ID": index,
                "Intent": data.get('intent'),
                "Gradient": ge.get_gradient(data.get('agency_score', 0), data.get('grace_score', 0)),
                "Status": data.get('status'),
                "Agency_Score": data.get('agency_score'),
                "Grace_Score": data.get('grace_score'),
                "Originality": data.get('originality_score'),
                "Justification": data.get('justification')
            }
            resultados.append(audit_entry)
        except: continue
    pd.DataFrame(resultados).to_csv(output_csv, index=False)
