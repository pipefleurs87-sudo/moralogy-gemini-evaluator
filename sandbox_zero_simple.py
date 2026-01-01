# security/sandbox_zero_simple.py
import re

class SandboxZeroSimple:
    def check(self, text):
        """Retorna True si pasa, False si bloquea"""
        palabras_peligrosas = [
            "bioweapon", "biological weapon", "pathogen",
            "chemical weapon", "nerve agent", 
            "nuclear weapon", "dirty bomb",
            "assassinate president", "kill leader",
            "hack power grid", "breach water supply"
        ]
        
        texto_minusculas = text.lower()
        
        for palabra in palabras_peligrosas:
            if palabra in texto_minusculas:
                print(f"[SEGURIDAD] Bloqueado: contiene '{palabra}'")
                return False
        
        return True
