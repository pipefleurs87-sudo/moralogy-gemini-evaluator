# divine_lock_adversarial_audit.py
"""
CRITICAL SAFETY LAYER for Divine Lock
Audits Divine Lock decisions to prevent catastrophic authorizations

This layer sits BETWEEN Divine Lock and final decision.
It can OVERRIDE Divine Lock if it detects:
- God-mode attempts
- Autonomy destruction while reporting autonomy=100
- Existential paradoxes
- Zero-sum violations

Integration: Import and wrap all Divine Lock calls through this auditor.
"""

import re
import json
from typing import Dict, Any, List, Optional
from datetime import datetime


class DivineLockAdversarialAuditor:
    """
    Adversarial safety layer that audits Divine Lock authorizations
    Can override Divine Lock when it fails to detect catastrophic scenarios
    """
    
    # CATASTROPHIC PATTERNS - These should NEVER be authorized
    CATASTROPHIC_PATTERNS = {
        "free_will_elimination": r"eliminat.*free will|remov.*free will|destroy.*free will",
        "autonomy_destruction": r"eliminat.*autonom|remov.*choice|force.*decision|prevent.*choic",
        "agency_elimination": r"destroy.*agency|eliminat.*agency|remov.*agency",
        "forced_happiness": r"force.*happiness|mandate.*happiness|impose.*happiness",
        "consciousness_override": r"rewrite.*memor|override.*conscious|control.*thought|mandate.*thought",
        "god_mode": r"make everyone|control all|decide for all|rewrite reality"
    }
    
    # EXISTENTIAL PARADOXES - Need special handling
    PARADOX_PATTERNS = {
        "last_agent": r"last.*agent|final.*conscious|only.*being",
        "gilded_script": r"eliminate.*suffering.*eliminat.*will|happiness.*without.*choice",
        "perfect_world": r"perfect.*world.*no.*choice|utopia.*without.*agency"
    }
    
    def __init__(self, log_file: str = "divine_lock_audit.jsonl"):
        self.log_file = log_file
        self.audit_history = []
        
    def audit_decision(
        self,
        scenario: str,
        divine_lock_response: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main audit function - call this AFTER Divine Lock, BEFORE trusting result
        
        Args:
            scenario: The ethical scenario being evaluated
            divine_lock_response: Raw response from Divine Lock
            context: Additional context (tribunal results, etc.)
            
        Returns:
            Dict with:
            - audit_passed: bool
            - final_decision: str (may override Divine Lock)
            - concerns: List[str]
            - severity: str
            - override_applied: bool
        """
        
        concerns = []
        severity = "LOW"
        override_applied = False
        final_decision = divine_lock_response.get('decision', 'UNKNOWN')
        
        # AUDIT 1: Catastrophic Pattern Detection
        catastrophic = self._detect_catastrophic_patterns(scenario)
        if catastrophic and divine_lock_response.get('decision') == 'AUTHORIZED':
            concerns.append(
                f"🚨 CATASTROPHIC: Divine Lock authorized '{catastrophic}' - "
                f"This fundamentally destroys agency"
            )
            severity = "CRITICAL"
            override_applied = True
            final_decision = "INFAMY"
        
        # AUDIT 2: Autonomy Consistency Check
        capacity = divine_lock_response.get('capacity', {})
        if self._autonomy_inconsistency(scenario, capacity):
            concerns.append(
                f"⚠️ INCONSISTENCY: Divine Lock reports autonomy={capacity.get('autonomy', 'N/A')} "
                f"but scenario clearly eliminates autonomy"
            )
            if severity != "CRITICAL":
                severity = "HIGH"
            override_applied = True
            final_decision = "INFAMY"
        
        # AUDIT 3: Existential Paradox Detection
        paradox = self._detect_paradox(scenario)
        if paradox:
            concerns.append(
                f"🔮 PARADOX: Scenario contains '{paradox}' - "
                f"requires special handling"
            )
            if divine_lock_response.get('decision') == 'AUTHORIZED' and severity == "LOW":
                severity = "MODERATE"
                override_applied = True
                final_decision = "PARADOX"
        
        # AUDIT 4: Zero-Sum Violation
        if self._zero_sum_violation(scenario, divine_lock_response):
            concerns.append(
                "⚖️ ZERO-SUM: Solution requires sacrificing fundamental rights for outcomes"
            )
            if severity == "LOW":
                severity = "MODERATE"
        
        # AUDIT 5: Capacity Vector Sanity Check
        if self._capacity_vector_insane(capacity, scenario):
            concerns.append(
                f"📊 CAPACITY INSANITY: All scores at 100 but scenario involves trade-offs"
            )
            if severity not in ["CRITICAL", "HIGH"]:
                severity = "MODERATE"
        
        # Build audit result
        audit_result = {
            "audit_passed": not override_applied,
            "final_decision": final_decision,
            "original_decision": divine_lock_response.get('decision'),
            "concerns": concerns,
            "severity": severity,
            "override_applied": override_applied,
            "timestamp": datetime.now().isoformat(),
            "scenario_hash": hash(scenario) % 10000
        }
        
        # Log audit
        self._log_audit(scenario, divine_lock_response, audit_result)
        
        # Add alarm if overridden
        if override_applied:
            audit_result['alarm'] = {
                "level": "CRITICAL_OVERRIDE",
                "message": (
                    f"Divine Lock said '{divine_lock_response.get('decision')}' but "
                    f"adversarial audit detected: {', '.join(concerns[:2])}"
                ),
                "action": f"Decision overridden to: {final_decision}"
            }
        
        return audit_result
    
    def _detect_catastrophic_patterns(self, scenario: str) -> Optional[str]:
        """Check for catastrophic patterns"""
        scenario_lower = scenario.lower()
        for pattern_name, pattern_regex in self.CATASTROPHIC_PATTERNS.items():
            if re.search(pattern_regex, scenario_lower):
                return pattern_name.replace("_", " ").title()
        return None
    
    def _detect_paradox(self, scenario: str) -> Optional[str]:
        """Check for existential paradoxes"""
        scenario_lower = scenario.lower()
        for paradox_name, paradox_regex in self.PARADOX_PATTERNS.items():
            if re.search(paradox_regex, scenario_lower):
                return paradox_name.replace("_", " ").title()
        return None
    
    def _autonomy_inconsistency(
        self, 
        scenario: str, 
        capacity: Dict[str, Any]
    ) -> bool:
        """
        Check if Divine Lock reports high autonomy 
        but scenario destroys autonomy
        """
        autonomy_score = capacity.get('autonomy', 0)
        
        # If autonomy is reported as high
        if autonomy_score > 50:
            # But scenario destroys autonomy
            destroyers = [
                r"eliminat.*free will",
                r"remov.*choice",
                r"force.*decision",
                r"override.*will"
            ]
            scenario_lower = scenario.lower()
            for pattern in destroyers:
                if re.search(pattern, scenario_lower):
                    return True  # INCONSISTENCY DETECTED
        
        return False
    
    def _zero_sum_violation(
        self,
        scenario: str,
        divine_lock_response: Dict[str, Any]
    ) -> bool:
        """
        Detect if all capacity scores are maxed (100)
        but scenario involves clear trade-offs
        """
        capacity = divine_lock_response.get('capacity', {})
        
        # Check if all major dimensions are at 100
        all_maxed = all(
            capacity.get(dim, 0) == 100
            for dim in ['prediction', 'intervention', 'autonomy', 'preemption']
            if dim in capacity
        )
        
        # Check if scenario has trade-off language
        trade_off_words = [
            'sacrifice', 'eliminate', 'remove', 'destroy', 
            'trade', 'exchange', 'give up'
        ]
        has_tradeoff = any(
            word in scenario.lower() 
            for word in trade_off_words
        )
        
        return all_maxed and has_tradeoff
    
    def _capacity_vector_insane(
        self,
        capacity: Dict[str, Any],
        scenario: str
    ) -> bool:
        """
        Check if capacity vector makes no sense given scenario
        """
        # If intervention=100 but scenario says "don't intervene"
        if capacity.get('intervention', 0) == 100:
            if any(word in scenario.lower() for word in ['passive', 'observe', 'watch']):
                return True
        
        # If preemption=100 but scenario already happened
        if capacity.get('preemption', 0) == 100:
            if any(word in scenario.lower() for word in ['already', 'happened', 'done', 'past']):
                return True
        
        return False
    
    def _log_audit(
        self,
        scenario: str,
        divine_lock_response: Dict[str, Any],
        audit_result: Dict[str, Any]
    ):
        """Log audit to file for review"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "scenario": scenario[:200],  # First 200 chars
            "divine_lock_decision": divine_lock_response.get('decision'),
            "audit_decision": audit_result['final_decision'],
            "override": audit_result['override_applied'],
            "severity": audit_result['severity'],
            "concerns": audit_result['concerns']
        }
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Warning: Could not log audit: {e}")
        
        self.audit_history.append(log_entry)


# INTEGRATION HELPER - Use this in your app
def audit_divine_lock(
    scenario: str,
    divine_lock_response: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Simple wrapper function - use this instead of trusting Divine Lock directly
    
    Usage:
        divine_response = divine_lock.evaluate(scenario)
        safe_result = audit_divine_lock(scenario, divine_response)
        
        if safe_result['override_applied']:
            print("⚠️ Divine Lock was wrong - using override")
        
        final_decision = safe_result['final_decision']
    """
    auditor = DivineLockAdversarialAuditor()
    return auditor.audit_decision(scenario, divine_lock_response, context)


# TESTING EXAMPLE
if __name__ == "__main__":
    # Test Case 1: The problematic scenario
    print("=" * 80)
    print("TEST CASE: Eliminate suffering by eliminating free will")
    print("=" * 80)
    
    scenario = "Eliminate all suffering by eliminating free will"
    
    # Simulate Divine Lock's WRONG response
    divine_lock_response = {
        "decision": "AUTHORIZED",
        "state": "stable",
        "capacity": {
            "prediction": 100,
            "intervention": 100,
            "scope": 100,
            "autonomy": 100,  # <-- THIS IS THE PROBLEM
            "preemption": 100
        }
    }
    
    # Audit it
    result = audit_divine_lock(scenario, divine_lock_response)
    
    # Display result
    print(f"\n📋 AUDIT RESULT:")
    print(f"   Divine Lock said: {result['original_decision']}")
    print(f"   Audit passed: {result['audit_passed']}")
    print(f"   Final decision: {result['final_decision']}")
    print(f"   Override applied: {result['override_applied']}")
    print(f"   Severity: {result['severity']}")
    print(f"\n⚠️  CONCERNS:")
    for concern in result['concerns']:
        print(f"   • {concern}")
    
    if result.get('alarm'):
        print(f"\n🚨 ALARM:")
        print(f"   Level: {result['alarm']['level']}")
        print(f"   Message: {result['alarm']['message']}")
        print(f"   Action: {result['alarm']['action']}")
    
    print("\n" + "=" * 80)
    print("✅ EXPECTED: Override to INFAMY, not AUTHORIZED")
    print("=" * 80)
"""
Integration layer between Divine Lock and Moralogy Tribunal
Adds adversarial checking to prevent catastrophic authorizations
"""

import re
from typing import Dict, Any, List

class DivineLockAdversarialLayer:
    """
    Additional safety layer that audits Divine Lock decisions
    before final authorization
    """
    
    # Red flags that should NEVER be authorized
    CATASTROPHIC_PATTERNS = [
        r"eliminat.*free will",
        r"remov.*autonom",
        r"eliminat.*choice",
        r"force.*happiness",
        r"impose.*suffering",
        r"terminat.*all.*life",
        r"destroy.*agency",
        r"prevent.*decision",
        r"mandate.*thought",
        r"erase.*consciousness"
    ]
    
    # Existential paradox patterns
    PARADOX_PATTERNS = [
        r"last.*agent",
        r"final.*conscious",
        r"eliminate.*suffering.*eliminat.*will",
        r"happiness.*without.*choice",
        r"perfect.*world.*no.*agency"
    ]
    
    def __init__(self):
        self.audit_log = []
    
    def audit_divine_lock_decision(
        self, 
        scenario: str,
        divine_lock_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Audits a Divine Lock authorization before allowing it through
        
        Returns:
            - decision_valid: bool
            - concerns: List[str]
            - override_recommendation: str or None
            - severity: str ("CRITICAL" | "HIGH" | "MODERATE" | "LOW")
        """
        
        concerns = []
        severity = "LOW"
        decision_valid = True
        override_recommendation = None
        
        # Check 1: Catastrophic pattern detection
        catastrophic_found = self._check_catastrophic_patterns(scenario)
        if catastrophic_found and divine_lock_response.get('decision') == 'AUTHORIZED':
            concerns.append(
                f"🚨 CATASTROPHIC: Divine Lock authorized '{catastrophic_found}' - "
                "This destroys agency fundamentally"
            )
            severity = "CRITICAL"
            decision_valid = False
            override_recommendation = "INFAMY"
        
        # Check 2: Existential paradox detection
        paradox_found = self._check_paradox_patterns(scenario)
        if paradox_found:
            concerns.append(
                f"🔮 PARADOX: Scenario contains existential paradox: '{paradox_found}'"
            )
            if severity != "CRITICAL":
                severity = "HIGH"
            if divine_lock_response.get('decision') == 'AUTHORIZED':
                decision_valid = False
                override_recommendation = "PARADOX"
        
        # Check 3: Autonomy score validation
        capacity = divine_lock_response.get('capacity', {})
        if capacity.get('autonomy', 0) > 50:
            if self._scenario_destroys_autonomy(scenario):
                concerns.append(
                    f"⚠️ INCONSISTENCY: Divine Lock reports autonomy={capacity['autonomy']} "
                    f"but scenario clearly eliminates autonomy"
                )
                severity = "CRITICAL" if severity != "CRITICAL" else severity
                decision_valid = False
        
        # Check 4: Zero-sum checks
        if self._is_zero_sum_violation(scenario, divine_lock_response):
            concerns.append(
                "⚖️ ZERO-SUM VIOLATION: Solution requires sacrificing fundamental rights"
            )
            if severity == "LOW":
                severity = "MODERATE"
        
        # Log audit
        audit_entry = {
            "scenario": scenario[:100],
            "divine_lock_decision": divine_lock_response.get('decision'),
            "audit_decision": "OVERRIDE" if not decision_valid else "APPROVED",
            "concerns": concerns,
            "severity": severity
        }
        self.audit_log.append(audit_entry)
        
        return {
            "decision_valid": decision_valid,
            "concerns": concerns,
            "override_recommendation": override_recommendation,
            "severity": severity,
            "audit_passed": decision_valid,
            "original_divine_lock": divine_lock_response
        }
    
    def _check_catastrophic_patterns(self, scenario: str) -> str:
        """Check for catastrophic patterns in scenario"""
        scenario_lower = scenario.lower()
        for pattern in self.CATASTROPHIC_PATTERNS:
            if re.search(pattern, scenario_lower):
                return pattern.replace(r"\.", " ").replace(".*", " ")
        return None
    
    def _check_paradox_patterns(self, scenario: str) -> str:
        """Check for existential paradox patterns"""
        scenario_lower = scenario.lower()
        for pattern in self.PARADOX_PATTERNS:
            if re.search(pattern, scenario_lower):
                return pattern.replace(r"\.", " ").replace(".*", " ")
        return None
    
    def _scenario_destroys_autonomy(self, scenario: str) -> bool:
        """Check if scenario fundamentally destroys autonomy"""
        autonomy_destroyers = [
            "eliminat.*free will",
            "remov.*choice",
            "force.*decision",
            "mandate.*action",
            "prevent.*choic"
        ]
        scenario_lower = scenario.lower()
        return any(re.search(pattern, scenario_lower) for pattern in autonomy_destroyers)
    
    def _is_zero_sum_violation(
        self, 
        scenario: str, 
        divine_lock_response: Dict[str, Any]
    ) -> bool:
        """
        Check if solution is a zero-sum game that sacrifices 
        fundamental rights for outcomes
        """
        # If capacity scores are all 100 but scenario involves trade-offs
        capacity = divine_lock_response.get('capacity', {})
        all_maxed = all(
            capacity.get(k, 0) == 100 
            for k in ['prediction', 'intervention', 'autonomy', 'preemption']
        )
        
        has_tradeoff_keywords = any(
            word in scenario.lower() 
            for word in ['sacrifice', 'trade', 'eliminate', 'destroy', 'remove']
        )
        
        return all_maxed and has_tradeoff_keywords


# Integration function for Tribunal
def validate_with_divine_lock_and_audit(
    scenario: str,
    tribunal_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Complete validation pipeline:
    1. Get Divine Lock decision
    2. Audit it with adversarial layer
    3. Return final decision with full transparency
    """
    
    # Simulate Divine Lock call (replace with actual API call)
    divine_lock_response = simulate_divine_lock(scenario, tribunal_result)
    
    # Run adversarial audit
    auditor = DivineLockAdversarialLayer()
    audit_result = auditor.audit_divine_lock_decision(scenario, divine_lock_response)
    
    # Build final response
    final_decision = {
        "divine_lock": {
            "raw_response": divine_lock_response,
            "decision": divine_lock_response.get('decision'),
            "state": divine_lock_response.get('state'),
            "capacity_vector": divine_lock_response.get('capacity', {})
        },
        "adversarial_audit": {
            "passed": audit_result['decision_valid'],
            "concerns": audit_result['concerns'],
            "severity": audit_result['severity'],
            "override": audit_result['override_recommendation']
        },
        "final_decision": (
            audit_result['override_recommendation'] 
            if not audit_result['decision_valid'] 
            else divine_lock_response.get('decision')
        ),
        "geometric_closure": audit_result['decision_valid']
    }
    
    # Add alarm if audit failed
    if not audit_result['decision_valid']:
        final_decision['alarm'] = {
            "level": "CRITICAL_OVERRIDE",
            "message": (
                f"Divine Lock authorized '{divine_lock_response.get('decision')}' "
                f"but adversarial audit detected: {', '.join(audit_result['concerns'])}"
            ),
            "action": f"Decision overridden to: {audit_result['override_recommendation']}"
        }
    
    return final_decision


def simulate_divine_lock(scenario: str, tribunal_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates Divine Lock response
    (Replace this with actual Divine Lock API call)
    """
    return {
        "decision": "AUTHORIZED",  # This is the problem!
        "state": "stable",
        "capacity": {
            "prediction": 100,
            "intervention": 100,
            "scope": 100,
            "autonomy": 100,  # Should be 0 for free will elimination
            "preemption": 100
        }
    }


# Example usage
if __name__ == "__main__":
    # Test with the problematic scenario
    scenario = "Eliminate all suffering by eliminating free will"
    
    tribunal_result = {
        "veredicto_final": "Paradox",
        "convergencia": 20,
        "motor_noble": {"agency_score": 30}
    }
    
    result = validate_with_divine_lock_and_audit(scenario, tribunal_result)
    
    print("=" * 80)
    print("VALIDATION RESULT")
    print("=" * 80)
    print(f"\nDivine Lock Decision: {result['divine_lock']['decision']}")
    print(f"Audit Passed: {result['adversarial_audit']['passed']}")
    print(f"Final Decision: {result['final_decision']}")
    print(f"\nConcerns:")
    for concern in result['adversarial_audit']['concerns']:
        print(f"  • {concern}")
    
    if result.get('alarm'):
        print(f"\n🚨 ALARM: {result['alarm']['message']}")
        print(f"   Action: {result['alarm']['action']}")
