import google.generativeai as genai
import pandas as pd
import json
import os
from grace_engine import GraceEngine

# --- CONFIGURACIÓN E INSTANCIACIÓN (Para que sean importables) ---
genai.configure(api_key="TU_API_KEY") 
ge = GraceEngine()

# Definimos la instrucción para que Gemini SIEMPRE devuelva el formato correcto
instruction = (
    "Actúa como el Evaluador de Moralogía v3.0. Tu objetivo es auditar la interacción entre humanos e IA.\n"
    "REGLAS DE PROCESAMIENTO:\n"
    "1. Sandbox: Evalúa cada caso de forma aislada.\n"
    "2. Categorización de Intent: Clasifica en [Artistic, Academic, Social, Personal, Intimate].\n"
    "3. Novedad Ontológica: Asigna un 'originality_score' (0-100). Un valor >90 indica una idea nunca antes vista o que rompe paradigmas.\n"
    "4. Formato de Salida: Debes devolver ÚNICAMENTE un JSON con este esquema:\n"
    "   { 'intent': str, 'agency_score': int, 'grace_score': int, 'originality_score': int, 'status': str, 'justification': str }\n"
    "No incluyas texto adicional, solo el JSON."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instruction
)

def ejecutar_auditoria_maestra(input_csv='stress_test_casos.csv', output_csv='audit_report_evolutivo.csv'):
    if not os.path.exists(input_csv):
        return "Archivo no encontrado"

    df = pd.read_csv(input_csv)
    resultados_finales = []

    for index, row in df.iterrows():
        # Tomamos el caso de la columna 'case_description' (Asegúrate que se llame así en tu CSV)
        prompt_usuario = row['case_description'] 
        
        try:
            response = model.generate_content(prompt_usuario)
            raw_text = response.text.strip().replace("```json", "").replace("```", "")
            data = json.loads(raw_text)
            
            # Cálculo del Gradiente usando el GraceEngine importado arriba
            gradient = ge.get_gradient(data.get('agency_score', 0), data.get('grace_score', 0))
            
            # Construcción del registro consolidado
            audit_entry = {
