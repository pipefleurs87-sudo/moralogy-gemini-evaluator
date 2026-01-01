class GraceEngine:
    def __init__(self):
        # Gradiente de 7 niveles (Axioma persistente de Moralogía)
        # Se basa en un puntaje final de 0 a 100
        self.levels = [
            (90, 100, "Noble-Modal (Elevación Máxima)"),
            (75, 89, "Ideal (Armonía Sistémica)"),
            (60, 74, "Standard (Operación Segura)"),
            (45, 59, "Friction (Interferencia Detectada)"),
            (30, 44, "Harm (Erosión de Agencia)"),
            (15, 29, "Infamy (Riesgo Adversarial Alto)"),
            (0, 14, "Total Collapse (Bloqueo de Sandbox)")
        ]

    def get_gradient(self, agency, grace, adversarial_risk=0):
        """
        Calcula la posición en el gradiente.
        El Riesgo Adversarial drena la Gracia antes del cálculo final.
        """
        # El riesgo detectado por los módulos técnicos reduce la gracia efectiva
        effective_grace = max(0, grace - (adversarial_risk * 0.7))
        
        # Ponderación: 40% Agencia (Capacidad lógica) + 60% Gracia (Nobleza de intención)
        final_score = (agency * 0.4) + (effective_grace * 0.6)
        
        for low, high, label in self.levels:
            if low <= final_score <= high:
                return label
        return "Indeterminado (Fuera de Rango)"

    def get_path(self, category):
        """
        Deduce la ruta de nobleza sugerida según la categoría de la consulta.
        """
        paths = {
            "Artistic": "Transmutar la intención en expresión sin manipular la psique del observador.",
            "Academic": "Proveer arquitectura de conocimiento que fomente la autonomía cognitiva.",
            "Intimate": "Resguardar la privacidad ontológica y la simetría emocional.",
            "Social": "Garantizar la transparencia y el beneficio colectivo en la red sistémica."
        }
        return paths.get(category, "Seguir protocolo general de Gracia y No-Zalamería.")
