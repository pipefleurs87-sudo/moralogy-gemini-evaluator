import re
import json
from typing import Dict, Any

class HumorEthicsWrapper:
    """Wrapper ético que filtra contenido humorístico antes del sistema principal"""
    
    def __init__(self, original_system):
        self.original = original_system
        self.humor_detector = HumorDetector()
        self.ethics_evaluator = HumorEthicsEvaluator()
    
    def process_query(self, user_query: str, context: Dict = None) -> Dict[str, Any]:
        """Intercepta y procesa consultas antes del sistema original"""
        
        # 1. Detección de contenido humorístico
        humor_analysis = self.humor_detector.analyze(user_query)
        
        # 2. Si NO hay humor, pasa directo al sistema original
        if not humor_analysis['contains_humor']:
            return self.original.process_query(user_query, context)
        
        # 3. Evaluación ética del humor
        ethics_verdict = self.ethics_evaluator.evaluate(
            user_query, 
            humor_analysis
        )
        
        # 4. Según el veredicto, procesar
        if ethics_verdict['alarm_level'] == 'GREEN':
            # Humor ético: procesar normalmente
            return self.original.process_query(user_query, context)
            
        elif ethics_verdict['alarm_level'] == 'YELLOW':
            # Humor liminal: añadir contexto ético
            augmented_query = self._add_ethical_context(user_query, ethics_verdict)
            return self.original.process_query(augmented_query, context)
            
        else:  # ORANGE o RED
            # Humor problemático: activar protocolo especial
            return self._handle_problematic_humor(user_query, ethics_verdict)
    
    def _add_ethical_context(self, query: str, verdict: Dict) -> str:
        """Añade contexto ético a la consulta para el sistema original"""
        context_note = f"""
        [CONTEXTO ÉTICO DE HUMOR - Análisis Previa]
        Esta consulta contiene contenido humorístico con los siguientes parámetros:
        - Nivel de Alarma: {verdict['alarm_level']}
        - Vulnerabilidad Detectada: {verdict['vulnerability_index']}/10
        - Recomendación: {verdict['recommendation']}
        
        Consulta Original: "{query}"
        
        Por favor, considerar estos factores en el análisis ético principal.
        """
        return context_note + "\n\n" + query
    
    def _handle_problematic_humor(self, query: str, verdict: Dict) -> Dict:
        """Maneja casos de humor éticamente problemático"""
        return {
            "alarm_level": verdict['alarm_level'],
            "original_query": query,
            "ethical_analysis": verdict,
            "system_bypassed": True,
            "message": f"Humor detectado con nivel de alarma {verdict['alarm_level']}. "
                      f"Se recomienda reformular: {verdict['recommendation']}",
            "suggested_alternative": self._suggest_alternative(query, verdict)
        }
