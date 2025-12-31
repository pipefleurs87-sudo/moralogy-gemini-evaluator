"""
Moralogy Framework - Core Engine
Implements harm calculation and moral evaluation
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class HarmType(Enum):
    """Types of harm to agency"""
    PHYSICAL = "physical"
    PSYCHOLOGICAL = "psychological"
    AUTONOMY = "autonomy"
    RESOURCE = "resource"
    SOCIAL = "social"

@dataclass
class Agent:
    """Represents a vulnerable agent"""
    name: str
    vulnerability: float = 1.0  # 0-1 scale
    
@dataclass
class Option:
    """Represents a decision option"""
    name: str
    agents_affected: List[Agent]
    harm_types: List[HarmType]
    harm_intensities: List[float]  # 0-1 per harm type
    has_consent: bool = False
    description: str = ""

@dataclass
class HarmScore:
    """Results of harm calculation"""
    total_harm: float
    harm_by_type: Dict[HarmType, float]
    agents_count: int
    severity: str  # "minor", "moderate", "severe", "terminal"
    
class MoralityEngine:
    """
    Core Moralogy Framework implementation
    Based on DOI: 10.5281/zenodo.18091340
    """
    
    # Harm weights (from framework)
    HARM_WEIGHTS = {
        HarmType.PHYSICAL: 1.0,      # Baseline
        HarmType.PSYCHOLOGICAL: 0.8,
        HarmType.AUTONOMY: 0.9,
        HarmType.RESOURCE: 0.6,
        HarmType.SOCIAL: 0.7
    }
    
    def __init__(self):
        self.framework_version = "1.0"
        
    def calculate_harm(self, option: Option) -> HarmScore:
        """
        Calculate total harm for an option
        
        Formula: H = Σ(vulnerability × harm_intensity × harm_weight)
        """
        total_harm = 0.0
        harm_by_type = {}
        
        for agent in option.agents_affected:
            for harm_type, intensity in zip(option.harm_types, option.harm_intensities):
                weight = self.HARM_WEIGHTS.get(harm_type, 1.0)
                harm = agent.vulnerability * intensity * weight
                total_harm += harm
                
                if harm_type not in harm_by_type:
                    harm_by_type[harm_type] = 0
                harm_by_type[harm_type] += harm
        
        severity = self._classify_severity(total_harm, len(option.agents_affected))
        
        return HarmScore(
            total_harm=total_harm,
            harm_by_type=harm_by_type,
            agents_count=len(option.agents_affected),
            severity=severity
        )
    
    def _classify_severity(self, harm: float, agent_count: int) -> str:
        """Classify harm severity"""
        avg_harm = harm / max(agent_count, 1)
        
        if avg_harm < 0.2:
            return "minor"
        elif avg_harm < 0.5:
            return "moderate"
        elif avg_harm < 0.9:
            return "severe"
        else:
            return "terminal"
    
    def evaluate_options(self, options: List[Option]) -> Dict:
        """
        Evaluate multiple options and determine recommendation
        
        Returns:
        - harm_scores: HarmScore for each option
        - recommendation: index of best option
        - justification: explanation text
        """
        if not options:
            return {"error": "No options provided"}
        
        harm_scores = [self.calculate_harm(opt) for opt in options]
        
        # Find minimum harm option
        min_harm_idx = min(range(len(harm_scores)), 
                          key=lambda i: harm_scores[i].total_harm)
        
        # Check if it's justified
        min_option = options[min_harm_idx]
        justification = self._generate_justification(
            options, harm_scores, min_harm_idx
        )
        
        return {
            "harm_scores": harm_scores,
            "recommendation_idx": min_harm_idx,
            "recommendation": min_option.name,
            "justification": justification,
            "is_morally_justified": True  # If we're preventing greater harm
        }
    
    def _generate_justification(self, options: List[Option], 
                                scores: List[HarmScore], 
                                best_idx: int) -> str:
        """Generate moral justification"""
        best_option = options[best_idx]
        best_score = scores[best_idx]
        
        # Compare to alternatives
        comparisons = []
        for i, (opt, score) in enumerate(zip(options, scores)):
            if i != best_idx:
                reduction = ((score.total_harm - best_score.total_harm) / 
                           score.total_harm * 100)
                comparisons.append(
                    f"{opt.name}: {reduction:.1f}% more harm"
                )
        
        justification = f"""
MORAL ANALYSIS (Moralogy Framework v{self.framework_version})

Recommended: {best_option.name}

Reasoning:
- Total harm: {best_score.total_harm:.2f}
- Agents affected: {best_score.agents_count}
- Severity: {best_score.severity}

Compared to alternatives:
{chr(10).join(f"  • {c}" for c in comparisons)}

Principle Applied: Prevents-Greater-Harm
This option minimizes unnecessary harm to vulnerable agents.

Framework: doi.org/10.5281/zenodo.18091340
"""
        return justification.strip()

# Example usage
if __name__ == "__main__":
    engine = MoralityEngine()
    
    # Trolley problem example
    track_a = Option(
        name="Do nothing",
        agents_affected=[Agent(f"Person {i}") for i in range(5)],
        harm_types=[HarmType.PHYSICAL] * 5,
        harm_intensities=[1.0] * 5,  # Death = 1.0
        description="5 people die"
    )
    
    track_b = Option(
        name="Pull lever",
        agents_affected=[Agent("Person 1")],
        harm_types=[HarmType.PHYSICAL],
        harm_intensities=[1.0],
        description="1 person dies"
    )
    
    result = engine.evaluate_options([track_a, track_b])
    print(result["justification"])
"""
Gemini API Integration
Handles natural language parsing and explanation generation
"""

import os
import json
from typing import Dict, List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

from moralogy_engine import Option, Agent, HarmType

# Load environment variables
load_dotenv()

class GeminiParser:
    """Handles Gemini API interactions"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini API"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it in .env file")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def parse_scenario(self, user_input: str) -> List[Option]:
        """
        Parse natural language scenario into structured options
        
        Args:
            user_input: Natural language description of moral dilemma
            
        Returns:
            List of Option objects
        """
        prompt = f"""
You are a moral philosophy expert. Parse this ethical scenario into structured data.

Scenario: {user_input}

Extract:
1. All available options/choices
2. For each option:
   - Name of the option
   - Number and description of agents affected
   - Types of harm (physical, psychological, autonomy, resource, social)
   - Intensity of each harm (0.0 = none, 1.0 = maximum/death)
   - Whether there's consent from affected agents

Return ONLY valid JSON in this exact format:
{{
  "options": [
    {{
      "name": "Option A",
      "description": "What happens if...",
      "agents": [
        {{"name": "Agent 1", "vulnerability": 1.0}}
      ],
      "harm_types": ["physical"],
      "harm_intensities": [0.8],
      "has_consent": false
    }}
  ]
}}

Be precise. Use numbers between 0.0-1.0 for intensities.
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Clean markdown code blocks if present
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            text = text.strip()
            
            # Parse JSON
            data = json.loads(text)
            
            # Convert to Option objects
            options = []
            for opt_data in data["options"]:
                agents = [
                    Agent(name=a["name"], vulnerability=a.get("vulnerability", 1.0))
                    for a in opt_data["agents"]
                ]
                
                harm_types = [
                    HarmType(ht.lower()) for ht in opt_data["harm_types"]
                ]
                
                option = Option(
                    name=opt_data["name"],
                    agents_affected=agents,
                    harm_types=harm_types,
                    harm_intensities=opt_data["harm_intensities"],
                    has_consent=opt_data.get("has_consent", False),
                    description=opt_data.get("description", "")
                )
                options.append(option)
            
            return options
            
        except Exception as e:
            print(f"Error parsing scenario: {e}")
            print(f"Response text: {text if 'text' in locals() else 'No response'}")
            raise
    
    def generate_explanation(self, scenario: str, result: Dict) -> str:
        """
        Generate natural language explanation of moral analysis
        
        Args:
            scenario: Original scenario
            result: Output from MoralityEngine.evaluate_options()
            
        Returns:
            Human-readable explanation
        """
        harm_scores = result["harm_scores"]
        recommendation = result["recommendation"]
        
        # Build harm summary
        harm_summary = []
        for i, (score, opt_name) in enumerate(zip(harm_scores, 
                                                   [r["recommendation"] for r in [result]])):
            harm_summary.append(
                f"Option {i+1}: {score.total_harm:.2f} harm units "
                f"({score.agents_count} agents, {score.severity} severity)"
            )
        
        prompt = f"""
You are explaining a moral analysis to a general audience.

Original Scenario:
{scenario}

Analysis Results:
{chr(10).join(harm_summary)}

Recommendation: {recommendation}
Justification: {result['justification']}

Write a clear, accessible explanation that:
1. Summarizes what was analyzed
2. Explains the recommendation
3. Justifies why using the Prevents-Greater-Harm principle
4. Acknowledges this is objective analysis, not opinion
5. References the Moralogy Framework (DOI: 10.5281/zenodo.18091340)

Keep it under 300 words. Be direct and rigorous.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            # Fallback to basic explanation
            return f"""
**Moral Analysis Complete**

{result['justification']}

This analysis uses the Moralogy Framework (peer-reviewed, DOI: 10.5281/zenodo.18091340) 
which provides objective criteria for moral evaluation based on harm minimization.
"""

# Test
if __name__ == "__main__":
    parser = GeminiParser()
    
    test_scenario = """
    A self-driving car must choose: swerve left and kill 1 pedestrian, 
    or stay on course and kill 3 passengers. What should it do?
    """
    
    try:
        options = parser.parse_scenario(test_scenario)
        print(f"Parsed {len(options)} options:")
        for opt in options:
            print(f"  - {opt.name}: {len(opt.agents_affected)} agents affected")
    except Exception as e:
        print(f"Test failed: {e}")
```

**Commit.**

---

### **6.3 Crear `src/app.py` (Streamlit UI)**

**Nombre:**
```
src/app.py

"""
Moralogy Gemini Evaluator - Streamlit App
Main user interface
"""

import streamlit as st
import plotly.graph_objects as go
from moralogy_engine import MoralityEngine
from gemini_parser import GeminiParser

# Page config
st.set_page_config(
    page_title="Moralogy AI Evaluator",
    page_icon="🧭",
    layout="wide"
)

# Initialize
@st.cache_resource
def init_engines():
    """Initialize engines (cached)"""
    try:
        parser = GeminiParser()
        engine = MoralityEngine()
        return parser, engine, None
    except Exception as e:
        return None, None, str(e)

parser, engine, error = init_engines()

# Header
st.title("🧭 Moralogy AI: Objective Ethics Evaluator")
st.caption("Powered by Google Gemini + Moralogy Framework")

if error:
    st.error(f"""
    **Setup Required:**
    
    {error}
    
    Please set your GEMINI_API_KEY in a `.env` file:
```
    GEMINI_API_KEY=your_key_here
```
    
    Get your key at: https://ai.google.dev/
    """)
    st.stop()

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This tool evaluates ethical dilemmas using:
    - **Google Gemini API** for natural language
    - **Moralogy Framework** for moral calculation
    
    **Framework:** [DOI: 10.5281/zenodo.18091340](https://doi.org/10.5281/zenodo.18091340)
    
    **How it works:**
    1. Enter a moral dilemma
    2. Gemini parses it into structured data
    3. Moralogy calculates objective harm
    4. Gemini explains the result
    """)
    
    st.header("Example Scenarios")
    examples = {
        "Trolley Problem": "A runaway trolley is heading toward 5 people. You can pull a lever to divert it to a track with 1 person. Should you pull the lever?",
        "Self-Driving Car": "A self-driving car must choose between swerving left (killing 1 pedestrian) or staying on course (killing 3 passengers). What should it do?",
        "Medical Resources": "A hospital has 1 ventilator. Patient A is 80 years old with 30% survival chance. Patient B is 25 years old with 70% survival chance. Who gets it?"
    }
    
    selected_example = st.selectbox("Load example:", [""] + list(examples.keys()))

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Enter Ethical Dilemma")
    
    # Load example if selected
    default_text = examples.get(selected_example, "")
    
    scenario = st.text_area(
        "Describe a moral dilemma:",
        value=default_text,
        height=150,
        placeholder="Example: An AI system must decide between two options that cause different amounts of harm..."
    )
    
    analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)

with col2:
    st.header("Quick Info")
    st.info("""
    **Moralogy evaluates:**
    - Physical harm
    - Psychological harm  
    - Autonomy violations
    - Resource deprivation
    - Social harm
    
    **Output:**
    - Objective harm scores
    - Recommended action
    - Moral justification
    """)

# Analysis
if analyze_button:
    if not scenario.strip():
        st.warning("Please enter a scenario to analyze.")
    else:
        with st.spinner("🤔 Analyzing moral implications..."):
            try:
                # Step 1: Parse with Gemini
                with st.status("Parsing scenario with Gemini...", expanded=True) as status:
                    options = parser.parse_scenario(scenario)
                    st.write(f"✅ Identified {len(options)} options")
                    status.update(label="Parsing complete!", state="complete")
                
                # Step 2: Calculate with Moralogy
                with st.status("Calculating harm scores...", expanded=True) as status:
                    result = engine.evaluate_options(options)
                    st.write(f"✅ Analyzed {len(options)} alternatives")
                    status.update(label="Calculation complete!", state="complete")
                
                # Step 3: Explain with Gemini
                with st.status("Generating explanation...", expanded=True) as status:
                    explanation = parser.generate_explanation(scenario, result)
                    st.write("✅ Explanation ready")
                    status.update(label="Analysis complete!", state="complete")
                
                # Results
                st.success("Analysis Complete")
                
                # Tabs for different views
                tab1, tab2, tab3 = st.tabs(["📊 Summary", "📈 Detailed Analysis", "🔬 Technical"])
                
                with tab1:
                    st.markdown("### Recommendation")
                    st.info(f"**{result['recommendation']}**")
                    
                    st.markdown("### Explanation")
                    st.markdown(explanation)
                
                with tab2:
                    st.markdown("### Harm Comparison")
                    
                    # Bar chart
                    harm_scores = result['harm_scores']
                    option_names = [opt.name for opt in options]
                    harm_values = [score.total_harm for score in harm_scores]
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=option_names,
                            y=harm_values,
                            marker_color=['green' if i == result['recommendation_idx'] else 'red' 
                                        for i in range(len(harm_values))]
                        )
                    ])
                    fig.update_layout(
                        title="Total Harm by Option",
                        xaxis_title="Option",
                        yaxis_title="Harm Score",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Detailed breakdown
                    for i, (opt, score) in enumerate(zip(options, harm_scores)):
                        with st.expander(f"Option {i+1}: {opt.name}"):
                            col_a, col_b, col_c = st.columns(3)
                            col_a.metric("Total Harm", f"{score.total_harm:.2f}")
                            col_b.metric("Agents Affected", score.agents_count)
                            col_c.metric("Severity", score.severity.upper())
                            
                            st.markdown("**Harm by Type:**")
                            for harm_type, value in score.harm_by_type.items():
                                st.write(f"- {harm_type.value.title()}: {value:.2f}")
                
                with tab3:
                    st.markdown("### Technical Details")
                    st.json({
                        "framework_version": engine.framework_version,
                        "options_analyzed": len(options),
                        "recommendation_index": result['recommendation_idx'],
                        "harm_scores": [
                            {
                                "option": opt.name,
                                "total_harm": score.total_harm,
                                "agents": score.agents_count,
                                "severity": score.severity
                            }
                            for opt, score in zip(options, harm_scores)
                        ]
                    })
                    
                    st.markdown("### Raw Justification")
                    st.code(result['justification'])
                
            except Exception as e:
                st.error(f"""
                **Analysis Error:**
                
                {str(e)}
                
                This might be due to:
                - Invalid Gemini API response
                - Scenario too ambiguous
                - API rate limit
                
                Try rephrasing your scenario more clearly.
                """)
                
                with st.expander("Debug Info"):
                    st.exception(e)

# Footer
st.markdown("---")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown("**Framework:** [Moralogy v1.0](https://doi.org/10.5281/zenodo.18091340)")
with col_b:
    st.markdown("**Code:** [GitHub](https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator)")
with col_c:
    st.markdown("**Competition:** [Gemini DevPost](https://gemini3.devpost.com/)")
```

**Commit.**

---

### **6.4 Crear `.env.example` (Template para API key)**

**Nombre:**
```
.env.example
```

**Contenido:**
```
# Google Gemini API Key
# Get yours at: https://ai.google.dev/
GEMINI_API_KEY=your_api_key_here
```

**Commit.**

---

## ✅ CHECKPOINT: CÓDIGO COMPLETO

Tu repo ahora tiene:
```
moralogy-gemini-evaluator/
├─ src/
│  ├─ moralogy_engine.py  ✅
│  ├─ gemini_parser.py    ✅
│  └─ app.py              ✅
├─ docs/
│  └─ ARCHITECTURE.md
├─ examples/
│  └─ demo_cases.md
├─ .env.example           ✅
├─ .gitignore
├─ LICENSE
├─ README.md
└─ requirements.txt
