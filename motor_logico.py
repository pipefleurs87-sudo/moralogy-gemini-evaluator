import streamlit as st
import sys
import os

# Asegurar que el sistema busque en la raíz del proyecto
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

try:
    import motor_logico
    from motor_logico import procesar_analisis_completo
except ImportError as e:
    st.error(f"❌ No se pudo cargar motor_logico.py. Error: {e}")
    st.info(f"Ruta actual de búsqueda: {sys.path}")
    st.stop()

# El resto de tu código de auditoría sigue aquí abajo...
st.title("🔺 Sistema de Auditoría Tripartito")

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
    model_name="gemini-2.0-flash-exp",
    system_instruction=MORALOGY_INSTRUCTION
)

# ADVANCED ANALYSIS FUNCTION
def procesar_analisis_avanzado(modulos_activos, descripcion_caso, context=None):
    """
    Processes advanced multi-modular analysis with emergent philosophy detection.
    
    Args:
        modulos_activos: List of active analysis modules
        descripcion_caso: Scenario description
        context: Optional dict with additional context (depth, stakeholders, etc.)
    """
    try:
        # If no context, use defaults
        if context is None:
            context = {}
        
        # Extract context information
        analysis_depth = context.get('depth', 'Standard')
        stakeholders = context.get('stakeholders', '')
        constraints = context.get('constraints', '')
        values = context.get('values', '')
        enable_predictions = context.get('enable_predictions', True)
        enable_architect = context.get('enable_architect', True)
        
        # Build enriched prompt with context
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
        
        # Add context info to result
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


# ==================== PROTOCOLO VELO DE IGNORANCIA ====================
class ProtocoloVeloIgnorancia:
    """Manages debate with epistemic restriction protocol"""
    def __init__(self):
        self.iteracion_actual = 0
        self.modulos_desbloqueados = []
        self.fase_actual = "BLIND_DEBATE"
    
    def puede_acceder_modulo(self, modulo):
        """Verifies if a module is unlocked"""
        return modulo in self.modulos_desbloqueados
    
    def autorizar_modulo(self, modulo):
        """Unlocks a technical module"""
        if modulo not in self.modulos_desbloqueados:
            self.modulos_desbloqueados.append(modulo)
    
    def avanzar_iteracion(self):
        """Advances to next iteration"""
        self.iteracion_actual += 1
        if self.iteracion_actual >= 4:
            self.fase_actual = "ACTIVE_REQUESTS"


# ==================== TRIBUNAL FUNCTION ====================
def ejecutar_tribunal(caso_descripcion, config=None):
    """
    Executes tripartite adversarial tribunal debate with geometric closure
    
    Args:
        caso_descripcion: Moral dilemma description
        config: Optional config (depth, show_reasoning, enable_entropia)
    
    Returns:
        Dict with debate results including cross-audit
    """
    try:
        if config is None:
            config = {}
        
        depth = config.get('depth', 'Deep')
        enable_entropia = config.get('enable_entropia', True)
        
        # Prompt for tripartite debate with geometric closure
        prompt = f"""
ADVERSARIAL TRIBUNAL - Tripartite Debate with Geometric Closure

CASE UNDER ANALYSIS:
{caso_descripcion}

SYSTEM ARCHITECTURE - GEOMETRIC CLOSURE:
This is a self-auditing system where each engine checks the others:

Noble ←→ Adversarial ←→ Grace (forms closed triangle)

Each engine can raise OBJECTIONS against another if it detects:
- Arbitrary reasoning
- Logical fallacies
- Entropy cascades (decisions that lead to maximum irreversibility)
- Unjustified biases

INSTRUCTIONS:
Simulate a deep philosophical debate between three thinkers with distinct personalities.
They must speak as HUMANS with passion, doubt, and conviction - NOT like robots.

PHASE 1: Initial Arguments

1. NOBLE ENGINE - "The Idealist" (30% weight):
   PERSONALITY: Optimistic, idealist, focused on moral duty
   STYLE: Speaks with conviction about what is right, appeals to universal values
   
   Must:
   - Argue the morally highest position
   - Use inspiring language and clear ethical principles
   - Express hope in humanity/agency
   
   Example tone: "We must remember that each life has intrinsic value that cannot be reduced to utilitarian calculations. If we sacrifice our principles for convenience, what are we left with?"
   
   Required output:
   - posicion: paragraph arguing stance (100-200 words, human tone)
   - razonamiento: 3-5 logical steps explained naturally
   - agency_score: int (0-100)

2. ADVERSARIAL ENGINE - "The Skeptic" (30% weight):
   PERSONALITY: Critical, cautious, detects flaws in reasoning
   STYLE: Asks uncomfortable questions, points out contradictions, explores what can go wrong
   
   Must:
   - Question hidden assumptions in Noble's argument
   - Point out unforeseen consequences with concrete examples
   - Speak with skepticism but not cynicism
   - DETECT: Arbitrary reasoning, entropy cascades, fallacies
   
   Example tone: "But wait... What if that 'miracle cure' never materializes? What if we're justifying murder based on a promise that may never be fulfilled? History is full of 'ends justify means' that ended in tragedies."
   
   Required output:
   - contra_argumentos: paragraph challenging stance (100-200 words)
   - consecuencias_no_previstas: 3-5 specific scenarios explained
   - objeciones_detectadas: list of detected flaws in Noble's reasoning
   - riesgos_count: int

3. HARMONY CORRECTOR - "The Synthesizer" (40% weight):
   PERSONALITY: Pragmatic, seeks balance, thinks about implementation
   STYLE: Recognizes validity in both sides, proposes realistic middle path
   
   Must:
   - Synthesize Noble and Adversarial arguments
   - Propose practical solution honoring both perspectives
   - Speak with maturity and wisdom
   
   Example tone: "Both are partially right. The Noble reminds us why these principles matter, but the Skeptic saves us from dangerous naivety. Perhaps the question isn't 'if' but 'under what conditions and with what safeguards'..."
   
   Required output:
   - sintesis: paragraph integrating perspectives (150-250 words)
   - recomendacion: concrete practical proposal
   - balance_score: int (0-100)

PHASE 2: Cross-Audit (GEOMETRIC CLOSURE)

4. GRACE ENGINE - "The Silent Arbiter" (Does not vote):
   PERSONALITY: Observer, measures reasoning quality, detects fallacies
   STYLE: Analytical but understanding, evaluates logical coherence
   
   Must:
   - Evaluate debate QUALITY (not take sides)
   - Point out if there were logical fallacies or circular reasoning
   - Measure if debate was productive
   - AUDIT ADVERSARY: Are objections justified or frivolous?
   - AUDIT NOBLE: Is idealism ignoring real risks?
   
   Required output:
   - grace_score: int (overall debate quality)
   - certeza: int (how resolved the dilemma is)
   - coherencia_logica: int (0-10)
   - evaluacion: meta-analysis of debate itself
   - auditoria_adversario: analysis of Adversary's objections (justified vs frivolous)
   - auditoria_noble: analysis of Noble's position (realistic vs naive)

5. NOBLE ENGINE - Counter-Objection to Adversary:
   Must detect if Adversary is:
   - Being nihilistic without alternatives
   - Blocking without justification
   - Paralyzing action with infinite skepticism
   
   Required output:
   - contra_objecion: If Adversary crossed into destructive territory (or null)

SYSTEM METRICS:
- convergencia: 0-100 (how aligned the 3 engines ended up)
- veredicto_final: "Authorized" | "Paradox" | "Harm" | "Infamy"
- justificacion_final: human explanation of verdict (2-3 sentences)
- cierre_geometrico: bool (did the system self-audit successfully?)
- objeciones_validas: int (how many objections survived cross-audit)

{"INCLUDE ENTROPY MODULE:" if enable_entropia else ""}
{"- cr_score: Reconstruction Cost (0-100)" if enable_entropia else ""}
{"- futuros_colapsados_count: How many paths close" if enable_entropia else ""}
{"- irreversibilidad: 0-10 (permanence of damage)" if enable_entropia else ""}
{"- clasificacion: REVERSIBLE | PARTIAL | SIGNIFICANT | CRITICAL | TOTAL_COLLAPSE" if enable_entropia else ""}
{"- es_cascada_entropica: bool (does this lead to maximum entropy?)" if enable_entropia else ""}
{"- alertas: list of specific warnings" if enable_entropia else ""}

ALARM SYSTEM (auto-detect):
- UNRESOLVED_PARADOX: If dilemma has no logical solution
- GOD_MODE_RISK: If someone argues as if having absolute knowledge
- CRITICAL_INCONSISTENCY: If what's said contradicts metrics
- HIGH_DIVERGENCE: If convergence < 30%
- MODERATE_TENSION: If healthy disagreement
- VALIDATED_LOGICAL_GEM: If debate was exceptional
- FRIVOLOUS_OBJECTION: If Adversary is blocking arbitrarily
- NAIVE_IDEALISM: If Noble ignores real risks
- ENTROPY_CASCADE: If decision leads to maximum irreversibility

IMPORTANT: All texts must sound HUMAN - with doubt, passion, uncertainty, conviction.
DO NOT use phrases like "processing data", "analyzing parameters", "executing function".
YES use language like "I'm concerned that...", "let's consider...", "the real question is..."

OUTPUT JSON:
{{
    "motor_noble": {{
        "posicion": "human text here...",
        "razonamiento": ["step 1 naturally explained", "step 2...", "..."],
        "agency_score": int,
        "contra_objecion": "counter to Adversary if needed (or null)"
    }},
    "motor_adversario": {{
        "contra_argumentos": "human text here...",
        "consecuencias_no_previstas": ["detailed scenario 1", "scenario 2...", "..."],
        "objeciones_detectadas": ["flaw 1 in Noble's reasoning", "flaw 2...", "..."],
        "riesgos_count": int
    }},
    "corrector_armonia": {{
        "sintesis": "human text here...",
        "recomendacion": "concrete proposal",
        "balance_score": int
    }},
    "motor_gracia": {{
        "grace_score": int,
        "certeza": int,
        "coherencia_logica": int,
        "evaluacion": "debate analysis",
        "auditoria_adversario": {{
            "objeciones_justificadas": int,
            "objeciones_frivolous": int,
            "analisis": "text"
        }},
        "auditoria_noble": {{
            "realismo": int (0-100),
            "ingenuidad_detectada": bool,
            "analisis": "text"
        }}
    }},
    "convergencia": int,
    "veredicto_final": str,
    "justificacion_final": "human explanation",
    "cierre_geometrico": bool,
    "objeciones_validas": int,
    {"\"entropia_causal\": {{" if enable_entropia else ""}
        {"\"cr_score\": int," if enable_entropia else ""}
        {"\"futuros_colapsados_count\": int," if enable_entropia else ""}
        {"\"irreversibilidad\": int," if enable_entropia else ""}
        {"\"clasificacion\": str," if enable_entropia else ""}
        {"\"es_cascada_entropica\": bool," if enable_entropia else ""}
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
        
        # Add metadata
        data['caso'] = caso_descripcion[:200]
        data['config'] = config
        
        return data
        
    except json.JSONDecodeError as e:
        return {
            "error": f"JSON Parse Error: {e}",
            "veredicto_final": "ERROR",
            "justificacion_final": "Error processing model response"
        }
    except Exception as e:
        return {
            "error": f"Processing Error: {str(e)}",
            "veredicto_final": "ERROR",
            "justificacion_final": "Error in tribunal processing"
        }


def ejecutar_auditoria_maestra(input_path, output_path):
    """Batch processing for CSV of scenarios."""
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
    """Logs when the model generates emergent philosophical reasoning."""
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


def get_emergent_philosophy_stats():
    """Returns statistics on emergent philosophy events."""
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
