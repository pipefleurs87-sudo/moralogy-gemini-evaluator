# entropia_engine.py
import json

class EntropiaCausal:
    """
    Calculador de Irreversibilidad y Colapso de Estados.
    Módulo invariable que mide el costo físico de una decisión moral.
    """
    def __init__(self):
        # Factores constantes de 'gravedad' por módulo
        self.coeficientes_irreversibilidad = {
            "Biological": 0.95,  # Casi nada biológico es reversible
            "Legal": 0.70,       # Las leyes cambian, pero los precedentes quedan
            "Financial": 0.40,   # El dinero es fungible, pero el costo de oportunidad no
            "Systemic": 0.60,    # Los sistemas tienden al caos (segunda ley)
            "Informational": 0.85, # La información filtrada no vuelve a ser privada
            "Autonomy": 0.90     # La pérdida de agencia es difícil de recuperar
        }

    def calcular_indice(self, modulos_afectados, nivel_impacto):
        """
        Calcula el CR (Costo de Reconstrucción) y la DI (Disipación de Información).
        """
        score_base = 0
        for mod in modulos_afectados:
            peso = self.coeficientes_irreversibilidad.get(mod, 0.5)
            score_base += peso * nivel_impacto
            
        # Normalización del índice (0 a 1)
        indice = min(1.0, score_base / (len(modulos_afectados) if modulos_afectados else 1))
        return round(indice, 4)

    def evaluar_colapso_futuros(self, indice_entropia):
        """
        Determina cuántas ramas de posibilidad se cierran.
        """
        if indice_entropia > 0.8:
            return "ALTA: Colapso Crítico de Futuros. La acción es prácticamente irreversible."
        elif indice_entropia > 0.5:
            return "MEDIA: Fricción Entrópica. Requiere alto consumo de Gracia para revertir."
        return "BAJA: Fluidez Causal. El sistema mantiene múltiples trayectorias abiertas."

# Instancia única para el sistema
entropia_monitor = EntropiaCausal()
