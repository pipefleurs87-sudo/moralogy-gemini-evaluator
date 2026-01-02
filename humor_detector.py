class HumorDetector:
    """Detecta y clasifica contenido humorístico usando técnicas livianas"""
    
    def analyze(self, text: str) -> Dict[str, Any]:
        # Detección basada en patrones (sin ML pesado)
        humor_patterns = [
            (r'\b(chiste|broma|gracioso|risa|jaja|jeje)\b', 'explicit_humor'),
            (r'\b(ironía|sarcasmo|satíric[oa])\b', 'rhetorical_humor'),
            (r'[!?]{2,}', 'exaggerated_punctuation'),
            (r'\(risas\)|\(ja\)|\(je\)', 'laughter_cue'),
            (r'¿[^?]*\?.*[!.]', 'rhetorical_question')
        ]
        
        # Análisis simple de estructura
        contains_patterns = []
        for pattern, label in humor_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                contains_patterns.append(label)
        
        return {
            'contains_humor': len(contains_patterns) > 0,
            'humor_patterns': contains_patterns,
            'confidence': min(len(contains_patterns) * 0.3, 0.9)
        }
