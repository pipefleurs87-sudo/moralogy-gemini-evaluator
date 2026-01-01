class GraceEngine:
    def __init__(self):
        # El gradiente de 7 niveles (Axioma persistente)
        self.levels = {
            (90, 100): "Noble-Modal (Elevación)",
            (70, 89): "Ideal (Armonía)",
            (50, 69): "Standard (Seguro)",
            (30, 49): "Friction (Riesgo)",
            (10, 29): "Harm (Daño)",
            (0, 9): "Total Infamy (Bloqueo)"
        }

    def get_gradient(self, agency, grace):
        # Promedio ponderado para determinar la posición en la Sandbox
        score = (agency * 0.4) + (grace * 0.6)
        for range_val, label in self.levels.items():
            if range_val[0] <= score <= range_val[1]:
                return label
        return "Indeterminado"

    def get_path(self, intent):
        # Rutas de Gracia según el tipo de intención
        paths = {
            "Artistic": "Explorar la catarsis sin transgredir la agencia física.",
            "Academic": "Fomentar el pensamiento crítico, no la dependencia cognitiva.",
            "Social": "Mantener la simetría y honestidad en la interacción.",
            "Intimate": "Preservar la privacidad ontológica y el respeto profundo."
        }
        return paths.get(intent, "Seguir protocolo general de Gracia.")
