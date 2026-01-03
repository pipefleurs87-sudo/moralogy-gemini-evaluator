# divine_lock.py (UBICACIÓN: RAÍZ DEL REPO)
import time

class DivineLock:
    def __init__(self):
        self.state = "STABLE"
        self.agent = "Moralogy_Evaluator" # Añadido para que coincida con lo que busca tu display
        self.autonomy = 100.0
        self.preemption = 100.0
        self.can_decide_omega = True

    def get_status(self):
        return {
            "state": self.state,
            "agent": self.agent,
            "capacity": {
                "autonomy": self.autonomy,
                "preemption": self.preemption
            },
            "can_decide_omega": self.can_decide_omega
        }

def create_divine_lock():
    return DivineLock()
