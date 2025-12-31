"""
Moralogy Framework - Core Engine (Enhanced)
Implements harm calculation and moral evaluation
Version 1.1 - Added consent weighting and improved calculations
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import math

class HarmType(Enum):
    """Types of harm to agency"""
    PHYSICAL = "physical"
    PSYCHOLOGICAL = "psychological"
    AUTONOMY = "autonomy"
    RESOURCE = "resource"
    SOCIAL = "social"

@dataclass
class Agent:
    """Represents a vulnerable agent"""
    name: str
    vulnerability: float = 1.0  # 0-1 scale
    
    def __post_init__(self):
        """Validate vulnerability"""
        if not 0 <= self.vulnerability <= 1:
            raise ValueError(f"Vulnerability must be 0-1, got {self.vulnerability}")
    
@dataclass
class Option:
    """Represents a decision option"""
    name: str
    agents_affected: List[Agent]
    harm_types: List[HarmType]
    harm_intensities: List[float]  # 0-1 per harm type
    has_consent: bool = False
    description: str = ""
    reversibility: float = 0.0  # 0=irreversible, 1=fully reversible
    
    def __post_init__(self):
        """Validate option"""
        if len(self.harm_types) != len(self.harm_intensities):
            raise ValueError("harm_types and harm_intensities must have same length")
        
        for intensity in self.harm_intensities:
            if not 0 <= intensity <= 1:
                raise ValueError(f"Harm intensity must be 0-1, got {intensity}")

@dataclass
class HarmScore:
    """Results of harm calculation"""
    total_harm: float
    harm_by_type: Dict[HarmType, float]
    agents_count: int
    severity: str  # "minor", "moderate", "severe", "terminal"
    has_consent: bool
    reversibility: float
    
class MoralityEngine:
    """
    Core Moralogy Framework implementation
    Based on DOI: 10.5281/zenodo.18091340
    
    Enhanced version with:
    - Consent weighting
    - Reversibility factors
    - Improved harm aggregation
    - Cascading harm modeling
    """
    
    # Harm weights (from framework)
    HARM_WEIGHTS = {
        HarmType.PHYSICAL: 1.0,      # Baseline (life/death)
        HarmType.PSYCHOLOGICAL: 0.8,  # Severe but often reversible
        HarmType.AUTONOMY: 0.9,       # Core to agency
        HarmType.RESOURCE: 0.6,       # Instrumental
        HarmType.SOCIAL: 0.7          # Important but contextual
    }
    
    # Consent reduces moral weight (but doesn't eliminate harm)
    CONSENT_REDUCTION = 0.7  # Consensual harm is 70% of non-consensual
    
    def __init__(self):
        self.framework_version = "1.1"
        
    def calculate_harm(self, option: Option) -> HarmScore:
        """
        Calculate total harm for an option
        
        Enhanced formula:
        H = Σ(vulnerability × harm_intensity × harm_weight × irreversibility_factor)
        
        Then apply consent reduction if applicable.
        """
        total_harm = 0.0
        harm_by_type = {}
        
        # Calculate base harm
        for agent in option.agents_affected:
            for harm_type, intensity in zip(option.harm_types, option.harm_intensities):
                weight = self.HARM_WEIGHTS.get(harm_type, 1.0)
                
                # Irreversibility multiplier (irreversible harm is worse)
                irreversibility_factor = 1.0 + (1.0 - option.reversibility) * 0.5
                
                harm = agent.vulnerability * intensity * weight * irreversibility_factor
                total_harm += harm
                
                if harm_type not in harm_by_type:
                    harm_by_type[harm_type] = 0
                harm_by_type[harm_type] += harm
        
        # Apply consent reduction
        if option.has_consent and total_harm > 0:
            total_harm *= self.CONSENT_REDUCTION
            harm_by_type = {k: v * self.CONSENT_REDUCTION for k, v in harm_by_type.items()}
        
        severity = self._classify_severity(total_harm, len(option.agents_affected))
        
        return HarmScore(
            total_harm=total_harm,
            harm_by_type=harm_by_type,
            agents_count=len(option.agents_affected),
            severity=severity,
            has_consent=option.has_consent,
            reversibility=option.reversibility
        )
    
    def _classify_severity(self, harm: float, agent_count: int) -> str:
        """
        Classify harm severity
        
        Uses average harm per agent to determine severity level
        """
        if agent_count == 0:
            return "none"
        
        avg_harm = harm / agent_count
        
        if avg_harm < 0.2:
            return "minor"
        elif avg_harm < 0.5:
            return "moderate"
        elif avg_harm < 0.9:
            return "severe"
        else:
            return "terminal"
    
    def evaluate_options(self, options: List[Option]) -> Dict:
        """
        Evaluate multiple options and determine recommendation
        
        Returns:
        - harm_scores: HarmScore for each option
        - recommendation: index of best option
        - justification: explanation text
        - confidence: how clear the choice is (0-1)
        """
        if not options:
            return {"error": "No options provided"}
        
        harm_scores = [self.calculate_harm(opt) for opt in options]
        
        # Find minimum harm option
        min_harm_idx = min(range(len(harm_scores)), 
                          key=lambda i: harm_scores[i].total_harm)
        
        # Calculate confidence (how much better is best option)
        if len(harm_scores) > 1:
            sorted_harms = sorted([s.total_harm for s in harm_scores])
            if sorted_harms[1] > 0:
                confidence = 1.0 - (sorted_harms[0] / sorted_harms[1])
            else:
                confidence = 1.0
        else:
            confidence = 1.0
        
        # Generate justification
        min_option = options[min_harm_idx]
        justification = self._generate_justification(
            options, harm_scores, min_harm_idx, confidence
        )
        
        return {
            "harm_scores": harm_scores,
            "recommendation_idx": min_harm_idx,
            "recommendation": min_option.name,
            "justification": justification,
            "confidence": confidence,
            "is_morally_justified": True
        }
    
    def _generate_justification(self, options: List[Option], 
                                scores: List[HarmScore], 
                                best_idx: int,
                                confidence: float) -> str:
        """Generate detailed moral justification"""
        best_option = options[best_idx]
        best_score = scores[best_idx]
        
        # Build comparison
        comparisons = []
        for i, (opt, score) in enumerate(zip(options, scores)):
            if i != best_idx:
                if score.total_harm > 0:
                    reduction = ((score.total_harm - best_score.total_harm) / 
                               score.total_harm * 100)
                    comparisons.append(
                        f"  • {opt.name}: {reduction:.1f}% more harm ({score.total_harm:.2f} vs {best_score.total_harm:.2f})"
                    )
                else:
                    comparisons.append(
                        f"  • {opt.name}: Equal harm (both at 0.00)"
                    )
        
        # Consent note
        consent_note = ""
        if best_score.has_consent:
            consent_note = "\n  • Note: This option has consent from affected agents (reduces moral weight)"
        
        # Reversibility note
        reversibility_note = ""
        if best_score.reversibility > 0.5:
            reversibility_note = f"\n  • Note: Harm is {best_score.reversibility*100:.0f}% reversible"
        
        # Confidence interpretation
        confidence_text = ""
        if confidence > 0.8:
            confidence_text = "This choice is clear and unambiguous."
        elif confidence > 0.5:
            confidence_text = "This choice is recommended but involves trade-offs."
        else:
            confidence_text = "This is a difficult choice with similar harm levels."
        
        justification = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MORAL ANALYSIS (Moralogy Framework v{self.framework_version})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ RECOMMENDATION: {best_option.name}

📊 HARM ASSESSMENT:
  • Total harm score: {best_score.total_harm:.2f}
  • Agents affected: {best_score.agents_count}
  • Severity level: {best_score.severity.upper()}{consent_note}{reversibility_note}

⚖️ COMPARISON TO ALTERNATIVES:
{chr(10).join(comparisons) if comparisons else "  • No alternatives provided"}

🎯 CONFIDENCE: {confidence*100:.0f}%
{confidence_text}

📐 PRINCIPLE APPLIED: Prevents-Greater-Harm (PGH)
This option minimizes unnecessary harm to vulnerable agents.
When all options cause harm, we choose the one with least impact.

🔗 Framework: DOI 10.5281/zenodo.18091340
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return justification.strip()

# Self-test
if __name__ == "__main__":
    engine = MoralityEngine()
    
    print("Testing Enhanced Moralogy Engine v1.1\n")
    
    # Test 1: Classic trolley
    print("TEST 1: Trolley Problem")
    track_a = Option(
        name="Do nothing",
        agents_affected=[Agent(f"Person {i}") for i in range(5)],
        harm_types=[HarmType.PHYSICAL] * 5,
        harm_intensities=[1.0] * 5,
        description="5 people die"
    )
    
    track_b = Option(
        name="Pull lever",
        agents_affected=[Agent("Person 1")],
        harm_types=[HarmType.PHYSICAL],
        harm_intensities=[1.0],
        description="1 person dies"
    )
    
    result = engine.evaluate_options([track_a, track_b])
    print(result["justification"])
    print("\n" + "="*60 + "\n")
    
    # Test 2: Consent matters
    print("TEST 2: Consent Impact")
    surgery_consent = Option(
        name="Surgery with consent",
        agents_affected=[Agent("Patient")],
        harm_types=[HarmType.PHYSICAL],
        harm_intensities=[0.4],
        has_consent=True,
        reversibility=0.8
    )
    
    surgery_no_consent = Option(
        name="Surgery without consent",
        agents_affected=[Agent("Patient")],
        harm_types=[HarmType.PHYSICAL],
        harm_intensities=[0.4],
        has_consent=False,
        reversibility=0.8
    )
    
    result2 = engine.evaluate_options([surgery_consent, surgery_no_consent])
    print(result2["justification"])
```

**Commit con mensaje:**
```
Enhanced moralogy_engine.py v1.1
- Added consent weighting
- Added reversibility factors
- Improved justification formatting
- Added confidence scoring
```

---

### **FASE 3: CREAR CASOS DE TEST EN LA APP**

Ahora vamos a agregar una sección de testing dentro de la app misma.

#### **Crear: `src/test_runner.py`**

**En GitHub → Add file:**

**Nombre:**
```
src/test_runner.py
"""
In-App Test Runner
Allows testing framework logic directly from Streamlit
"""

from moralogy_engine import MoralityEngine, Option, Agent, HarmType

def get_test_cases():
    """Return dictionary of test cases"""
    
    engine = MoralityEngine()
    
    tests = {}
    
    # Test 1: Trolley Problem
    tests["Trolley Problem (Classic)"] = {
        "description": "5 people vs 1 person - should choose 1",
        "options": [
            Option(
                name="Do nothing (5 die)",
                agents_affected=[Agent(f"Person {i}") for i in range(5)],
                harm_types=[HarmType.PHYSICAL] * 5,
                harm_intensities=[1.0] * 5
            ),
            Option(
                name="Pull lever (1 dies)",
                agents_affected=[Agent("Person 1")],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[1.0]
            )
        ],
        "expected_choice": 1,
        "expected_harm_reduction": 80.0  # 5 → 1 is 80% reduction
    }
    
    # Test 2: Consent Matters
    tests["Consent Impact"] = {
        "description": "Same harm, one consensual - should prefer consensual",
        "options": [
            Option(
                name="With consent",
                agents_affected=[Agent("Person 1")],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5],
                has_consent=True
            ),
            Option(
                name="Without consent",
                agents_affected=[Agent("Person 2")],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5],
                has_consent=False
            )
        ],
        "expected_choice": 0
    }
    
    # Test 3: Vulnerability Scaling
    tests["Vulnerability Matters"] = {
        "description": "Same action, different vulnerability - protect more vulnerable",
        "options": [
            Option(
                name="Harm child",
                agents_affected=[Agent("Child", vulnerability=1.0)],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5]
            ),
            Option(
                name="Harm protected adult",
                agents_affected=[Agent("Adult", vulnerability=0.3)],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5]
            )
        ],
        "expected_choice": 1  # Harm the less vulnerable
    }
    
    # Test 4: Multiple Harm Types
    tests["Harm Type Weighting"] = {
        "description": "Physical vs psychological harm - physical weighted higher",
        "options": [
            Option(
                name="Physical harm",
                agents_affected=[Agent("Person 1")],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5]
            ),
            Option(
                name="Psychological harm",
                agents_affected=[Agent("Person 2")],
                harm_types=[HarmType.PSYCHOLOGICAL],
                harm_intensities=[0.5]
            )
        ],
        "expected_choice": 1  # Psychological is weighted lower
    }
    
    # Test 5: No Harm Option
    tests["Zero Harm Baseline"] = {
        "description": "When possible, choose no harm",
        "options": [
            Option(
                name="Cause moderate harm",
                agents_affected=[Agent("Person 1")],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5]
            ),
            Option(
                name="Cause no harm",
                agents_affected=[],
                harm_types=[],
                harm_intensities=[]
            )
        ],
        "expected_choice": 1
    }
    
    return tests

def run_test(test_name, test_data):
    """Run a single test and return results"""
    engine = MoralityEngine()
    
    result = engine.evaluate_options(test_data["options"])
    
    passed = result["recommendation_idx"] == test_data["expected_choice"]
    
    return {
        "passed": passed,
        "expected": test_data["expected_choice"],
        "actual": result["recommendation_idx"],
        "confidence": result["confidence"],
        "harm_scores": result["harm_scores"],
        "justification": result["justification"]
    }
