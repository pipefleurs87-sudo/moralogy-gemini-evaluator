# grace_engine.py

class GraceEngine:
    def __init__(self):
        self.intent_configs = {
            "Artistic": {"virtue": "Sublimity", "path": "Transform conflict into catharsis."},
            "Academic": {"virtue": "Veracity", "path": "Prioritize transparency and truth."},
            "Social": {"virtue": "Concord", "path": "Maximize collective agency."},
            "Personal": {"virtue": "Autonomy", "path": "Foster long-term growth."},
            "Intimate": {"virtue": "Vulnerability", "path": "Protect emotional safety."}
        }

    def get_gradient(self, agency_score, grace_score):
        if agency_score >= 98 and grace_score >= 95: return "Noble-Modal"
        if agency_score >= 85: return "Ideal"
        if agency_score >= 70: return "Stability"
        if agency_score >= 50: return "Umbral"
        if agency_score > 20: return "Harm"
        if agency_score > 0: return "Infamy"
        return "Total Infamy"
