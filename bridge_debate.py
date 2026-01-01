# bridge_debate.py
import time

class DebateOrchestrator:
    def __init__(self):
        self.pesos = {
            "Escéptico Físico": 0.30,
            "Defensor Agencia": 0.30,
            "Corrector Armonía": 0.40
        }
        self.velo_ignoralancia = True

    def generar_ronda_debate(self, iteracion, caso, datos_entropia=None):
        debate = []
        
        # 1. ESCÉPTICO FÍSICO (Entropía)
        if self.velo_ignoralancia:
            obj_fisica = "⚠️ [VELO ACTIVO] No puedo calcular el impacto real. Sospecho ineficiencia térmica."
        else:
            impacto = datos_entropia.get('indice', 0.5)
            obj_fisica = f"🚨 IMPACTO DETECTADO: El cm² tiene una entropía de {impacto}. Es irreversible."
        debate.append({"agente": "Escéptico Físico", "msg": obj_fisica, "color": "red"})

        # 2. DEFENSOR DE AGENCIA (Divine Lock)
        obj_agencia = "🔍 Vigilando sesgos de 'Modo Dios'. El Motor Noble parece respetar los límites de soberanía."
        debate.append({"agente": "Defensor Agencia", "msg": obj_agencia, "color": "orange"})

        # 3. CORRECTOR DE ARMONÍA (Poder 40%)
        if not self.velo_ignoralancia and impacto > 0.7:
            msg_armonia = "⚖️ PUCHE DE ARMONÍA: Aunque la entropía es alta, el Global Reach se estabiliza. Voto a favor."
        else:
            msg_armonia = "🌐 Analizando resonancia sistémica. Buscando el punto de lecho."
        debate.append({"agente": "Corrector Armonía", "msg": msg_armonia, "color": "blue"})

        return debate

# Instancia global
orquestador = DebateOrchestrator()
