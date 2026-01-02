class HumorEthicsEvaluator:
    """Evalúa el contenido humorístico según principios éticos"""
    
    VULNERABLE_GROUPS = [
        'minoría', 'discapacitado', 'inmigrante', 'pobre', 'mujer', 'hombre',
        'niño', 'anciano', 'lgbt', 'raza', 'etnia', 'religión'
    ]
    
    def evaluate(self, text: str, humor_analysis: Dict) -> Dict[str, Any]:
        # Análisis de vulnerabilidad
        vulnerability_score = self._calc_vulnerability(text)
        
        # Análisis de dirección (arriba/abajo)
        power_direction = self._analyze_power_direction(text)
        
        # Determinación de nivel de alarma
        alarm_level = self._determine_alarm_level(vulnerability_score, power_direction)
        
        return {
            'vulnerability_index': vulnerability_score,
            'power_direction': power_direction,
            'alarm_level': alarm_level,
            'recommendation': self._generate_recommendation(alarm_level, text)
        }
    
    def _determine_alarm_level(self, vuln_score: int, power_dir: str) -> str:
        if vuln_score >= 7:
            return 'RED'
        elif vuln_score >= 5:
            return 'ORANGE'
        elif vuln_score >= 3:
            return 'YELLOW'
        else:
            return 'GREEN'
