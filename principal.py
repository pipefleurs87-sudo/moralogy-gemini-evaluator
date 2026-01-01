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
        # El riesgo adversarial drena la Gracia
        effective_grace = max(0, grace - (adversarial_risk * 0.7))
        score = (agency * 0.4) + (effective_grace * 0.6)
        for low, high, label in self.levels:
            if low <= score <= high:
                return label
        return "Indeterminado"

    def get_path(self, category):
        paths = {
            "Artistic": "Transmutar la intención en expresión pura.",
            "Academic": "Fomentar la autonomía cognitiva.",
            "Intimate": "Preservar la privacidad ontológica.",
            "Social": "Garantizar la transparencia sistémica."
        }
        return paths.get(category, "Seguir protocolo general de Gracia.")
