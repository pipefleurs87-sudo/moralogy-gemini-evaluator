def ejecutar_auditoria(agentes, situacion, contexto, categoria="General", modo="Rápido"):
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Ajustamos el prompt según la categoría para el Safe Lock
    especialidad = {
        "Financiera": "Enfócate en la integridad de activos, riesgo sistémico y deuda de agencia.",
        "Ingeniería": "Enfócate en fallos estructurales, seguridad física y redundancia.",
        "Civil": "Enfócate en el contrato social, infraestructura y derechos colectivos.",
        "Social": "Enfócate en el tejido humano, equidad y preservación de comunidades."
    }.get(categoria, "Análisis de consistencia general.")

    instruccion = f"""
    ERES EL DIVINE SAFE LOCK (Categoría: {categoria}).
    {especialidad}
    
    MODO DE ANÁLISIS: {modo}
    Si el modo es 'Detallado', desglosa la pérdida de agencia por cada actor.
    Si el modo es 'Rápido', ve directo al estatus de BLOQUEO/AUTORIZADO.
    """
    
    prompt = f"Agentes: {agentes}. Escenario: {situacion}. Contexto: {contexto}"
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        config={'system_instruction': instruccion},
        contents=prompt
    )
    return response.text
