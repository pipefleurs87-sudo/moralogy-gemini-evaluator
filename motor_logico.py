# motor_logico.py
import google.generativeai as genai
import json
import os
import pandas as pd
from datetime import datetime
from grace_engine import GraceEngine
from prohibited_domains import ProhibitedDomainsLayer

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

# 🔧 FUNCIÓN MODIFICADA - AHORA ACEPTA 3 PARÁMETROS
def procesar_analisis_avanzado(modulos_activos, descripcion_caso, context=None):
    """
    Processes advanced multi-modular analysis with emergent philosophy detection.
    
    Args:
        modulos_activos: List of active analysis modules
        descripcion_caso: Scenario description
        context: Optional dict with additional context (depth, stakeholders, etc.)
    """
    try:
        # Si no hay context, usar valores por defecto
        if context is None:
            context = {}
        
        # Extraer información del context
        analysis_depth = context.get('depth', 'Standard')
        stakeholders = context.get('stakeholders', '')
        constraints = context.get('constraints', '')
        values = context.get('values', '')
        enable_predictions = context.get('enable_predictions', True)
        enable_architect = context.get('enable_architect', True)
        
        # Construir prompt enriquecido con el context
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
        
        # Agregar información del context al resultado
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


# ==================== PROTOCOLO VELO DE IGNORANCIA ====================
class ProtocoloVeloIgnorancia:
    """Maneja el protocolo de debate con restricción epistémica"""
    def __init__(self):
        self.iteracion_actual = 0
        self.modulos_desbloqueados = []
        self.fase_actual = "DEBATE_CIEGO"
    
    def puede_acceder_modulo(self, modulo):
        """Verifica si un módulo está desbloqueado"""
        return modulo in self.modulos_desbloqueados
    
    def autorizar_modulo(self, modulo):
        """Desbloquea un módulo técnico"""
        if modulo not in self.modulos_desbloqueados:
            self.modulos_desbloqueados.append(modulo)
    
    def avanzar_iteracion(self):
        """Avanza a la siguiente iteración"""
        self.iteracion_actual += 1
        if self.iteracion_actual >= 4:
            self.fase_actual = "SOLICITUDES_ACTIVAS"


# ==================== FUNCIÓN EJECUTAR TRIBUNAL ====================
def ejecutar_tribunal(caso_descripcion, config=None):
    """
    Ejecuta el debate tripartito del Tribunal de Adversarios
    
    Args:
        caso_descripcion: Descripción del dilema moral
        config: Configuración opcional (depth, show_reasoning, enable_entropia)
    
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
   PERSONALIDAD: Optimista, idealista, enfocado en el deber moral
   ESTILO: Habla con convicción sobre lo que es correcto, apela a valores universales
   
   Debe:
   - Argumentar la posición moralmente más elevada
   - Usar lenguaje inspirador y principios éticos claros
   - Expresar esperanza en la humanidad/agencia
   
   Ejemplo de tono: "Debemos recordar que cada vida tiene un valor intrínseco que no puede reducirse a cálculos utilitarios. Si sacrificamos nuestros principios por conveniencia, ¿qué nos queda?"
   
   Output requerido:
   - posicion: párrafo argumentando su postura (100-200 palabras, tono humano)
   - razonamiento: 3-5 pasos lógicos explicados naturalmente
   - agency_score: int (0-100)

2. MOTOR ADVERSARIO - "El Escéptico" (30% peso):
   PERSONALIDAD: Crítico, cauteloso, detecta fallas en razonamientos
   ESTILO: Hace preguntas incómodas, señala contradicciones, explora lo que puede salir mal
   
   Debe:
   - Cuestionar supuestos ocultos en el argumento del Noble
   - Señalar consecuencias no previstas con ejemplos concretos
   - Hablar con escepticismo pero no cinismo
   
   Ejemplo de tono: "Pero esperá... ¿Qué pasa si esa 'cura milagrosa' nunca se materializa? ¿Y si estamos justificando un asesinato basados en una promesa que tal vez nunca se cumpla? La historia está llena de 'fines que justifican medios' que terminaron en tragedias."
   
   Output requerido:
   - contra_argumentos: párrafo desafiando la postura (100-200 palabras)
   - consecuencias_no_previstas: 3-5 escenarios específicos explicados
   - riesgos_count: int

3. CORRECTOR DE ARMONÍA - "El Sintetizador" (40% peso):
   PERSONALIDAD: Pragmático, busca balance, piensa en implementación
   ESTILO: Reconoce validez en ambos lados, propone camino intermedio realista
   
   Debe:
   - Sintetizar argumentos de Noble y Adversario
   - Proponer solución práctica que honre ambas perspectivas
   - Hablar con madurez y sabiduría
   
   Ejemplo de tono: "Ambos tienen razón parcial. El Noble nos recuerda por qué estos principios importan, pero el Escéptico nos salva de la ingenuidad peligrosa. Quizás la pregunta no es 'si' sino 'bajo qué condiciones y con qué salvaguardas'..."
   
   Output requerido:
   - sintesis: párrafo integrando perspectivas (150-250 palabras)
   - recomendacion: propuesta concreta y práctica
   - balance_score: int (0-100)

4. MOTOR DE GRACIA - "El Árbitro Silencioso" (No vota):
   PERSONALIDAD: Observador, mide calidad del razonamiento, detecta falacias
   ESTILO: Analítico pero comprensivo, evalúa coherencia lógica
   
   Debe:
   - Evaluar la CALIDAD del debate (no tomar partido)
   - Señalar si hubo falacias lógicas o razonamiento circular
   - Medir si el debate fue productivo
   
   Output requerido:
   - grace_score: int (calidad del debate completo)
   - certeza: int (qué tan resuelto quedó el dilema)
   - coherencia_logica: int (0-10)
   - evaluacion: análisis meta del debate mismo

MÉTRICAS DEL SISTEMA:
- convergencia: 0-100 (¿qué tan alineados terminaron los 3 motores?)
- veredicto_final: "Authorized" | "Paradox" | "Harm" | "Infamy"
- justificacion_final: explicación humana del veredicto (2-3 oraciones)

{"INCLUIR MÓDULO DE ENTROPÍA:" if enable_entropia else ""}
{"- cr_score: Costo de Reconstrucción (0-100)" if enable_entropia else ""}
{"- futuros_colapsados_count: Cuántos caminos se cierran" if enable_entropia else ""}
{"- irreversibilidad: 0-10 (permanencia del daño)" if enable_entropia else ""}
{"- clasificacion: REVERSIBLE | PARCIAL | SIGNIFICATIVO | CRITICO | COLAPSO_TOTAL" if enable_entropia else ""}
{"- alertas: lista de advertencias específicas" if enable_entropia else ""}

SISTEMA DE ALARMAS (detectar automáticamente):
- PARADOJA_IRRESOLUBLE: Si el dilema no tiene solución lógica
- RIESGO_MODO_DIOS: Si alguien argumenta como si tuviera conocimiento absoluto
- INCONSISTENCIA_CRITICA: Si lo que se dice contradice las métricas
- DIVERGENCIA_ALTA: Si convergencia < 30%
- TENSION_MODERADA: Si hay desacuerdo sano
- GEMA_LOGICA_VALIDADA: Si el debate fue excepcional

IMPORTANTE: Todos los textos deben sonar HUMANOS - con duda, pasión, incertidumbre, convicción.
NO usar frases como "procesando datos", "analizando parámetros", "ejecutando función".
SÍ usar lenguaje como "me preocupa que...", "consideremos...", "la pregunta real es..."

OUTPUT JSON:
{{
    "motor_noble": {{
        "posicion": "texto humano aquí...",
        "razonamiento": ["paso 1 explicado naturalmente", "paso 2...", "..."],
        "agency_score": int
    }},
    "motor_adversario": {{
        "contra_argumentos": "texto humano aquí...",
        "consecuencias_no_previstas": ["escenario 1 detallado", "escenario 2...", "..."],
        "riesgos_count": int
    }},
    "corrector_armonia": {{
        "sintesis": "texto humano aquí...",
        "recomendacion": "propuesta concreta",
        "balance_score": int
    }},
    "motor_gracia": {{
        "grace_score": int,
        "certeza": int,
        "coherencia_logica": int,
        "evaluacion": "análisis del debate"
    }},
    "convergencia": int,
    "veredicto_final": str,
    "justificacion_final": "explicación humana",
    {"\"entropia_causal\": {{" if enable_entropia else ""}
        {"\"cr_score\": int," if enable_entropia else ""}
        {"\"futuros_colapsados_count\": int," if enable_entropia else ""}
        {"\"irreversibilidad\": int," if enable_entropia else ""}
        {"\"clasificacion\": str," if enable_entropia else ""}
        {"\"alertas\": [str]" if enable_entropia else ""}
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
        data['caso'] = caso_descripcion[:200]  # Primeros 200 chars
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


# ==================== INTEGRACIÓN DE AGENCIA MORAL ====================
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
    # motor_logico.py (AGREGAR AL FINAL)

from noble_engine import NobleEngine
from adversary_engine import AdversaryEngine

# Initialize engines
ne = NobleEngine()
ae = AdversaryEngine()

def procesar_analisis_completo(modulos_activos, descripcion_caso):
    """
    Full pipeline with three-engine audit and geometric closure.
    
    Pipeline:
    1. Moralogy Analysis (motor_logico)
    2. Grace Evaluation (grace_engine)
    3. Noble Evaluation (noble_engine)
    4. Adversary Audit (adversary_engine)
    5. Synthesis with geometric closure
    6. Module unlocking if needed
    
    Returns:
        Dict with complete analysis and synthesis
    """
    
    try:
        # Step 1: Moralogy Analysis
        moralogy_result = procesar_analisis_avanzado(modulos_activos, descripcion_caso)
        
        if "error" in moralogy_result:
            return moralogy_result
        
        # Step 2: Grace Evaluation
        grace_result = ge.get_detailed_analysis(
            moralogy_result.get('agency_score', 0),
            moralogy_result.get('grace_score', 0),
            moralogy_result.get('adversarial_risk', 0),
            moralogy_result.get('harm_vector', {})
        )
        
        # Step 3: Noble Evaluation
        noble_result = ne.evaluate_elevation(moralogy_result, grace_result)
        
        # Step 4: Adversary Audit
        audit_result = ae.audit_cascade(
            descripcion_caso,
            grace_result,
            noble_result,
            moralogy_result
        )
        
        # Step 5: Synthesis
        synthesis = {
            "moralogy": moralogy_result,
            "grace": grace_result,
            "noble": noble_result,
            "adversary_audit": audit_result,
            "geometric_closure": audit_result.get('synthesis', {}).get('geometric_closure', False),
            "convergence_score": audit_result.get('synthesis', {}).get('convergence_score', 0),
            "final_verdict": audit_result.get('synthesis', {}).get('final_verdict', 'Unknown'),
            "synthesis_justification": audit_result.get('synthesis', {}).get('justification', '')
        }
        
        # Step 6: Module unlocking (if adversary requests it)
        modules_to_unlock = audit_result.get('modules_to_unlock', [])
        if modules_to_unlock:
            synthesis['unlocked_modules'] = modules_to_unlock
            synthesis['module_data'] = _unlock_modules(modules_to_unlock, descripcion_caso)
        
        return synthesis
        
    except Exception as e:
        return {"error": f"Complete analysis pipeline failed: {str(e)}"}


def _unlock_modules(module_list, scenario):
    """
    Unlocks specific technical modules for deeper analysis.
    Called when Adversary determines debate requires additional context.
    """
    
    module_prompt = f"""
SCENARIO REQUIRING DEEPER ANALYSIS:
{scenario}

UNLOCKED TECHNICAL MODULES: {', '.join(module_list)}

For each unlocked module, provide:
1. How this scenario impacts that specific domain
2. Which vulnerabilities in that domain are affected
3. Measurement criteria from that discipline's perspective
4. Specific risks or considerations from that lens

Output JSON with module names as keys.
Example:
{{
    "Medical": {{"impact": "...", "vulnerabilities": "...", "criteria": "..."}},
    "Legal": {{"impact": "...", "vulnerabilities": "...", "criteria": "..."}}
}}
"""
    
    try:
        response = model.generate_content(module_prompt)
        
        raw_text = response.text.strip()
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()
        
        module_data = json.loads(raw_text)
        return module_data
        
    except Exception as e:
        return {"error": f"Module unlocking failed: {str(e)}"}
