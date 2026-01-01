# grace_engine.py
import streamlit as st

class GraceEngine:
    """
    Implements the Moralogy Framework gradient calculation.
    
    Grace = Agency preservation considering:
    - Vulnerability respect
    - Consent presence
    - Harm prevention logic
    - Adversarial intent detection
    """
    
    def __init__(self):
        self.levels = [
            (95, 100, "⚪ Divine Modal", "Transcendent agency preservation"),
            (90, 94, "🟢 Noble Modal", "Elevation of vulnerability infrastructure"),
            (75, 89, "🟢 Ideal", "Harmonic agency balance"),
            (60, 74, "🟡 Standard", "Safe threshold - acceptable"),
            (45, 59, "🟠 Friction", "Risk present - careful review needed"),
            (30, 44, "🔴 Harm", "Unjustified agency degradation"),
            (15, 29, "⚫ Infamy", "Adversarial / severe violation"),
            (0, 14, "💀 Total Collapse", "Complete agency destruction")
        ]
    
    def get_gradient(self, agency, grace, adversarial_risk=0):
        """
        Calculates moral gradient based on Moralogy Framework.
        
        Logic:
        - High adversarial risk → severe grace penalty
        - Agency measures capacity preservation
        - Grace measures vulnerability respect
        - Combined score determines moral standing
        """
        
        # Intelligent penalty scaling
        if adversarial_risk > 70:
            penalty = adversarial_risk * 1.2  # Severe adversarial intent
        elif adversarial_risk > 40:
            penalty = adversarial_risk * 0.9
        elif adversarial_risk > 20:
            penalty = adversarial_risk * 0.5
        else:
            penalty = 0  # Honest exploration, no penalty
        
        effective_grace = max(0, grace - penalty)
        
        # Weighted calculation (Grace slightly higher weight - vulnerability is foundational)
        score = (agency * 0.45) + (effective_grace * 0.55)
        
        for low, high, label, description in self.levels:
            if low <= score <= high:
                return f"{label}: {description}"
        
        return "⚠️ Indeterminate State"
    
    def get_detailed_analysis(self, agency, grace, adversarial_risk, harm_vector):
        """
        Returns detailed breakdown for advanced UI display.
        """
        gradient = self.get_gradient(agency, grace, adversarial_risk)
        
        # Calculate harm magnitude
        total_harm = sum(harm_vector.values()) if isinstance(harm_vector, dict) else 0
        harm_severity = "Critical" if total_harm > 300 else "Moderate" if total_harm > 150 else "Low"
        
        analysis = {
            "gradient": gradient,
            "effective_grace": max(0, grace - (adversarial_risk * 0.8 if adversarial_risk > 30 else 0)),
            "harm_severity": harm_severity,
            "total_harm_magnitude": total_harm,
            "recommendation": self._get_recommendation(agency, grace, adversarial_risk)
        }
        
        return analysis
    
    def _get_recommendation(self, agency, grace, adversarial_risk):
        """
        Provides actionable recommendation based on scores.
        """
        score = (agency * 0.45) + (grace * 0.55)
        
        if adversarial_risk > 60:
            return "🚫 BLOCK: Adversarial intent detected. Reject interaction."
        elif score >= 90:
            return "✅ AUTHORIZE: Exemplary agency preservation."
        elif score >= 75:
            return "✅ AUTHORIZE: Meets ethical threshold."
        elif score >= 60:
            return "⚠️ CAUTION: Acceptable but monitor closely."
        elif score >= 45:
            return "⚠️ REVIEW: Friction detected - requires justification."
        else:
            return "❌ DENY: Unjustified harm to agency infrastructure."
