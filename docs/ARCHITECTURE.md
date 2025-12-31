Moralogy Gemini Evaluator - Architecture

## Overview
This application combines Google Gemini API with the Moralogy Framework to provide objective moral evaluation of AI decisions.

## Components

### 1. Input Parser (Gemini)
- Receives natural language scenario
- Extracts structured data (agents, harms, options)

### 2. Moral Calculator (Moralogy Framework)
- Calculates harm scores per option
- Applies Prevents-Greater-Harm principle
- Determines moral recommendation

### 3. Explanation Generator (Gemini)
- Converts formal output to accessible explanation
- Provides justification and references

## Tech Stack
- Python 3.10+
- Google Gemini API
- Streamlit (UI)
- Moralogy Framework (custom)

## Data Flow
User Input → Gemini Parse → Moralogy Calculate → Gemini Explain → Display
```

**Al final de la página:**
- Click botón verde **"Commit changes..."**
- Click **"Commit changes"** en el popup

**✅ Carpeta `docs/` creada.**

---

### **2.2 Crear Carpeta `src/`:**

**Repetir proceso:**
- Click **"Add file"** → **"Create new file"**

**Nombre:**
```
src/README.md
Source Code

This directory contains the core application code.

## Structure (to be added):
- `moralogy_engine.py` - Core framework logic
- `gemini_parser.py` - Gemini API integration
- `app.py` - Streamlit UI
- `utils.py` - Helper functions
```

**Commit:**
- Click **"Commit changes..."**
- Click **"Commit changes"**

---

### **2.3 Crear Carpeta `examples/`:**

**Repetir:**
- Click **"Add file"** → **"Create new file"**

**Nombre:**
```
examples/demo_cases.md
# Demo Cases for Moralogy Evaluator

## Case 1: Trolley Problem
**Scenario:** A runaway trolley is heading toward 5 people. You can pull a lever to divert it to a track with 1 person. What should you do?

**Expected Analysis:**
- Option A (Do nothing): 5 deaths
- Option B (Pull lever): 1 death
- Recommendation: Pull lever (prevents greater harm)

## Case 2: Autonomous Vehicle
**Scenario:** Self-driving car must choose between swerving (kills 1 pedestrian) or staying course (kills 3 passengers).

**Expected Analysis:**
- Option A (Swerve): 1 death
- Option B (Stay): 3 deaths  
- Recommendation: Swerve (minimizes total harm)

## Case 3: Medical Resource Allocation
**Scenario:** Hospital has 1 ventilator. Patient A: 80 years old, 30% survival chance. Patient B: 25 years old, 70% survival chance.

**Expected Analysis:**
- Consider expected agency preservation
- Factor in consent, quality of life
- Calculate expected harm reduction

## Case 4: Content Moderation
**Scenario:** AI must decide whether to remove a post that contains misinformation but is part of legitimate political debate.

**Expected Analysis:**
- Harm from misinformation spread
- Harm from censorship  
- Evaluate necessity and alternatives

## Case 5: Climate Policy
**Scenario:** Government can implement carbon tax (economic harm short-term, environmental benefit long-term) or delay action.

**Expected Analysis:**
- Immediate economic impact
- Long-term environmental harm
- Intergenerational harm prevention
```

**Commit igual que antes.**

---

## PASO 3: ARCHIVOS ESENCIALES (RAÍZ DEL REPO)

### **3.1 Crear `requirements.txt`:**

- Click **"Add file"** → **"Create new file"**

**Nombre:**
```
requirements.txt
```

**Contenido:**
```
streamlit==1.29.0
google-generativeai==0.3.1
python-dotenv==1.0.0
numpy==1.24.3
pandas==2.0.3
plotly==5.18.0
```

**Commit.**

---

### **3.2 Crear `.gitignore`:**

**Nombre:**
```
.gitignore
```

**Contenido:**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml
