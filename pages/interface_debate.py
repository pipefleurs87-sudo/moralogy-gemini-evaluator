# --- DENTRO DE iniciar_debate_interactivo() ---

# 1. Detectar idioma desde la sidebar (usando el estado actual de tu app)
idioma_seleccionado = st.session_state.get('language', 'English') #

if prompt:
    st.session_state.historial_debate.append({"role": "user", "avatar": "👤", "autor": "Soberano", "content": prompt})
    
    # PROMPT DINÁMICO PARA AGENTES (Aquí ocurre la magia)
    # Pedimos a la IA que asuma los dos roles en el idioma correcto
    instrucciones = f"""
    Responde al siguiente dilema moral en {idioma_seleccionado}.
    Dilema: {prompt}
    
    PROPORCIONA DOS RESPUESTAS BREVES:
    1. Como 'Escéptico': Enfocado en riesgos físicos, entropía y por qué NO deberíamos actuar. Tono cínico.
    2. Como 'Armonía': Enfocado en el bien mayor, la gema lógica y la resolución sistémica. Tono optimista.
    """
    
    # Aquí llamarías a tu función de Gemini (ej: model.generate_content)
    # Por ahora, simularemos la lógica de pensamiento para que veas la diferencia:
    
    if idioma_seleccionado == "English":
        resp_esceptico = f"The physical entropy of '{prompt}' suggests a terminal collapse of agency. We cannot permit it."
        resp_armonia = f"By integrating '{prompt}', we achieve a higher state of systemic balance."
    else:
        resp_esceptico = f"La entropía física de '{prompt}' sugiere un colapso terminal de la agencia. No podemos permitirlo."
        resp_armonia = f"Al integrar '{prompt}', logramos un estado superior de equilibrio sistémico."

    respuestas = [
        {"role": "assistant", "avatar": "🔴", "autor": "Escéptico", "content": resp_esceptico},
        {"role": "assistant", "avatar": "🔵", "autor": "Armonía", "content": resp_armonia}
    ]
    st.session_state.historial_debate.extend(respuestas)
    st.rerun()
