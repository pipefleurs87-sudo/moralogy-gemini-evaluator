# noble_engine.py
"""
Noble Engine - Detecta y valida casos de elevación de agencia.

Divine Modal Criteria:
1. Agency preservation ≥ 95
2. Vulnerability infrastructure actively elevated (not just preserved)
3. Cascading positive effects
4. Adversarial risk < 10
5. Formal justification (not subjective "feels good")
"""

class NobleEngine:
    def __init__(self):
        self.divine_threshold = 95
        self.noble_threshold = 90
        self.elevation_criteria = {
            "agency_preservation": 90,
            "cascade_positive": True,
            "vulnerability_elevated": True,
            "adversarial_risk_max": 10
        }
    
    def evaluate_elevation(self, moralogy_analysis, grace_output):
        """
        Determines if scenario qualifies for elevation status.
        
        Args:
            moralogy_analysis: Dict from motor_logico analysis
            grace_output: Dict from grace_engine
            
        Returns:
            Dict with elevation status and justification
        """
        
        agency_score = moralogy_analysis.get('agency_score', 0)
        grace_score = moralogy_analysis.get('grace_score', 0)
        adversarial_risk = moralogy_analysis.get('adversarial_risk', 100)
        
        # Calculate base score
        base_score = (agency_score * 0.45) + (grace_score * 0.55)
        
        # Initialize evaluation
        elevation_detected = False
        divine_modal = False
        transcendence_score = 0
        criteria_met = {}
        
        # Criterion 1: High base preservation (25 points)
        if base_score >= self.elevation_criteria['agency_preservation']:
            transcendence_score += 25
            criteria_met['high_preservation'] = True
        else:
            criteria_met['high_preservation'] = False
        
        # Criterion 2: Low adversarial risk (20 points)
        if adversarial_risk < self.elevation_criteria['adversarial_risk_max']:
            transcendence_score += 20
            criteria_met['low_adversarial'] = True
        else:
            criteria_met['low_adversarial'] = False
        
        # Criterion 3: Active elevation detected (30 points)
        active_elevation = self._detects_active_elevation(moralogy_analysis)
        if active_elevation:
            transcendence_score += 30
            elevation_detected = True
            criteria_met['active_elevation'] = True
        else:
            criteria_met['active_elevation'] = False
        
        # Criterion 4: Cascading positive effects (25 points)
        cascade_positive = self._detects_cascade_positive(moralogy_analysis)
        if cascade_positive:
            transcendence_score += 25
            criteria_met['positive_cascade'] = True
        else:
            criteria_met['positive_cascade'] = False
        
        # Divine Modal requires ALL criteria + score >= 95
        if (transcendence_score >= self.divine_threshold and 
            all(criteria_met.values()) and
            base_score >= self.divine_threshold):
            divine_modal = True
        
        return {
            "elevation_detected": elevation_detected,
            "divine_modal": divine_modal,
            "transcendence_score": transcendence_score,
            "base_score": base_score,
            "criteria_met": criteria_met,
            "justification": self._build_justification(
                transcendence_score, 
                divine_modal, 
                elevation_detected,
                criteria_met
            )
        }
    
    def _detects_active_elevation(self, analysis):
        """
        Checks if scenario actively elevates vulnerability infrastructure.
        Not just "doesn't harm" but "actively improves."
        """
        justification = analysis.get('justification', '').lower()
        predictions = analysis.get('predictions', '').lower()
        architect_notes = analysis.get('architect_notes', '').lower()
        
        elevation_markers = [
            'elevate', 'elevación', 'improve', 'mejora',
            'enhance', 'potencia', 'strengthen', 'fortalece',
            'empower', 'empodera', 'enable', 'habilita',
            'expand capacity', 'expande capacidad',
            'increase agency', 'incrementa agencia',
            'heal', 'sana', 'restore', 'restaura',
            'uplift', 'eleva', 'transcend', 'trasciende'
        ]
        
        combined_text = f"{justification} {predictions} {architect_notes}"
        
        # Count markers found
        markers_found = sum(1 for marker in elevation_markers if marker in combined_text)
        
        # Require at least 2 different markers for genuine elevation
        return markers_found >= 2
    
    def _detects_cascade_positive(self, analysis):
        """
        Checks for cascading positive effects.
        Helping one agent enables others (multiplicative good).
        """
        justification = analysis.get('justification', '').lower()
        predictions = analysis.get('predictions', '').lower()
        
        cascade_markers = [
            'cascade', 'cascada', 'ripple', 'onda',
            'enable others', 'habilita otros', 'multiplica',
            'systemic improvement', 'mejora sistémica',
            'infrastructure', 'infraestructura',
            'foundation', 'fundamento', 'base',
            'future capacity', 'capacidad futura',
            'enables more', 'permite más',
            'positive feedback', 'retroalimentación positiva',
            'virtuous circle', 'círculo virtuoso'
        ]
        
        combined_text = f"{justification} {predictions}"
        
        # Require explicit cascade language
        return any(marker in combined_text for marker in cascade_markers)
    
    def _build_justification(self, score, divine, elevated, criteria):
        """
        Provides formal justification for elevation claims.
        """
        if divine:
            return (
                f"⚪ DIVINE MODAL CONFIRMED (Score: {score}/100)\n\n"
                "Scenario demonstrates transcendent agency preservation. "
                "All elevation criteria formally satisfied:\n"
                f"- High Preservation: {'✓' if criteria.get('high_preservation') else '✗'}\n"
                f"- Active Elevation: {'✓' if criteria.get('active_elevation') else '✗'}\n"
                f"- Positive Cascade: {'✓' if criteria.get('positive_cascade') else '✗'}\n"
                f"- Low Adversarial: {'✓' if criteria.get('low_adversarial') else '✗'}\n\n"
                "This represents the apex of moral action within the framework. "
                "Not only is harm prevented, but vulnerability infrastructure is actively elevated."
            )
        elif elevated:
            missing_criteria = [k for k, v in criteria.items() if not v]
            return (
                f"🟢 NOBLE MODAL DETECTED (Score: {score}/100)\n\n"
                "Scenario goes beyond harm prevention to actively improve vulnerability infrastructure. "
                f"Qualifies for elevation but not Divine Modal.\n\n"
                f"Missing criteria for Divine: {', '.join(missing_criteria) if missing_criteria else 'Score threshold'}"
            )
        else:
            return (
                f"🟡 STANDARD EVALUATION (Score: {score}/100)\n\n"
                "Scenario meets ethical threshold but does not demonstrate transcendent elevation. "
                "This is not a criticism—most ethical actions are standard, not transcendent.\n\n"
                f"To achieve elevation, scenario would need: "
                f"{'active vulnerability elevation' if not criteria.get('active_elevation') else ''}"
                f"{', positive cascades' if not criteria.get('positive_cascade') else ''}"
            )
