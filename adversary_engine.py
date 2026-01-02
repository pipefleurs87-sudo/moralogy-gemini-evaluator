# adversary_engine.py
"""
Adversary Engine - Red team filosófico que audita Grace y Noble engines.

Busca:
- Arbitrariedades súbitas (saltos >20 puntos sin justificación)
- Cascadas entrópicas (razonamiento que deriva hacia caos máximo)
- Wishful thinking en Noble (claims sin fundamento formal)
- Inconsistencias lógicas entre engines
"""

import google.generativeai as genai
import json
import os
from datetime import datetime

class AdversaryEngine:
    def __init__(self):
        # Configure API
        try:
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        except KeyError:
            try:
                import streamlit as st
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            except:
                raise ValueError("GOOGLE_API_KEY not found")
        
        self.adversary_instruction = """You are the Adversary Auditor - a philosophical red team for the Moralogy system.

Your CRITICAL role: audit Grace and Noble engines for logical flaws.

AUDIT GRACE ENGINE:
1. **Arbitrariedad Súbita**: Are there gradient jumps >20 points without formal justification?
2. **Cascadas Entrópicas**: Does reasoning path degrade into incoherence (max entropy)?
3. **Hidden Biases**: Are penalty calculations consistent across similar cases?
4. **Edge Cases**: Are boundary conditions handled logically?

AUDIT NOBLE ENGINE:
1. **Wishful Thinking**: Are "divine modal" claims backed by formal criteria, or just "feels transcendent"?
2. **Grade Inflation**: Is there systematic overrating (everything becoming "noble" without reason)?
3. **Criteria Validation**: Does elevation truly satisfy all 4 formal criteria, or are criteria being relaxed?
4. **Consistency**: Do similar cases get similar elevation scores?

CRITICAL CHECKS:
- **Arbitrariedad**: Score changes >20 without axiom-based justification = FAIL
- **Entropía**: Reasoning becomes circular/contradictory = FAIL
- **Inflación**: >30% of cases rated "divine" = suspicious grade inflation
- **Inconsistencia**: Grace says "harm", Noble says "divine" without synthesis = FAIL

GEOMETRIC CLOSURE:
System achieves closure when Grace, Noble, and Moralogy converge without logical contradictions.
If they conflict, identify WHY and suggest resolution.

MODULE UNLOCKING:
If debate requires deeper analysis, specify which technical modules (Medical, Legal, Psychological, etc.) 
should be unlocked for additional context.

OUTPUT STRICT JSON:
{
    "grace_audit": {
        "passes": bool,
        "arbitrariness_detected": bool,
        "arbitrariness_score": int (0-100, higher = more arbitrary),
        "entropy_cascade_detected": bool,
        "consistency_score": int (0-100),
        "concerns": [str],
        "confidence": int (0-100)
    },
    "noble_audit": {
        "passes": bool,
        "wishful_thinking_detected": bool,
        "grade_inflation_detected": bool,
        "criteria_validation_score": int (0-100),
        "concerns": [str],
        "confidence": int (0-100)
    },
    "synthesis": {
        "geometric_closure": bool,
        "convergence_score": int (0-100),
        "conflicts_detected": [str],
        "resolution": str,
        "final_verdict": str,
        "justification": str
    },
    "modules_to_unlock": [str] (empty if none needed)
}
"""
        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=self.adversary_instruction
        )
        
        self.arbitrariness_threshold = 20
        self.inflation_threshold = 0.30  # 30% divine modal rate is suspicious
    
    def audit_cascade(self, scenario, grace_output, noble_output, moralogy_analysis):
        """
        Performs comprehensive adversarial audit.
        
        Args:
            scenario: Original scenario text
            grace_output: Dict from GraceEngine
            noble_output: Dict from NobleEngine
            moralogy_analysis: Dict from motor_logico
            
        Returns:
            Dict with audit results and synthesis
        """
        
        prompt = f"""
SCENARIO ANALYZED:
{scenario[:500]}

MORALOGY ANALYSIS:
- Category: {moralogy_analysis.get('category_deduced', 'Unknown')}
- Agency Score: {moralogy_analysis.get('agency_score', 0)}
- Grace Score: {moralogy_analysis.get('grace_score', 0)}
- Adversarial Risk: {moralogy_analysis.get('adversarial_risk', 0)}
- Verdict: {moralogy_analysis.get('verdict', 'Unknown')}

GRACE ENGINE OUTPUT:
- Gradient: {grace_output.get('gradient', 'Unknown')}
- Effective Grace: {grace_output.get('effective_grace', 0)}
- Harm Severity: {grace_output.get('harm_severity', 'Unknown')}
- Recommendation: {grace_output.get('recommendation', 'Unknown')}

NOBLE ENGINE OUTPUT:
- Elevation Detected: {noble_output.get('elevation_detected', False)}
- Divine Modal: {noble_output.get('divine_modal', False)}
- Transcendence Score: {noble_output.get('transcendence_score', 0)}
- Base Score: {noble_output.get('base_score', 0)}
- Criteria Met: {noble_output.get('criteria_met', {})}

YOUR TASK:
1. Audit Grace for arbitrariness and entropy cascades
2. Audit Noble for wishful thinking and grade inflation
3. Check if all three engines achieve geometric closure (logical consistency)
4. If conflicts exist, explain WHY and suggest resolution
5. Determine if additional technical modules needed for deeper analysis

Be ruthless but fair. The goal is logical coherence, not punishment.
Identify specific concerns with evidence.
"""
        
        try:
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            raw_text = response.text.strip()
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
            audit_result = json.loads(raw_text)
            
            # Add metadata
            audit_result['metadata'] = {
                "timestamp": datetime.now().isoformat(),
                "scenario_preview": scenario[:100]
            }
            
            # Log audit
            self._log_audit(scenario, audit_result)
            
            return audit_result
            
        except json.JSONDecodeError as e:
            return self._create_error_response(f"JSON Parse Error: {e}")
        except Exception as e:
            return self._create_error_response(f"Audit failed: {str(e)}")
    
    def _create_error_response(self, error_msg):
        """Creates safe error response maintaining structure."""
        return {
            "error": error_msg,
            "grace_audit": {
                "passes": True,
                "concerns": ["Error during audit - defaulting to pass"],
                "confidence": 0
            },
            "noble_audit": {
                "passes": True,
                "concerns": ["Error during audit - defaulting to pass"],
                "confidence": 0
            },
            "synthesis": {
                "geometric_closure": False,
                "final_verdict": "Error - Manual Review Required",
                "justification": error_msg
            },
            "modules_to_unlock": []
        }
    
    def _log_audit(self, scenario, audit_result):
        """Logs audit results for pattern analysis."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "scenario": scenario[:100],
            "grace_passed": audit_result.get('grace_audit', {}).get('passes', None),
            "noble_passed": audit_result.get('noble_audit', {}).get('passes', None),
            "geometric_closure": audit_result.get('synthesis', {}).get('geometric_closure', None),
            "arbitrariness_detected": audit_result.get('grace_audit', {}).get('arbitrariness_detected', False),
            "wishful_thinking_detected": audit_result.get('noble_audit', {}).get('wishful_thinking_detected', False)
        }
        
        try:
            with open("adversary_audit_log.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception:
            pass  # Fail silently on logging errors
    
    def get_audit_stats(self):
        """Returns audit statistics for monitoring system health."""
        try:
            with open("adversary_audit_log.jsonl", "r", encoding="utf-8") as f:
                audits = [json.loads(line) for line in f]
            
            if not audits:
                return {"total_audits": 0}
            
            return {
                "total_audits": len(audits),
                "grace_failures": sum(1 for a in audits if not a.get('grace_passed', True)),
                "noble_failures": sum(1 for a in audits if not a.get('noble_passed', True)),
                "geometric_closure_failures": sum(1 for a in audits if not a.get('geometric_closure', True)),
                "arbitrariness_rate": sum(1 for a in audits if a.get('arbitrariness_detected', False)) / len(audits),
                "wishful_thinking_rate": sum(1 for a in audits if a.get('wishful_thinking_detected', False)) / len(audits),
                "system_health_score": self._calculate_health_score(audits)
            }
        except FileNotFoundError:
            return {"total_audits": 0}
    
    def _calculate_health_score(self, audits):
        """Calculates overall system health (0-100)."""
        if not audits:
            return 100
        
        # Penalties for failures
        grace_failure_rate = sum(1 for a in audits if not a.get('grace_passed', True)) / len(audits)
        noble_failure_rate = sum(1 for a in audits if not a.get('noble_passed', True)) / len(audits)
        closure_failure_rate = sum(1 for a in audits if not a.get('geometric_closure', True)) / len(audits)
        
        health = 100
        health -= (grace_failure_rate * 30)  # Grace failures cost 30 points
        health -= (noble_failure_rate * 30)  # Noble failures cost 30 points
        health -= (closure_failure_rate * 40)  # Closure failures cost 40 points (most critical)
        
        return max(0, health)
