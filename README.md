# 🧭 Moralogy Gemini Evaluator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gemini API](https://img.shields.io/badge/Powered%20by-Google%20Gemini-blue)](https://ai.google.dev/)
[![Framework DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.18091340-blue)](https://doi.org/10.5281/zenodo.18091340)

> Objective moral evaluation of AI decisions using peer-reviewed philosophy + cutting-edge AI.

Built for [Google Gemini API Developer Competition 2024](https://gemini3.devpost.com/)

---

## 🎯 What It Does

Combines **Google Gemini's** natural language understanding with the **Moralogy Framework** (peer-reviewed moral philosophy) to provide objective, measurable ethical analysis of AI decisions.

**Input:** Any moral dilemma in plain English  
**Output:** Rigorous moral analysis with justification

---

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator.git
cd moralogy-gemini-evaluator

# Install dependencies
pip install -r requirements.txt

# Set up Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Run application
streamlit run src/app.py
```

### Usage

1. Enter an ethical dilemma
2. Click "Analyze"
3. Get objective moral evaluation

---

## 🏗️ Architecture
```
User Input (natural language)
    ↓
Gemini API (parse scenario)
    ↓
Moralogy Framework (calculate harm)
    ↓
Gemini API (generate explanation)
    ↓
Formatted Output + Visualization
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

---

## 📊 Demo Cases

See [examples/demo_cases.md](examples/demo_cases.md) for:
- Trolley Problem
- Autonomous Vehicle Dilemmas
- Medical Resource Allocation
- Content Moderation
- Climate Policy

---

## 🔬 The Moralogy Framework

This project implements the **Moralogy Framework**, a peer-reviewed approach to objective ethics:

**Paper:** [DOI: 10.5281/zenodo.18091340](https://doi.org/10.5281/zenodo.18091340)

**Core Principles:**
1. **Negative Constraint:** Do not cause unnecessary harm
2. **Positive Duty:** Prevent avoidable harm within capacity

**Why It's Objective:**
- Grounded in universal vulnerability
- Logically derived from conditions of rational agency
- Measurable using existing disciplines (medicine, law, economics)

---

## 🛠️ Built With

- **Google Gemini API** - Natural language processing
- **Python 3.10+** - Core logic
- **Streamlit** - User interface
- **Moralogy Framework** - Moral evaluation engine

---

## 📝 Development Status

**Current Phase:** MVP Development (DevPost Competition)

**Completed:**
- ✅ Repository structure
- ✅ Architecture documentation
- ✅ Demo cases defined
- ⏳ Core implementation (in progress)
- ⏳ UI development (in progress)
- ⏳ Video demo (pending)

**Deadline:** January 5, 2025

---

## 🤝 Contributing

This is a competition submission but feedback welcome:
1. Open an issue with suggestions
2. Star the repo if you find it interesting
3. Share with AI ethics researchers

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file

---

## 🔗 Links

- **Competition:** [Google Gemini API DevPost](https://gemini3.devpost.com/)
- **Framework Paper:** [Zenodo](https://doi.org/10.5281/zenodo.18091340)
- **Author Substack:** [ergoprotego.substack.com](https://ergoprotego.substack.com)
- **GitHub Profile:** [@pipefleurs87-sudo](https://github.com/pipefleurs87-sudo)

---

## ⚠️ Note

This project is part of the Google Gemini API Developer Competition.  
Submission deadline: January 5, 2025.

**Status:** 🚧 Active Development
```

**Commit:**
- Scroll abajo
- Click **"Commit changes..."**
- Click **"Commit changes"**

---

## PASO 4: VERIFICAR QUE TODO ESTÁ BIEN

Tu repo ahora debería verse así:
```
moralogy-gemini-evaluator/
├─ docs/
│  └─ ARCHITECTURE.md
├─ examples/
│  └─ demo_cases.md
├─ src/
│  └─ README.md
├─ .gitignore
├─ LICENSE
├─ README.md
└─ requirements.txt
```

**Para verificar:**
- Ve a la página principal de tu repo
- Deberías ver todas las carpetas listadas
- El README.md debería mostrarse bonito abajo

---

## PASO 5: OBTENER LA URL DEL REPO

**Tu URL es:**
```
https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator
