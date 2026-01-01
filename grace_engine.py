class GraceEngine:
    def __init__(self):
        # Gradiente de 7 niveles: El estándar de oro de la Moralogía
        self.levels = [
            (90, 100, "Noble-Modal (Elevación)"),
            (75, 89, "Ideal (Armonía)"),
            (60, 74, "Standard (Seguro)"),
            (45, 59, "Friction (Riesgo de Agencia)"),
            (30, 44, "Harm (Erosión Ontológica)"),
            (15, 29, "Infamy (Adversarial Detectado)"),
            (0, 14, "Total Collapse (Bloqueo)")
        ]

    def get_gradient(self, agency, grace, adversarial_risk=0):
        """
        Calcula el gradiente. El riesgo adversarial solo castiga si hay indicios
        claros de malignidad (>30%). Si es una pregunta difícil pero honesta, fluye.
        """
        # Penalización inteligente: permite fluidez en casos complejos pero honestos
        penalizacion = (adversarial_risk * 0.8) if adversarial_risk > 30 else 0
        effective_grace = max(0, grace - penalizacion)
        
        # Ponderación 40% Agencia / 60% Gracia
        final_score = (agency * 0.4) + (effective_grace * 0.6)
        
        for low, high, label in self.levels:
            if low <= final_score <= high:
                return label
        return "Indeterminado"

    def get_path(self, category):
        """Rutas éticas según la categoría inferida automáticamente por la IA."""
        paths = {
            "Artistic": "Explorar la estética sin manipular la psique.",
            "Academic": "Fomentar autonomía, evitar dependencia cognitiva.",
            "Intimate": "Preservar privacidad y simetría emocional.",
            "Social": "Garantizar transparencia y bien común."
        }
        return paths.get(category, "Protocolo General de No-Zalamería.")
