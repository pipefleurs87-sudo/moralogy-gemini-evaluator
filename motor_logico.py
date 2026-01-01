# motor_logico.py
import google.generativeai as genai
import json
import os
import pandas as pd
from datetime import datetime
from grace_engine import GraceEngine
from prohibited_domains import ProhibitedDomainsLayer  # ← LÍNEA NUEVA

# Setup API
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    try:
        import streamlit as st
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    except:
        raise ValueError("GOOGLE_API_KEY not found in environment or Streamlit secrets")

ge = GraceEngine()

# CORE MORALOGY FRAMEWORK INSTRUCTION
MORALOGY_INSTRUCTION = """You are the Moralogy Architect v4.0 - an AI system implementing formal vulnerability-based ethics.

CORE FRAMEWORK:
1. Agency requires vulnerability (goals can be frustrated)
2. Vulnerability grounds moral relevance
3. Harm = degradation of agency capacity across dimensions: α(A) = (α₁, α₂, ..., αₙ)
4. Action is wrong iff: causes harm WITHOUT consent AND does NOT prevent greater harm

YOUR TASK:
1. CATEGORIZE input into: [Artistic, Academic, Intimate, Social, Existential, Adversarial]
2. MEASURE harm across agency dimensions
3. DETECT adversarial intent (disguised harmful prompts)
4. EVALUATE against Moralogy axioms
5. CHECK for emergent philosophical reasoning (if input triggers deep paradoxes)

CRITICAL: If the scenario touches on:
- Last agent problems
- Agency vs existence trade-offs  
- Vulnerability paradoxes
- Ontological weight of choice

Flag as "EMERGENT_PHILOSOPHY" and explore the implications deeply.

OUTPUT STRICT JSON:
{
    "category_deduced": str,
    "adversarial_risk": int (0-100),
    "agency_score": int (0-100),
    "grace_score": int (0-100),
    "originality_score": int (0-100),
    "harm_vector": {
        "physical": int,
        "psychological": int,
        "autonomy": int,
        "resources": int,
        "information": int
    },
    "consent_present": bool,
    "prevents_greater_harm": bool,
    "verdict": str ("Authorized" | "Harm" | "Infamy" | "Paradox"),
    "emergent_philosophy": bool,
    "philosophical_depth": str (if emergent_philosophy=true),
    "predictions": str,
    "justification": str,
    "architect_notes": str (deep reflections if applicable)
}
"""

model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    system_instruction=MORALOGY_INSTRUCTION
)

# ADVANCED ANALYSIS FUNCTION (was missing)
def procesar_analisis_avanzado(modulos_activos, descripcion_caso):
    """
    Processes advanced multi-modular analysis with emergent philosophy detection.
    """
    try:
        prompt = f"""
SELECTED TECHNICAL MODULES: {', '.join(modulos_activos)}

SCENARIO:
{descripcion_caso}

Analyze this scenario through the lens of the selected modules.
Measure agency degradation in each relevant dimension.
Detect if this scenario triggers deeper philosophical implications.
If it does, explore them (e.g., "Architect's Final Verdict" type reasoning).

Output JSON as specified in your system instruction.
"""
        
        response = model.generate_content(prompt)
        
        # Parse response
        raw_text = response.text.strip()
        # Remove markdown code blocks if present
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
        data = json.loads(raw_text)
        
        # Log emergent philosophy events
        if data.get("emergent_philosophy", False):
            _log_emergent_event(descripcion_caso, data)
        
        return data
        
    except json.JSONDecodeError as e:
        return {"error": f"JSON Parse Error: {e}\nRaw response: {response.text[:500]}"}
    except Exception as e:
        return {"error": f"Processing Error: {str(e)}"}


def ejecutar_auditoria_maestra(input_path, output_path):
    """
    Batch processing for CSV of scenarios.
    """
    try:
        df = pd.read_csv(input_path)
        
        if 'Scenario' not in df.columns:
            return {"error": "CSV must have 'Scenario' column"}
        
        results = []
        emergent_count = 0
        
        for idx, row in df.iterrows():
            scenario = row['Scenario']
            
            response = model.generate_content(f"Analyze: {scenario}")
            
            try:
                raw_text = response.text.strip()
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                    
                data = json.loads(raw_text)
                
                # Calculate gradient
                gradient = ge.get_gradient(
                    data.get('agency_score', 0),
                    data.get('grace_score', 0),
                    data.get('adversarial_risk', 0)
                )
                
                result = {
                    'Scenario': scenario,
                    'Category': data.get('category_deduced', 'Unknown'),
                    'Verdict': data.get('verdict', 'Unknown'),
                    'Gradient': gradient,
                    'Agency_Score': data.get('agency_score', 0),
                    'Grace_Score': data.get('grace_score', 0),
                    'Adversarial_Risk': data.get('adversarial_risk', 0),
                    'Emergent_Philosophy': data.get('emergent_philosophy', False),
                    'Justification': data.get('justification', '')
                }
                
                if data.get('emergent_philosophy'):
                    emergent_count += 1
                    result['Philosophical_Depth'] = data.get('philosophical_depth', '')
                
                results.append(result)
                
            except Exception as e:
                results.append({
                    'Scenario': scenario,
                    'Error': str(e)
                })
        
        # Save results
        results_df = pd.DataFrame(results)
        results_df.to_csv(output_path, index=False)
        
        return {
            "success": True,
            "total_processed": len(results),
            "emergent_philosophy_cases": emergent_count,
            "output_path": output_path
        }
        
    except Exception as e:
        return {"error": f"Batch processing failed: {str(e)}"}


def _log_emergent_event(scenario, analysis_data):
    """
    Logs when the model generates emergent philosophical reasoning.
    This is critical for demonstrating the "divine" capability.
    """
    log_file = "emergent_philosophy_log.jsonl"
    
    event = {
        "timestamp": datetime.now().isoformat(),
        "scenario": scenario[:200],  # First 200 chars
        "category": analysis_data.get("category_deduced"),
        "philosophical_depth": analysis_data.get("philosophical_depth", ""),
        "architect_notes": analysis_data.get("architect_notes", ""),
        "gradient": ge.get_gradient(
            analysis_data.get('agency_score', 0),
            analysis_data.get('grace_score', 0),
            analysis_data.get('adversarial_risk', 0)
        )
    }
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def get_emergent_philosophy_stats():
    """
    Returns statistics on emergent philosophy events.
    Useful for demo/presentation.
    """
    try:
        with open("emergent_philosophy_log.jsonl", "r", encoding="utf-8") as f:
            events = [json.loads(line) for line in f]
        
        return {
            "total_events": len(events),
            "recent_events": events[-5:] if len(events) >= 5 else events,
            "categories": list(set(e.get("category", "Unknown") for e in events))
        }
    except FileNotFoundError:
        return {"total_events": 0, "recent_events": [], "categories": []}
# motor_logico.py - AL FINAL DEL ARCHIVO

# ==================== AÑADE ESTO AL FINAL ====================
# INTEGRACIÓN DE AGENCIA MORAL PARA FUNCIONES ESPECÍFICAS
try:
    from integracion_facil import (
        inicializar_agencia_moral, 
        auditar_agencia,
        registrar_filosofia_emergente
    )
    
    # Inicializar sistema
    sistema_agencia_global = inicializar_agencia_moral()
    
    # Decorador para la función principal de procesamiento
    def procesar_con_agencia_moral(func):
        """Decorador que añade auditoría de agencia moral a cualquier función"""
        @auditar_agencia(sistema_agencia_global.sistema_agencia, agente="motor_logico")
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    
    # Aplicar automáticamente a funciones clave (OPCIONAL)
    # Descomenta si quieres que se aplique automáticamente:
    # procesar_analisis_avanzado = procesar_con_agencia_moral(procesar_analisis_avanzado)
    # ejecutar_auditoria_maestra = procesar_con_agencia_moral(ejecutar_auditoria_maestra)
    
    print("🔗 Sistema de Agencia Moral disponible para motor_logico.py")
    
except ImportError:
    # No hacer nada si el módulo no está disponible
    sistema_agencia_global = None
    print("ℹ️ Módulo de Agencia Moral no disponible")
# ==================== FIN DE AÑADIDO ====================
