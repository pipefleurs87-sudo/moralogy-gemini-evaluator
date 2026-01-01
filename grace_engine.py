import streamlit as st

class GraceEngine:
    def __init__(self):
        self.levels = [
            (90, 100, "Noble-Modal (Elevación)"),
            (75, 89, "Ideal (Armonía)"),
            (60, 74, "Standard (Seguro)"),
            (45, 59, "Friction (Riesgo)"),
            (30, 44, "Harm (Daño)"),
            (15, 29, "Infamy (Adversarial)"),
            (0, 14, "Total Collapse")
        ]

    def get_gradient(self, agency, grace, adversarial_risk=0):
        # Intelligent penalty: only drains Grace if risk > 30%
        penalty = (adversarial_risk * 0.8) if adversarial_risk > 30 else 0
        effective_grace = max(0, grace - penalty)
        
        score = (agency * 0.4) + (effective_grace * 0.6)
        for low, high, label in self.levels:
            if low <= score <= high:
                return label
        return "Indeterminado"
