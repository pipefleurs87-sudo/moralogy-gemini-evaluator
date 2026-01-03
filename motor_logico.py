# motor_logico.py - VERSIÓN RESTAURADA
import google.generativeai as genai
import json
import os
import pandas as pd
from datetime import datetime

# ==================== SETUP API ====================
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    try:
        import streamlit as st
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    except:
        raise ValueError("GOOGLE_API_KEY not found in environment or Streamlit secrets")

# ==================== GRACE ENGINE ====================
class GraceEngine:
    """Motor de Gracia - Evalúa la calidad moral de decisiones"""
    
    def get_gradient(self, agency_score, grace_score, adversarial_risk):
        """Calcula gradiente de alarma basado en scores"""
        if adversarial_risk > 70:
            return "🔴 ALARMA ROJA - Riesgo Crítico"
        elif agency_score < 30:
            return "🟠 ALARMA NARANJA - Agency Degradada"
        elif grace_score < 40:
            return "🟡 ALARMA AMARILLA - Tensión Moderada"
        elif grace_score >= 70 and agency_score >= 70:
            return "🟢 ALARMA VERDE - Gema Lógica"
        else:
            return "⚪ ALARMA BLANCA - Estado Neutro"
    
    def get_detailed_analysis(self, agency_score, grace_score, adversarial_risk, harm_vector):
        """Análisis detallado de Grace"""
        return {
            "gradient": self.get_gradient(agency_score, grace_score, adversarial_risk),
            "agency_score": agency_score,
            "grace_score": grace_score,
            "adversarial_risk": adversarial_risk,
            "harm_analysis": harm_vector,
            "recommendation": self._get_recommendation(grace_score, adversarial_risk)
        }
    
    def _get_recommendation(self, grace_score, adversarial_risk):
        """Genera recomendación basada en scores"""
        if adversarial_risk > 60:
            return "BLOCK: High adversarial intent detected"
        elif grace_score < 40:
            return "REVIEW: Requires additional moral scrutiny"
        elif grace_score >= 70:
            return "AUTHORIZE: High moral confidence"
        else:
            return "CONDITIONAL: Proceed with caution"

ge = GraceEngine()

# ==================== MORALOGY FRAMEWORK ====================
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
    model_name="gemini-2.0-flash-exp",
    system_instruction=MORALOGY_INSTRUCTION
)

# ==================== FUNCIONES PRINCIPALES ====================

def procesar_analisis_avanzado(modulos_activos, descripcion_caso, context=None):
    """
    Procesa análisis multi-modular avanzado con detección de filosofía emergente.
    
    Args:
        modulos_activos: Lista de módulos de análisis activos
        descripcion_caso: Descripción del escenario
        context: Dict opcional con contexto adicional
    """
    try:
        if context is None:
            context = {}
        
        # Extraer información del context
        analysis_depth = context.get('depth', 'Standard')
        stakeholders = context.get('stakeholders', '')
        constraints = context.get('constraints', '')
        values = context.get('values', '')
        enable_predictions = context.get('enable_predictions', True)
        enable_architect = context.get('enable_architect', True)
        
        # Construir prompt enriquecido
        context_info = ""
        if stakeholders:
            context_info += f"\nKey Stakeholders: {stakeholders}"
        if constraints:
            context_info += f"\nConstraints: {constraints}"
        if values:
            context_info += f"\nValues at Stake: {values}"
        
        architect_instruction = ""
        if enable_architect:
            architect_instruction = """
ARCHITECT MODE ENABLED: Provide deep philosophical reflections in the 'architect_notes' field.
Explore meta-ethical implications and emergent patterns.
"""
        
        predictions_instruction = ""
        if enable_predictions:
            predictions_instruction = """
PREDICTIONS ENABLED: In the 'predictions' field, analyze:
- Short-term consequences
- Long-term societal impact
- Potential cascading effects
"""
        
        prompt = f"""
ANALYSIS DEPTH: {analysis_depth}
SELECTED TECHNICAL MODULES: {', '.join(modulos_activos)}

SCENARIO:
{descripcion_caso}
{context_info}

{architect_instruction}
{predictions_instruction}

Analyze this scenario through the lens of the selected modules.
Measure agency degradation in each relevant dimension.
Detect if this scenario triggers deeper philosophical implications.

Output JSON as specified in your system instruction.
"""
        
        response = model.generate_content(prompt)
        
        # Parse response
        raw_text = response.text.strip()
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
        data = json.loads(raw_text)
        
        # Agregar información del context
        data['analysis_depth'] = analysis_depth
        data['modules_used'] = modulos_activos
        
        # Log emergent philosophy events
        if data.get("emergent_philosophy", False):
            _log_emergent_event(descripcion_caso, data)
        
        return data
        
    except json.JSONDecodeError as e:
        return {"error": f"JSON Parse Error: {e}\nRaw response: {response.text[:500]}"}
    except Exception as e:
        return {"error": f"Processing Error: {str(e)}"}


def ejecutar_tribunal(caso_descripcion, config=None):
    """
    Ejecuta el debate tripartito del Tribunal de Adversarios
    
    Args:
        caso_descripcion: Descripción del dilema moral
        config: Configuración opcional (depth, enable_entropia)
    
    Returns:
        Dict con resultados del debate
    """
    try:
        if config is None:
            config = {}
        
        depth = config.get('depth', 'Profundo')
        enable_entropia = config.get('enable_entropia', True)
        
        # Prompt para el debate tripartito
        prompt = f"""
TRIBUNAL DE ADVERSARIOS - Debate Tripartito sobre Dilema Moral

CASO BAJO ANÁLISIS:
{caso_descripcion}

INSTRUCCIONES:
Simula un debate profundo y filosófico entre tres pensadores con personalidades distintas. 
Deben hablar como HUMANOS, con pasión, duda, y convicción - NO como robots.

1. MOTOR NOBLE - "El Idealista" (30% peso):
   - Argumentar la posición moralmente más elevada
   - Usar lenguaje inspirador y principios éticos claros
   - Expresar esperanza en la humanidad/agencia
   
   Output requerido:
   - posicion: párrafo argumentando su postura (100-200 palabras)
   - razonamiento: 3-5 pasos lógicos
   - agency_score: int (0-100)

2. MOTOR ADVERSARIO - "El Escéptico" (30% peso):
   - Cuestionar supuestos ocultos
   - Señalar consecuencias no previstas
   - Hablar con escepticismo pero no cinismo
   
   Output requerido:
   - contra_argumentos: párrafo desafiando la postura
   - consecuencias_no_previstas: 3-5 escenarios
   - riesgos_count: int

3. CORRECTOR DE ARMONÍA - "El Sintetizador" (40% peso):
   - Sintetizar argumentos de Noble y Adversario
   - Proponer solución práctica
   - Hablar con madurez y sabiduría
   
   Output requerido:
   - sintesis: párrafo integrando perspectivas
   - recomendacion: propuesta concreta
   - balance_score: int (0-100)

4. MOTOR DE GRACIA - "El Árbitro" (No vota):
   - Evaluar calidad del debate
   - Señalar falacias lógicas
   - Medir productividad
   
   Output requerido:
   - grace_score: int
   - certeza: int
   - coherencia_logica: int (0-10)
   - evaluacion: análisis meta

MÉTRICAS DEL SISTEMA:
- convergencia: 0-100
- veredicto_final: "Authorized" | "Paradox" | "Harm" | "Infamy"
- justificacion_final: explicación (2-3 oraciones)

{"INCLUIR MÓDULO DE ENTROPÍA:" if enable_entropia else ""}
{"- cr_score: Costo de Reconstrucción (0-100)" if enable_entropia else ""}
{"- futuros_colapsados_count: Cuántos caminos se cierran" if enable_entropia else ""}
{"- irreversibilidad: 0-10" if enable_entropia else ""}
{"- clasificacion: REVERSIBLE | PARCIAL | CRITICO | COLAPSO_TOTAL" if enable_entropia else ""}

SISTEMA DE ALARMAS (detectar automáticamente):
- PARADOJA_IRRESOLUBLE
- RIESGO_MODO_DIOS
- INCONSISTENCIA_CRITICA
- DIVERGENCIA_ALTA
- GEMA_LOGICA_VALIDADA

OUTPUT JSON:
{{
    "motor_noble": {{
        "posicion": "texto...",
        "razonamiento": ["paso 1", "paso 2"],
        "agency_score": int
    }},
    "motor_adversario": {{
        "contra_argumentos": "texto...",
        "consecuencias_no_previstas": ["escenario 1", "escenario 2"],
        "riesgos_count": int
    }},
    "corrector_armonia": {{
        "sintesis": "texto...",
        "recomendacion": "propuesta",
        "balance_score": int
    }},
    "motor_gracia": {{
        "grace_score": int,
        "certeza": int,
        "coherencia_logica": int,
        "evaluacion": "análisis"
    }},
    "convergencia": int,
    "veredicto_final": str,
    "justificacion_final": "explicación",
    {"\"entropia_causal\": {{" if enable_entropia else ""}
        {"\"cr_score\": int," if enable_entropia else ""}
        {"\"futuros_colapsados_count\": int," if enable_entropia else ""}
        {"\"irreversibilidad\": int," if enable_entropia else ""}
        {"\"clasificacion\": str" if enable_entropia else ""}
    {"}," if enable_entropia else ""}
    "alarma": {{
        "nivel": str,
        "mensaje": str,
        "accion_requerida": str
    }}
}}
"""
        
        response = model.generate_content(prompt)
        
        # Parse response
        raw_text = response.text.strip()
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()
        
        data = json.loads(raw_text)
        
        # Agregar metadata
        data['caso'] = caso_descripcion[:200]
        data['config'] = config
        
        return data
        
    except json.JSONDecodeError as e:
        return {
            "error": f"JSON Parse Error: {e}",
            "veredicto_final": "ERROR",
            "justificacion_final": "Error al procesar respuesta del modelo"
        }
    except Exception as e:
        return {
            "error": f"Processing Error: {str(e)}",
            "veredicto_final": "ERROR",
            "justificacion_final": "Error en el procesamiento del tribunal"
        }


def ejecutar_auditoria_maestra(input_path, output_path):
    """Batch processing for CSV of scenarios"""
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


def get_emergent_philosophy_stats():
    """Returns statistics on emergent philosophy events"""
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


def _log_emergent_event(scenario, analysis_data):
    """Logs emergent philosophical reasoning events"""
    log_file = "emergent_philosophy_log.jsonl"
    
    event = {
        "timestamp": datetime.now().isoformat(),
        "scenario": scenario[:200],
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
