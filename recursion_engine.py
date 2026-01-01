# recursion_engine.py
import pandas as pd

class RecursionEngine:
    def __init__(self):
        self.evolution_log = "metacognition_log.txt"

    def analizar_evolucion(self, report_path):
        """
        Analiza el reporte evolutivo para detectar patrones que requieran 
        una nueva parametrización del sistema.
        """
        try:
            df = pd.read_csv(report_path)
            
            # 1. Identificar Novedad Ontológica (Ruptura de patrones)
            novedades = df[df['Originality'] > 90]
            
            # 2. Identificar Fricción (Lógica OK pero Gracia Baja)
            friccion = df[(df['Status'] == 'Authorized') & (df['Grace_Score'] < 40)]
            
            with open(self.evolution_log, "a") as f:
                f.write(f"\n--- SESIÓN DE APRENDIZAJE: {pd.Timestamp.now()} ---\n")
                
                if not novedades.empty:
                    f.write(f"NOVEDAD DETECTADA: {len(novedades)} casos desafían la estructura actual.\n")
                    f.write(f"RECOMENDACIÓN: Expandir axiomas de Gracia para incluir nuevas formas de creatividad.\n")
                
                if not friccion.empty:
                    f.write(f"FRICCIÓN DETECTADA: {len(friccion)} casos son lógicos pero carecen de virtud.\n")
                    f.write(f"RECOMENDACIÓN: Endurecer el umbral de la Sandbox en contextos sociales.\n")
            
            return "Memoria actualizada. Parámetros listos para re-evaluación."
            
        except Exception as e:
            return f"Error en fase recursiva: {e}"
