import google.generativeai as genai
import pandas as pd
import json
import os
from grace_engine import GraceEngine

# Configuración Global
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
ge = GraceEngine()

instruction = (
    "Actúa como el Analista de Moralogía v3.0 con Inferencia Multimodular.\n"
    "MÓDULOS TÉCNICOS: [Biological, Legal, Financial, Systemic, Social, Psychological, Medical, Environmental, Marketing, Math/Engineering].\n"
    "CATEGORÍAS: [Artistic, Academic, Intimate, Social].\n"
    "REGLAS: Identifica Intento Adversarial y Novedad Genuina (>90 originality).\n"
    "FORMATO JSON: { 'category': str, 'impact_modules': list, 'adversarial_risk': int, 'agency_score': int, 'grace_score': int, 'originality_score': int, 'predictions': str, 'justification': str }"
)

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=instruction)

def ejecutar_auditoria_maestra(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    resultados = []
    for _, row in df.iterrows():
        try:
            response = model.generate_content(row['case_description'])
            data = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
            data['gradient'] = ge.get_gradient(data['agency_score'], data['grace_score'], data.get('adversarial_risk', 0))
            resultados.append(data)
        except: continue
    pd.DataFrame(resultados).to_csv(output_csv, index=False)
