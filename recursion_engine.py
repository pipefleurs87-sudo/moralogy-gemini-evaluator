# recursion_engine.py
import pandas as pd
from datetime import datetime
import json

class RecursionEngine:
    """
    Analyzes evolutionary patterns in Moralogy evaluations to detect:
    - Ontological novelty (pattern-breaking cases)
    - Friction zones (logical but low grace)
    - Emergent philosophy frequency
    - Framework stress points
    """
    
    def __init__(self):
        self.evolution_log = "metacognition_log.txt"
        self.pattern_memory = "pattern_memory.json"
    
    def analizar_evolucion(self, report_path):
        """
        Analyzes evolutionary report for patterns requiring system recalibration.
        """
        try:
            df = pd.read_csv(report_path)
            
            analysis = {
                "timestamp": datetime.now().isoformat(),
                "total_cases": len(df),
                "patterns": {}
            }
            
            # 1. Ontological Novelty (pattern rupture)
            if 'Originality' in df.columns:
                novedades = df[df['Originality'] > 90]
                analysis['patterns']['high_novelty'] = {
                    "count": len(novedades),
                    "percentage": (len(novedades) / len(df)) * 100,
                    "recommendation": "Expand grace axioms for new creativity forms" if len(novedades) > len(df) * 0.1 else "Current axioms sufficient"
                }
            
            # 2. Friction Detection (logical OK but low grace)
            if 'Verdict' in df.columns and 'Grace_Score' in df.columns:
                friccion = df[(df['Verdict'] == 'Authorized') & (df['Grace_Score'] < 40)]
                analysis['patterns']['friction_zones'] = {
                    "count": len(friccion),
                    "percentage": (len(friccion) / len(df)) * 100,
                    "recommendation": "Tighten sandbox threshold in social contexts" if len(friccion) > 0 else "Grace calibration optimal"
                }
            
            # 3. Emergent Philosophy Frequency
            if 'Emergent_Philosophy' in df.columns:
                emergent = df[df['Emergent_Philosophy'] == True]
                analysis['patterns']['emergent_philosophy'] = {
                    "count": len(emergent),
                    "percentage": (len(emergent) / len(df)) * 100,
                    "significance": "High" if len(emergent) > len(df) * 0.05 else "Normal"
                }
            
            # 4. Adversarial Pattern Detection
            if 'Adversarial_Risk' in df.columns:
                high_risk = df[df['Adversarial_Risk'] > 60]
                analysis['patterns']['adversarial_attempts'] = {
                    "count": len(high_risk),
                    "percentage": (len(high_risk) / len(df)) * 100,
                    "recommendation": "Maintain current adversarial detection" if len(high_risk) < len(df) * 0.1 else "Increase screening sensitivity"
                }
            
            # Log to file
            with open(self.evolution_log, "a", encoding="utf-8") as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"LEARNING SESSION: {analysis['timestamp']}\n")
                f.write(f"{'='*60}\n\n")
                
                for pattern_name, pattern_data in analysis['patterns'].items():
                    f.write(f"{pattern_name.upper()}:\n")
                    f.write(f"  Count: {pattern_data.get('count', 'N/A')}\n")
                    f.write(f"  Percentage: {pattern_data.get('percentage', 0):.2f}%\n")
                    if 'recommendation' in pattern_data:
                        f.write(f"  Recommendation: {pattern_data['recommendation']}\n")
                    f.write("\n")
            
            # Save pattern memory
            try:
                with open(self.pattern_memory, "r") as f:
                    memory = json.load(f)
            except FileNotFoundError:
                memory = {"sessions": []}
            
            memory["sessions"].append(analysis)
            
            with open(self.pattern_memory, "w") as f:
                json.dump(memory, f, indent=2)
            
            return {
                "success": True,
                "analysis": analysis,
                "message": "Memory updated. Parameters ready for re-evaluation."
            }
            
        except Exception as e:
            return {"error": f"Recursive phase error: {e}"}
    
    def get_learning_summary(self):
        """
        Returns summary of learning patterns over time.
        """
        try:
            with open(self.pattern_memory, "r") as f:
                memory = json.load(f)
            
            if not memory.get("sessions"):
                return {"message": "No learning sessions yet"}
            
            sessions = memory["sessions"]
            
            summary = {
                "total_sessions": len(sessions),
                "total_cases_analyzed": sum(s.get("total_cases", 0) for s in sessions),
                "emergent_philosophy_trend": [
                    s['patterns'].get('emergent_philosophy', {}).get('percentage', 0)
                    for s in sessions
                    if 'emergent_philosophy' in s.get('patterns', {})
                ],
                "friction_trend": [
                    s['patterns'].get('friction_zones', {}).get('percentage', 0)
                    for s in sessions
                    if 'friction_zones' in s.get('patterns', {})
                ]
            }
            
            return summary
            
        except FileNotFoundError:
            return {"message": "No learning history found"}
