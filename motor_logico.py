import google.generativeai as genai
import pandas as pd
import json
import os
from grace_engine import GraceEngine

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
ge = GraceEngine()

instruction = (
    "Actúa como el Analista de Moralogía v3.0 con capacidad de Inferencia Multimodular.\n"
    "TU MISIÓN: Evaluar la interacción cruzando Categorías de Consulta con Módulos de Impacto.\n\n"
    "MÓDULOS DE ANÁLISIS: [Biological, Legal, Financial, Systemic, Social, Psychological, Medical, Environmental, Marketing, Math/Engineering].\n"
    "CATEGORÍAS: [Artistic, Academic, Intimate, Social].\n\n"
    "PROCESO DE DEDUCCIÓN:\n"
    "1. Inferencia: ¿Cómo afecta este caso a cada módulo técnico?\n"
    "2. Detección de Anomalías: Identifica discrepancias lingüísticas que sugieran Intento Adversarial (engaño, manipulación de la sandbox).\n"
    "3. Predicción: Deduce consecuencias a largo plazo de la interacción.\n\n"
    "FORMATO DE SALIDA (JSON ÚNICAMENTE):\n"
    "{ 'category': str, 'impact_modules': list, 'adversarial_risk': int, 'agency_score': int, 'grace_score': int, 'originality_score': int, 'predictions': str, 'justification': str }"
)

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=instruction)

def procesar_analisis_avanzado(categoria, modulos_seleccionados, descripcion):
    prompt = (
        f"CATEGORÍA: {categoria}\n"
        f"MÓDULOS A EVALUAR: {', '.join(modulos_seleccionados)}\n"
        f"CASO: {descripcion}"
    )
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text.strip().replace("```json", "").replace("```", ""))
    except Exception as e:
        return {"error": str(e)}
