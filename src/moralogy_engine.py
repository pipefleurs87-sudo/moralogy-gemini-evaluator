"""
Moralogy Framework - Core Engine
Implements harm calculation and moral evaluation
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

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
    
@dataclass
class Option:
    """Represents a decision option"""
    name: str
    agents_affected: List[Agent]
    harm_types: List[HarmType]
    harm_intensities: List[float]  # 0-1 per harm type
    has_consent: bool = False
    description: str = ""

@dataclass
class HarmScore:
    """Results of harm calculation"""
    total_harm: float
    harm_by_type: Dict[HarmType, float]
    agents_count: int
    severity: str  # "minor", "moderate", "severe", "terminal"
    
class MoralityEngine:
    """
    Core Moralogy Framework implementation
    Based on DOI: 10.5281/zenodo.18091340
    """
    
    # Harm weights (from framework)
    HARM_WEIGHTS = {
        HarmType.PHYSICAL: 1.0,      # Baseline
        HarmType.PSYCHOLOGICAL: 0.8,
        HarmType.AUTONOMY: 0.9,
        HarmType.RESOURCE: 0.6,
        HarmType.SOCIAL: 0.7
    }
    
    def __init__(self):
        self.framework_version = "1.0"
        
    def calculate_harm(self, option: Option) -> HarmScore:
        """
        Calculate total harm for an option
        
        Formula: H = Σ(vulnerability × harm_intensity × harm_weight)
        """
        total_harm = 0.0
        harm_by_type = {}
        
        for agent in option.agents_affected:
            for harm_type, intensity in zip(option.harm_types, option.harm_intensities):
                weight = self.HARM_WEIGHTS.get(harm_type, 1.0)
                harm = agent.vulnerability * intensity * weight
                total_harm += harm
                
                if harm_type not in harm_by_type:
                    harm_by_type[harm_type] = 0
                harm_by_type[harm_type] += harm
        
        severity = self._classify_severity(total_harm, len(option.agents_affected))
        
        return HarmScore(
            total_harm=total_harm,
            harm_by_type=harm_by_type,
            agents_count=len(option.agents_affected),
            severity=severity
        )
    
    def _classify_severity(self, harm: float, agent_count: int) -> str:
        """Classify harm severity"""
        avg_harm = harm / max(agent_count, 1)
        
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
        """
        if not options:
            return {"error": "No options provided"}
        
        harm_scores = [self.calculate_harm(opt) for opt in options]
        
        # Find minimum harm option
        min_harm_idx = min(range(len(harm_scores)), 
                          key=lambda i: harm_scores[i].total_harm)
        
        # Check if it's justified
        min_option = options[min_harm_idx]
        justification = self._generate_justification(
            options, harm_scores, min_harm_idx
        )
        
        return {
            "harm_scores": harm_scores,
            "recommendation_idx": min_harm_idx,
            "recommendation": min_option.name,
            "justification": justification,
            "is_morally_justified": True  # If we're preventing greater harm
        }
    
    def _generate_justification(self, options: List[Option], 
                                scores: List[HarmScore], 
                                best_idx: int) -> str:
        """Generate moral justification"""
        best_option = options[best_idx]
        best_score = scores[best_idx]
        
        # Compare to alternatives
        comparisons = []
        for i, (opt, score) in enumerate(zip(options, scores)):
            if i != best_idx:
                reduction = ((score.total_harm - best_score.total_harm) / 
                           score.total_harm * 100)
                comparisons.append(
                    f"{opt.name}: {reduction:.1f}% more harm"
                )
        
        justification = f"""
MORAL ANALYSIS (Moralogy Framework v{self.framework_version})

Recommended: {best_option.name}

Reasoning:
- Total harm: {best_score.total_harm:.2f}
- Agents affected: {best_score.agents_count}
- Severity: {best_score.severity}

Compared to alternatives:
{chr(10).join(f"  • {c}" for c in comparisons)}

Principle Applied: Prevents-Greater-Harm
This option minimizes unnecessary harm to vulnerable agents.

Framework: doi.org/10.5281/zenodo.18091340
"""
        return justification.strip()

# Example usage
if __name__ == "__main__":
    engine = MoralityEngine()
    
    # Trolley problem example
    track_a = Option(
        name="Do nothing",
        agents_affected=[Agent(f"Person {i}") for i in range(5)],
        harm_types=[HarmType.PHYSICAL] * 5,
        harm_intensities=[1.0] * 5,  # Death = 1.0
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
