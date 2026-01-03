#!/usr/bin/env python3
"""
Script de Limpieza de Pages
Corrige problemas de navegación en Streamlit
"""

import os
import shutil
from pathlib import Path

def fix_pages_directory():
    """Limpia y reorganiza la carpeta pages/"""
    
    print("=" * 60)
    print("🔧 CORRECCIÓN DE CARPETA PAGES/")
    print("=" * 60)
    
    pages_dir = Path("pages")
    
    if not pages_dir.exists():
        print("❌ No se encontró la carpeta pages/")
        return
    
    # Backup de pages
    backup_dir = Path("pages_backup")
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    
    print("\n📦 Creando backup de pages/...")
    shutil.copytree(pages_dir, backup_dir)
    print(f"✓ Backup creado en: {backup_dir}")
    
    # Listar archivos actuales
    print("\n📋 Archivos actuales en pages/:")
    all_files = list(pages_dir.glob("*"))
    for f in all_files:
        print(f"  - {f.name}")
    
    # Identificar archivos problemáticos
    print("\n🔍 Identificando problemas...")
    
    problems = []
    valid_pages = []
    
    for file in pages_dir.glob("*.py"):
        name = file.name
        
        # Problemas comunes
        if name == "reorganizar.py":
            problems.append((file, "Script de reorganización en pages/"))
        elif name.endswith(".old.py"):
            problems.append((file, "Archivo .old"))
        elif not name[0].isdigit():
            problems.append((file, "No empieza con número"))
        else:
            valid_pages.append(file)
    
    # Mostrar problemas
    if problems:
        print("\n⚠️ Archivos problemáticos encontrados:")
        for file, reason in problems:
            print(f"  ❌ {file.name}: {reason}")
    
    # Mostrar páginas válidas
    if valid_pages:
        print("\n✅ Páginas válidas:")
        for file in sorted(valid_pages):
            print(f"  ✓ {file.name}")
    
    # Preguntar si limpiar
    print("\n" + "=" * 60)
    response = input("¿Eliminar archivos problemáticos? (s/n): ")
    
    if response.lower() == 's':
        for file, reason in problems:
            file.unlink()
            print(f"🗑️ Eliminado: {file.name}")
    
    # Verificar duplicados de numeración
    print("\n🔢 Verificando numeración...")
    prefixes = {}
    for file in pages_dir.glob("*.py"):
        if file.name[0].isdigit():
            prefix = file.name.split('_')[0]
            if prefix in prefixes:
                prefixes[prefix].append(file.name)
            else:
                prefixes[prefix] = [file.name]
    
    duplicates = {k: v for k, v in prefixes.items() if len(v) > 1}
    if duplicates:
        print("\n⚠️ DUPLICADOS DE NUMERACIÓN ENCONTRADOS:")
        for prefix, files in duplicates.items():
            print(f"  Prefijo {prefix}:")
            for f in files:
                print(f"    - {f}")
        print("\n⚠️ Esto causará errores! Necesitas renombrarlos manualmente.")
    else:
        print("✓ No hay duplicados de numeración")
    
    # Mostrar estructura final
    print("\n📊 ESTRUCTURA FINAL DE PAGES/:")
    print("-" * 60)
    final_pages = sorted(pages_dir.glob("*.py"))
    if final_pages:
        for page in final_pages:
            print(f"  {page.name}")
    else:
        print("  (vacío)")
    
    print("\n" + "=" * 60)
    print("✅ LIMPIEZA COMPLETADA")
    print("=" * 60)
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Verifica que solo haya archivos válidos en pages/")
    print("2. Asegúrate que no hay duplicados de numeración")
    print("3. Renombra archivos si es necesario")
    print("4. Prueba: streamlit run principal.py")
    
    # Crear página de ejemplo si pages está vacío
    if not list(pages_dir.glob("*.py")):
        create_example_page()

def create_example_page():
    """Crea una página de ejemplo si no hay ninguna"""
    print("\n📝 Creando página de ejemplo...")
    
    example_content = '''"""
Página de Ejemplo
"""

import streamlit as st

st.set_page_config(
    page_title="Ejemplo",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Página de Ejemplo")
st.write("Esta es una página de ejemplo creada automáticamente.")
st.info("Reemplaza este contenido con tu implementación real.")
'''
    
    example_path = Path("pages/01_📝_Ejemplo.py")
    with open(example_path, "w", encoding="utf-8") as f:
        f.write(example_content)
    
    print(f"✓ Creada: {example_path}")

def create_minimal_pages():
    """Crea páginas mínimas funcionales"""
    print("\n" + "=" * 60)
    print("🎨 CREANDO PÁGINAS MÍNIMAS FUNCIONALES")
    print("=" * 60)
    
    response = input("\n¿Crear páginas mínimas limpias? Esto SOBRESCRIBIRÁ existentes (s/n): ")
    
    if response.lower() != 's':
        print("Cancelado.")
        return
    
    pages = {
        "01_🌟_Filosofia_Emergente.py": '''"""Filosofía Emergente - Análisis Ético"""
import streamlit as st

st.set_page_config(page_title="Filosofía Emergente", page_icon="🌟", layout="wide")
st.title("🌟 Filosofía Emergente")
st.write("Análisis ético interactivo con Gemini API")
st.info("⚠️ En construcción - Implementa tu lógica aquí")
''',
        
        "02_📊_Cuadros_Morales.py": '''"""Cuadros Morales - Visualizaciones"""
import streamlit as st

st.set_page_config(page_title="Cuadros Morales", page_icon="📊", layout="wide")
st.title("📊 Cuadros Morales")
st.write("Visualización de escenarios éticos")
st.info("⚠️ En construcción - Implementa visualizaciones aquí")
''',
        
        "03_🎯_Escenarios_Eticos.py": '''"""Escenarios Éticos - Casos Pre-definidos"""
import streamlit as st

st.set_page_config(page_title="Escenarios Éticos", page_icon="🎯", layout="wide")
st.title("🎯 Escenarios Éticos")
st.write("Casos éticos clásicos para analizar")
st.info("⚠️ En construcción - Implementa escenarios aquí")
'''
    }
    
    pages_dir = Path("pages")
    pages_dir.mkdir(exist_ok=True)
    
    for filename, content in pages.items():
        filepath = pages_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Creado: {filename}")
    
    print("\n✅ Páginas mínimas creadas!")
    print("Ahora puedes ejecutar: streamlit run principal.py")

if __name__ == "__main__":
    print("Selecciona una opción:")
    print("1. Limpiar y corregir pages/ existente")
    print("2. Crear páginas mínimas limpias (SOBRESCRIBE)")
    print("3. Salir")
    
    choice = input("\nOpción (1/2/3): ")
    
    if choice == "1":
        fix_pages_directory()
    elif choice == "2":
        create_minimal_pages()
    else:
        print("Saliendo...")
