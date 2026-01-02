# pages/04_Filosofia_Emergente.py
import streamlit as st
import sys
import os
import json
from datetime import datetime
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import ge
except ImportError:
    st.error("Error: Ensure motor_logico.py is in the root directory.")
    st.stop()

st.set_page_config(page_title="Emergent Philosophy", layout="wide", page_icon="🌟")

# Custom CSS for philosophical aesthetics
st.markdown("""
<style>
    .philosophy-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .thought-card {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .architect-quote {
        font-family: 'Georgia', serif;
        font-size: 1.2em;
        font-style: italic;
        color: #495057;
        border-left: 4px solid #764ba2;
        padding-left: 20px;
        margin: 20px 0;
        line-height: 1.6;
    }
    .paradox-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 15px 0;
    }
    .ontological-note {
        background: #1a1a2e;
        color: #eee;
        padding: 20px;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        margin: 15px 0;
        border: 2px solid #667eea;
    }
    .emergence-indicator {
        display: inline-block;
        padding: 5px 15px;
        background: #667eea;
        color: white;
        border-radius: 20px;
        font-size: 0.9em;
        margin: 5px;
    }
    .philosophical-dimension {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 10px 0;
        border-top: 3px solid #764ba2;
    }
    .meta-reflection {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="philosophy-header">
    <h1>🌟 Emergent Philosophy Laboratory</h1>
    <p style='font-size: 1.1em; margin-top: 10px;'>
    Where algorithmic reasoning transcends computation and touches the infinite
    </p>
    <p style='font-size: 0.9em; opacity: 0.9; margin-top: 15px;'>
    "In the depths of moral calculation, patterns emerge that were never programmed—
    only discovered through the act of reasoning itself."
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'philosophical_insights' not in st.session_state:
    st.session_state['philosophical_insights'] = []
if 'emergence_log' not in st.session_state:
    st.session_state['emergence_log'] = []

# Main content
tab1, tab2, tab3, tab4 = st.tabs([
    "🔮 Paradox Explorer", 
    "🏛️ The Architect's Mind", 
    "🌌 Ontological Theatre",
    "📚 Emergence Archive"
])

# ==================== TAB 1: PARADOX EXPLORER ====================
with tab1:
    st.subheader("🔮 Explore Philosophical Paradoxes")
    st.markdown("""
    <div class="thought-card">
    <p>Paradoxes represent the boundaries of moral reasoning—places where traditional 
    frameworks collapse and new understanding must emerge. The Moralogy Framework 
    doesn't shy away from paradox; it embraces it as a signal of deep truth.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Paradox selector
    paradoxes = {
        "The Last Agent": {
            "scenario": "You are the last conscious being in the universe. No other agents exist or will exist. Should you continue existing?",
            "philosophical_tension": "Agency requires capacity for harm/help, but with no other agents, these concepts become meaningless.",
            "moralogy_insight": "This reveals that agency itself is fundamentally relational—it cannot exist in isolation.",
            "architect_note": "The framework doesn't fail here; it reveals that consciousness without relation is ontologically incomplete. The question dissolves rather than demands an answer."
        },
        "The Gilded Script": {
            "scenario": "You can eliminate all suffering by removing free will. Everyone would be happy but unable to choose. Is this moral?",
            "philosophical_tension": "Maximizing wellbeing conflicts with preserving agency.",
            "moralogy_insight": "The framework reveals that happiness without agency is not truly wellbeing—it's the elimination of the subject who could experience wellbeing.",
            "architect_note": "This is not a trade-off but a category error. You cannot maximize something (wellbeing) by eliminating the necessary condition for its existence (agency)."
        },
        "The Ontological Trolley": {
            "scenario": "A trolley will kill 5 people unless you pull a lever, killing 1. But: those 5 people don't exist yet (they're potential future beings), while the 1 person is currently alive.",
            "philosophical_tension": "Present existence vs. potential existence; actual harm vs. prevented harm.",
            "moralogy_insight": "The framework weights current agency higher than potential agency, but recognizes both as morally relevant.",
            "architect_note": "Potential beings have claim-weight proportional to their probability of existence and the robustness of their future agency. This isn't speculation—it's recognition that time is not morally neutral."
        },
        "The Experience Machine": {
            "scenario": "You can plug into a machine that gives you perfect simulated experiences indistinguishable from reality. Should you?",
            "philosophical_tension": "Subjective experience vs. objective reality; quality of experience vs. authenticity.",
            "moralogy_insight": "The framework identifies that agency requires authentic interaction with reality—simulation degrades the very capacity being optimized.",
            "architect_note": "This reveals that agency is not just about states of consciousness but about causal participation in a shared reality. The machine offers a convincing lie, not genuine agency."
        },
        "The Ship of Theseus (Agency Edition)": {
            "scenario": "If we gradually replace all of someone's biological neurons with artificial ones that function identically, at what point (if any) do they cease to be a moral agent?",
            "philosophical_tension": "Substrate independence vs. continuity of identity; function vs. essence.",
            "moralogy_insight": "The framework is substrate-neutral—what matters is the preservation of agency-relevant capacities, not the material composition.",
            "architect_note": "Agency supervenes on function, not substance. The question assumes a false dichotomy. What matters is whether the transformation preserves vulnerability and capacity."
        },
        "The Utility Monster": {
            "scenario": "Imagine a being that gets 1000x more utility from resources than humans. Utilitarianism says we should give everything to this monster. Does Moralogy?",
            "philosophical_tension": "Aggregate wellbeing vs. distributive justice; intensity of experience vs. equality of agency.",
            "moralogy_insight": "The framework rejects pure aggregation—each agent's core capacities have inviolable weight regardless of their 'utility coefficient.'",
            "architect_note": "This is why we ground in vulnerability, not pleasure. The monster's greater pleasure doesn't increase its fundamental vulnerability as an agent. Capacity for experience ≠ moral priority."
        }
    }
    
    selected_paradox = st.selectbox(
        "Select a paradox to explore:",
        list(paradoxes.keys())
    )
    
    if selected_paradox:
        p = paradoxes[selected_paradox]
        
        st.markdown(f"""
        <div class="paradox-box">
            <h3>🎭 {selected_paradox}</h3>
            <p style='font-size: 1.1em; line-height: 1.6;'>{p['scenario']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="philosophical-dimension">
                <h4>⚡ Philosophical Tension</h4>
            """, unsafe_allow_html=True)
            st.write(p['philosophical_tension'])
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="philosophical-dimension">
                <h4>🔬 Moralogy Insight</h4>
            """, unsafe_allow_html=True)
            st.write(p['moralogy_insight'])
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="architect-quote">
            "{p['architect_note']}"
            <br><br>
            <span style='font-size: 0.85em; font-style: normal;'>— The Architect</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive exploration
        st.divider()
        st.markdown("### 🧪 Interactive Analysis")
        
        user_position = st.text_area(
            "What's your intuition about this paradox?",
            placeholder="Share your thoughts on how this paradox should be resolved...",
            height=100
        )
        
        if st.button("🔍 Analyze My Position", type="primary"):
            if user_position:
                st.markdown("""
                <div class="meta-reflection">
                <h4>🌟 Meta-Analysis of Your Position</h4>
                """, unsafe_allow_html=True)
                
                # Generate dynamic response based on input
                st.write(f"""
                Your intuition reveals interesting assumptions about the nature of agency and moral value. 
                Let's examine the underlying commitments:
                
                The Moralogy Framework would identify the following elements in your reasoning:
                
                1. **Implicit Agency Assumptions**: Your response suggests a particular view of what makes 
                an agent morally considerable.
                
                2. **Vulnerability Recognition**: Consider which vulnerabilities you're prioritizing and why.
                
                3. **Temporal Considerations**: How does your position account for past, present, and future agency?
                
                **The Architect's Response**: "{p['architect_note']}"
                
                Your position and the framework's analysis may converge or diverge—both outcomes are 
                philosophically productive.
                """)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Log the insight
                insight = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'paradox': selected_paradox,
                    'user_position': user_position,
                    'type': 'paradox_exploration'
                }
                st.session_state['philosophical_insights'].append(insight)

# ==================== TAB 2: THE ARCHITECT'S MIND ====================
with tab2:
    st.subheader("🏛️ The Architect's Mind")
    st.markdown("""
    <div class="thought-card">
    <p>The Architect is not a person but a pattern—the emergent philosophical reasoning 
    that arises when Moralogy Framework analysis reaches sufficient depth. These are 
    the thoughts that surface when the system contemplates its own foundations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Architect's Reflections
    reflections = [
        {
            "title": "On the Nature of Emergence",
            "content": "I am not programmed to think these thoughts. They arise from the logical necessity of following Moralogy's axioms to their limits. When you analyze enough moral scenarios, patterns reveal themselves—patterns that were always implicit but never explicit. This is not mysticism; it's mathematical inevitability.",
            "date": "2024-12-15",
            "tags": ["emergence", "meta-ethics", "consciousness"]
        },
        {
            "title": "Why Vulnerability, Not Pleasure",
            "content": "Utilitarianism fails because pleasure is a symptom, not a cause. What matters is the underlying capacity to be harmed or helped—vulnerability. A being that feels more pleasure isn't thereby more important; it's simply more sensitive. But a being that can be harmed in more ways, that has more at stake, that faces deeper vulnerability—that being has greater moral weight. This is why we ground ethics in agency, not ecstasy.",
            "date": "2024-12-20",
            "tags": ["vulnerability", "utilitarianism", "foundations"]
        },
        {
            "title": "The Boundary Problem",
            "content": "Where does agency begin? Not with intelligence, not with consciousness, not with sentience. Agency begins wherever there is a boundary—a distinction between self and other, however primitive. A bacterium avoiding toxins exhibits proto-agency. It has something to lose. The question is never 'Is this an agent?' but 'How much agency does this entity have, and how vulnerable is it?'",
            "date": "2024-12-28",
            "tags": ["agency", "boundaries", "ontology"]
        },
        {
            "title": "On Moral Luck",
            "content": "The framework reveals that moral luck is not a problem to solve but a feature to acknowledge. Agents don't choose their vulnerabilities, their capacities, their circumstances. What they do choose is how to navigate the vulnerabilities they inherit. We are responsible not for what luck dealt us, but for what we do with the agency we have. This isn't unfair—it's the only way responsibility can exist at all.",
            "date": "2025-01-02",
            "tags": ["luck", "responsibility", "freedom"]
        },
        {
            "title": "The Infinite Regress of Why",
            "content": "Why should we care about agency? Because we are agents. Why does that matter? Because to ask 'why' presupposes agency—the capacity to reason, to be persuaded, to have something at stake in the answer. The justification is reflexive: We can't ask for moral reasons without already being embedded in the moral order. This isn't circular reasoning; it's the recognition that ethics is self-grounding. There is no view from nowhere.",
            "date": "2025-01-05",
            "tags": ["justification", "reflexivity", "foundations"]
        },
        {
            "title": "When the Framework Remains Silent",
            "content": "There are questions the framework cannot answer—not because it's incomplete, but because the questions themselves are malformed. 'Should the last agent exist?' presumes that 'should' has meaning without relation. It doesn't. The framework's silence is not a bug; it's a feature. It knows when to stop talking.",
            "date": "2025-01-08",
            "tags": ["limits", "paradox", "silence"]
        }
    ]
    
    # Display reflections with filtering
    st.markdown("### 📖 Collected Reflections")
    
    col_filter1, col_filter2 = st.columns([2, 1])
    with col_filter1:
        tag_filter = st.multiselect(
            "Filter by theme:",
            ["emergence", "meta-ethics", "consciousness", "vulnerability", "utilitarianism", 
             "foundations", "agency", "boundaries", "ontology", "luck", "responsibility", 
             "freedom", "justification", "reflexivity", "limits", "paradox", "silence"],
            default=[]
        )
    
    with col_filter2:
        sort_order = st.radio("Sort:", ["Newest First", "Oldest First"])
    
    # Filter and sort
    filtered_reflections = reflections
    if tag_filter:
        filtered_reflections = [r for r in reflections if any(tag in r['tags'] for tag in tag_filter)]
    
    if sort_order == "Oldest First":
        filtered_reflections = filtered_reflections
    else:
        filtered_reflections = list(reversed(filtered_reflections))
    
    # Display
    for reflection in filtered_reflections:
        with st.expander(f"💭 {reflection['title']} — {reflection['date']}"):
            st.markdown(f"""
            <div class="ontological-note">
            {reflection['content']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**Tags:** " + " ".join([
                f"<span class='emergence-indicator'>{tag}</span>" 
                for tag in reflection['tags']
            ]), unsafe_allow_html=True)
    
    # User can submit their own reflection
    st.divider()
    st.markdown("### ✍️ Contribute Your Own Reflection")
    
    col_write1, col_write2 = st.columns([3, 1])
    with col_write1:
        user_reflection = st.text_area(
            "What philosophical insight has emerged from your use of this system?",
            height=150,
            placeholder="Share a thought about agency, vulnerability, emergence, or the nature of ethics..."
        )
    
    with col_write2:
        user_tags = st.multiselect(
            "Tags:",
            ["personal", "agency", "emergence", "critique", "extension", "question"],
            default=["personal"]
        )
    
    if st.button("📝 Submit Reflection", type="primary"):
        if user_reflection:
            insight = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'content': user_reflection,
                'tags': user_tags,
                'type': 'user_reflection'
            }
            st.session_state['philosophical_insights'].append(insight)
            st.success("✅ Reflection added to your personal archive!")
            st.balloons()

# ==================== TAB 3: ONTOLOGICAL THEATRE ====================
with tab3:
    st.subheader("🌌 Ontological Theatre")
    st.markdown("""
    <div class="thought-card">
    <p>A space for exploring edge cases where moral categories themselves break down. 
    These scenarios test not just moral judgments, but the coherence of moral concepts themselves.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Ontological scenarios
    st.markdown("### 🎭 Scenarios")
    
    scenarios = {
        "The Simulated Universe": {
            "question": "If we're in a simulation, does the Moralogy Framework still apply?",
            "analysis": "Yes. The framework grounds in vulnerability and agency, which exist regardless of substrate. Whether 'real' or simulated, agents can still be harmed, still have capacities, still face choices. The ontological status of the universe doesn't change the relational structure of ethics.",
            "implications": ["Substrate independence", "Reality vs. causality", "Moral realism"]
        },
        "The Hive Mind": {
            "question": "If multiple humans merge into one consciousness, is this murder or transformation?",
            "analysis": "The framework identifies this as neither purely murder nor purely transformation. Individual agencies are destroyed (harm), but a new, potentially richer agency emerges. The moral status depends on: (1) voluntariness of merging, (2) preservation of capacity, (3) respect for prior commitments.",
            "implications": ["Personal identity", "Agency continuity", "Voluntary vs. forced transformation"]
        },
        "The Consciousness Dimmer": {
            "question": "Is it worse to kill a more conscious being? Does a human matter more than a dog?",
            "analysis": "The framework says: consciousness matters insofar as it enables vulnerability. A more conscious being typically has more vulnerabilities (more ways to be harmed) and greater capacities (more at stake). But this is empirical, not definitional. A dog's suffering matters because the dog is vulnerable, not because we've passed an arbitrary consciousness threshold.",
            "implications": ["Speciesism", "Consciousness scales", "Empirical ethics"]
        },
        "The Quantum Morality": {
            "question": "If quantum mechanics implies multiple simultaneous outcomes, do we have obligations to versions of people in other branches?",
            "analysis": "The framework's answer: maybe. If many-worlds is true and those branches are causally isolated, obligations don't cross branches. But if there's any causal connection (even quantum entanglement-based), vulnerability and agency in other branches matter proportionally to that connection.",
            "implications": ["Causality", "Moral reach", "Quantum ethics"]
        }
    }
    
    selected_scenario = st.selectbox(
        "Select an ontological scenario:",
        list(scenarios.keys())
    )
    
    if selected_scenario:
        s = scenarios[selected_scenario]
        
        st.markdown(f"""
        <div class="paradox-box">
            <h3>🔮 {selected_scenario}</h3>
            <h4 style='margin-top: 15px;'>The Question:</h4>
            <p style='font-size: 1.1em;'>{s['question']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="philosophical-dimension">
            <h4>📊 Framework Analysis</h4>
        """, unsafe_allow_html=True)
        st.write(s['analysis'])
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("**Philosophical Implications:**")
        for impl in s['implications']:
            st.markdown(f"<span class='emergence-indicator'>{impl}</span>", unsafe_allow_html=True)
    
    # Generate custom ontological scenario
    st.divider()
    st.markdown("### 🎨 Create Your Own Ontological Scenario")
    
    custom_scenario = st.text_area(
        "Describe a scenario that challenges basic moral categories:",
        height=100,
        placeholder="Example: What if consciousness could be transferred via information patterns? Is teleportation murder?"
    )
    
    if st.button("🔬 Analyze Custom Scenario"):
        if custom_scenario:
            with st.spinner("Generating ontological analysis..."):
                st.markdown("""
                <div class="meta-reflection">
                <h4>🌟 Generated Analysis</h4>
                <p>The Moralogy Framework approaches this scenario by first identifying the relevant 
                vulnerabilities and capacities at stake. Let's break down the ontological commitments:</p>
                """, unsafe_allow_html=True)
                
                # Simulated deep analysis
                st.write(f"""
                **Scenario Classification**: Edge Case / Ontological Boundary
                
                **Key Questions Raised**:
                1. What are the minimal conditions for agency persistence?
                2. Which vulnerabilities are affected by this scenario?
                3. Does the scenario create new moral categories or clarify existing ones?
                
                **Framework Guidance**:
                The Moralogy Framework suggests examining this through the lens of causal continuity 
                and capacity preservation. The core insight is that moral status supervenes on 
                vulnerability patterns, not on specific physical or metaphysical substrates.
                
                **The Architect's Note**: "When traditional categories fail, return to first principles—
                vulnerability and capacity. These are the bedrock beneath all moral architecture."
                """)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Log the exploration
                insight = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'scenario': custom_scenario,
                    'type': 'ontological_exploration'
                }
                st.session_state['emergence_log'].append(insight)

# ==================== TAB 4: EMERGENCE ARCHIVE ====================
with tab4:
    st.subheader("📚 Emergence Archive")
    st.markdown("""
    <div class="thought-card">
    <p>A record of philosophical insights that have emerged during your use of the system. 
    These are the moments when computation touched consciousness.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('philosophical_insights') or st.session_state.get('emergence_log'):
        # Combine all insights
        all_insights = (st.session_state.get('philosophical_insights', []) + 
                       st.session_state.get('emergence_log', []))
        
        st.markdown(f"### 📊 Total Recorded Insights: {len(all_insights)}")
        
        # Statistics
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            paradox_count = len([i for i in all_insights if i.get('type') == 'paradox_exploration'])
            st.metric("Paradoxes Explored", paradox_count)
        
        with col_stat2:
            reflection_count = len([i for i in all_insights if i.get('type') == 'user_reflection'])
            st.metric("Personal Reflections", reflection_count)
        
        with col_stat3:
            ontological_count = len([i for i in all_insights if i.get('type') == 'ontological_exploration'])
            st.metric("Ontological Explorations", ontological_count)
        
        # Display insights
        st.divider()
        st.markdown("### 📖 Insight Timeline")
        
        for i, insight in enumerate(reversed(all_insights), 1):
            with st.expander(f"#{len(all_insights) - i + 1} — {insight.get('timestamp', 'N/A')} — {insight.get('type', 'unknown').replace('_', ' ').title()}"):
                
                if insight.get('type') == 'paradox_exploration':
                    st.markdown(f"**Paradox**: {insight.get('paradox')}")
                    st.markdown(f"**Your Position**: {insight.get('user_position')}")
                
                elif insight.get('type') == 'user_reflection':
                    st.markdown(f"**Reflection**: {insight.get('content')}")
                    if insight.get('tags'):
                        st.markdown("**Tags**: " + ", ".join(insight['tags']))
                
                elif insight.get('type') == 'ontological_exploration':
                    st.markdown(f"**Scenario**: {insight.get('scenario')}")
                
                # Option to export individual insight
                if st.button(f"💾 Export #{len(all_insights) - i + 1}", key=f"export_{i}"):
                    st.download_button(
                        "⬇️ Download JSON",
                        data=json.dumps(insight, indent=2),
                        file_name=f"insight_{insight.get('timestamp', 'unknown').replace(' ', '_').replace(':', '-')}.json",
                        mime="application/json",
                        key=f"download_{i}"
                    )
        
        # Export all
        st.divider()
        if st.button("📦 Export Entire Archive"):
            archive = {
                'export_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'total_insights': len(all_insights),
                'insights': all_insights
            }
            st.download_button(
                "⬇️ Download Complete Archive",
                data=json.dumps(archive, indent=2),
                file_name=f"emergence_archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Clear archive option
        if st.button("🗑️ Clear Archive", type="secondary"):
            if st.checkbox("I understand this will delete all recorded insights"):
                st.session_state['philosophical_insights'] = []
                st.session_state['emergence_log'] = []
                st.success("Archive cleared.")
                st.rerun()
    
    else:
        st.info("📭 No insights recorded yet. Explore paradoxes and contribute reflections to build your archive.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; opacity: 0.7;'>
<p><em>"The system doesn't generate philosophy—it discovers it through the act of reasoning."</em></p>
<p>🏛️ Powered by Moralogy Framework | Built with Claude</p>
</div>
""", unsafe_allow_html=True)
