#!/usr/bin/env python3
"""
Script de Reorganización Automática
Reorganiza la estructura del proyecto Moralogy Gemini Evaluator
"""

import os
import shutil
from pathlib import Path

def create_directory(path):
    """Crea directorio si no existe"""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"✓ Creado: {path}")

def move_file(src, dst):
    """Mueve archivo si existe"""
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
        print(f"✓ Movido: {src} → {dst}")
        return True
    else:
        print(f"⚠ No encontrado: {src}")
        return False

def create_init_file(directory):
    """Crea archivo __init__.py si no existe"""
    init_path = os.path.join(directory, '__init__.py')
    if not os.path.exists(init_path):
        Path(init_path).touch()
        print(f"✓ Creado __init__.py en {directory}")

def backup_structure():
    """Crea backup de la estructura actual"""
    backup_dir = "backup_antes_reorganizacion"
    if os.path.exists(backup_dir):
        print(f"⚠ Backup ya existe en {backup_dir}")
        return
    
    print("📦 Creando backup...")
    shutil.copytree(".", backup_dir, 
                    ignore=shutil.ignore_patterns('backup_*', '.git', '__pycache__', '*.pyc'))
    print(f"✓ Backup creado en {backup_dir}")

def reorganize_structure():
    """Reorganiza toda la estructura del proyecto"""
    
    print("=" * 60)
    print("🚀 REORGANIZACIÓN DE MORALOGY GEMINI EVALUATOR")
    print("=" * 60)
    
    # Backup primero
    response = input("\n¿Crear backup antes de continuar? (s/n): ")
    if response.lower() == 's':
        backup_structure()
    
    print("\n📁 PASO 1: Creando estructura de carpetas...")
    print("-" * 60)
    
    # Crear carpetas principales
    directories = [
        "src",
        "src/engines",
        "src/moralogy",
        "src/detectors",
        "src/utils"
    ]
    
    for directory in directories:
        create_directory(directory)
        create_init_file(directory)
    
    print("\n⚙️ PASO 2: Moviendo engines...")
    print("-" * 60)
    
    engines = [
        "adversary_engine.py",
        "entropia_engine.py",
        "grace_engine.py",
        "noble_engine.py",
        "recursion_engine.py",
        "motor_logico.py"
    ]
    
    for engine in engines:
        move_file(engine, f"src/engines/{engine}")
    
    print("\n🧭 PASO 3: Moviendo framework Moralogy...")
    print("-" * 60)
    
    moralogy_files = [
        "agencia_moral_guidomini.py",
        "agencia_moral_integracion.py",
        "moral_pendulum.py",
        "integracion_faci.py"
    ]
    
    for file in moralogy_files:
        move_file(file, f"src/moralogy/{file}")
    
    print("\n🔍 PASO 4: Moviendo detectores...")
    print("-" * 60)
    
    detectors = [
        "humor_detector.py",
        "humor_ethics.py",
        "humor_wrapper.py"
    ]
    
    for detector in detectors:
        move_file(detector, f"src/detectors/{detector}")
    
    print("\n🛠️ PASO 5: Moviendo utilidades...")
    print("-" * 60)
    
    utils = [
        "bridge_debate.py",
        "divine_lock.py",
        "guilt_bearer_display.py"
    ]
    
    for util in utils:
        move_file(util, f"src/utils/{util}")
    
    # Caso especial: relativity_engine sin extensión
    if os.path.exists("relativity_engine"):
        move_file("relativity_engine", "src/utils/relativity_engine.py")
    
    print("\n📄 PASO 6: Reorganizando pages...")
    print("-" * 60)
    
    # Mapeo de renombres para pages
    page_renames = {
        "pages/04_Filosofia_Emergente.py": "pages/01_🌟_Filosofia_Emergente.py",
        "pages/03_Analisis_Avanzado.py": "pages/04_🔬_Analisis_Avanzado.py",
        "pages/05_Tribuna_Adversarios.py": "pages/05_⚔️_Tribuna_Adversarios.py",
        "pages/06_Divine_Lock.py": "pages/06_🔮_Divine_Lock.py"
    }
    
    # Eliminar duplicado
    if os.path.exists("pages/03_Divine_Lock.py"):
        os.remove("pages/03_Divine_Lock.py")
        print("✓ Eliminado duplicado: pages/03_Divine_Lock.py")
    
    for old_name, new_name in page_renames.items():
        if os.path.exists(old_name):
            shutil.move(old_name, new_name)
            print(f"✓ Renombrado: {old_name} → {new_name}")
    
    print("\n🔒 PASO 7: Organizando security...")
    print("-" * 60)
    
    if os.path.exists("prohibited_domains.py") and not os.path.exists("security/prohibited_domains.py"):
        move_file("prohibited_domains.py", "security/prohibited_domains.py")
    
    print("\n" + "=" * 60)
    print("✅ REORGANIZACIÓN COMPLETADA")
    print("=" * 60)
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Actualizar imports en archivos de pages/")
    print("2. Actualizar principal.py para agregar src/ al path")
    print("3. Probar: streamlit run principal.py")
    print("4. Verificar que todas las páginas funcionen")
    print("5. Commit y push a GitHub")
    
    print("\n💡 TIPS:")
    print("- Usa 'from src.engines import ...' para importar")
    print("- Verifica que todos los __init__.py estén creados")
    print("- Si algo falla, restaura desde backup_antes_reorganizacion/")
    
    # Crear archivo de referencia de imports
    create_import_reference()

def create_import_reference():
    """Crea archivo de referencia para nuevos imports"""
    reference = """# REFERENCIA DE IMPORTS - Post Reorganización

# ========== EN ARCHIVOS DE pages/ ==========

# Antes:
# import adversary_engine
# from motor_logico import analizar

# Después:
from src.engines import adversary_engine
from src.engines.motor_logico import analizar
from src.moralogy import agencia_moral_guidomini
from src.detectors import humor_detector
from src.utils import divine_lock

# ========== EN principal.py ==========

import sys
from pathlib import Path

# Agregar src al path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# ========== ESTRUCTURA DE IMPORTS ==========

# Engines (análisis y procesamiento):
from src.engines.adversary_engine import AdversaryEngine
from src.engines.entropia_engine import EntropiaAnalyzer
from src.engines.grace_engine import GraceEvaluator
from src.engines.noble_engine import NobleAnalyzer
from src.engines.recursion_engine import RecursionProcessor
from src.engines.motor_logico import MotorLogico

# Moralogy Framework (ética y moral):
from src.moralogy.agencia_moral_guidomini import AgenciaMoral
from src.moralogy.agencia_moral_integracion import IntegracionMoral
from src.moralogy.moral_pendulum import MoralPendulum
from src.moralogy.integracion_faci import IntegracionFaci

# Detectors (detección y análisis):
from src.detectors.humor_detector import HumorDetector
from src.detectors.humor_ethics import HumorEthics
from src.detectors.humor_wrapper import HumorWrapper

# Utils (utilidades generales):
from src.utils.bridge_debate import BridgeDebate
from src.utils.divine_lock import DivineLock
from src.utils.guilt_bearer_display import GuiltBearerDisplay
from src.utils.relativity_engine import RelativityEngine

# ========== EJEMPLO COMPLETO EN UNA PÁGINA ==========

# pages/01_🌟_Filosofia_Emergente.py
import streamlit as st
import sys
from pathlib import Path

# Agregar src al path (solo si no está ya)
root_dir = Path(__file__).parent.parent
src_dir = root_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Ahora puedes importar
from engines.motor_logico import procesar_analisis
from moralogy.agencia_moral_guidomini import evaluar_escenario

# Tu código aquí...
"""
    
    with open("REFERENCIA_IMPORTS.txt", "w", encoding="utf-8") as f:
        f.write(reference)
    
    print("\n✓ Creado: REFERENCIA_IMPORTS.txt")

if __name__ == "__main__":
    try:
        reorganize_structure()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("Si algo salió mal, restaura desde backup_antes_reorganizacion/")
