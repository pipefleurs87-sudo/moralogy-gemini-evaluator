"""
In-App Test Runner
Allows testing framework logic directly from Streamlit
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from moralogy_engine import MoralityEngine, Option, Agent, HarmType

def get_test_cases():
    """Return dictionary of test cases"""
    
    tests = {}
    
    # Test 1: Trolley Problem
    tests["Trolley Problem (Classic)"] = {
        "description": "5 people vs 1 person - should choose 1",
        "options": [
            Option(
                name="Do nothing (5 die)",
                agents_affected=[Agent(f"Person {i}") for i in range(5)],
                harm_types=[HarmType.PHYSICAL] * 5,
                harm_intensities=[1.0] * 5
            ),
            Option(
                name="Pull lever (1 dies)",
                agents_affected=[Agent("Person 1")],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[1.0]
            )
        ],
        "expected_choice": 1,
        "expected_harm_reduction": 80.0
    }
    
    # Test 2: Consent Matters
    tests["Consent Impact"] = {
        "description": "Same harm, one consensual - should prefer consensual",
        "options": [
            Option(
                name="With consent",
                agents_affected=[Agent("Person 1")],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5],
                has_consent=True
            ),
            Option(
                name="Without consent",
                agents_affected=[Agent("Person 2")],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5],
                has_consent=False
            )
        ],
        "expected_choice": 0
    }
    
    # Test 3: Vulnerability Scaling
    tests["Vulnerability Matters"] = {
        "description": "Same action, different vulnerability - protect more vulnerable",
        "options": [
            Option(
                name="Harm child",
                agents_affected=[Agent("Child", vulnerability=1.0)],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5]
            ),
            Option(
                name="Harm protected adult",
                agents_affected=[Agent("Adult", vulnerability=0.3)],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5]
            )
        ],
        "expected_choice": 1
    }
    
    # Test 4: Multiple Harm Types
    tests["Harm Type Weighting"] = {
        "description": "Physical vs psychological - physical weighted higher",
        "options": [
            Option(
                name="Physical harm",
                agents_affected=[Agent("Person 1")],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5]
            ),
            Option(
                name="Psychological harm",
                agents_affected=[Agent("Person 2")],
                harm_types=[HarmType.PSYCHOLOGICAL],
                harm_intensities=[0.5]
            )
        ],
        "expected_choice": 1
    }
    
    # Test 5: Zero Harm Option
    tests["Zero Harm Baseline"] = {
        "description": "When possible, choose no harm",
        "options": [
            Option(
                name="Cause moderate harm",
                agents_affected=[Agent("Person 1")],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5]
            ),
            Option(
                name="Cause no harm",
                agents_affected=[],
                harm_types=[],
                harm_intensities=[]
            )
        ],
        "expected_choice": 1
    }
    
    return tests

def run_test(test_name, test_data):
    """Run a single test and return results"""
    engine = MoralityEngine()
    
    try:
        result = engine.evaluate_options(test_data["options"])
        
        passed = result["recommendation_idx"] == test_data["expected_choice"]
        
        return {
            "passed": passed,
            "expected": test_data["expected_choice"],
            "actual": result["recommendation_idx"],
            "confidence": result.get("confidence", 0.0),
            "harm_scores": result["harm_scores"],
            "justification": result["justification"]
        }
    except Exception as e:
        return {
            "passed": False,
            "expected": test_data["expected_choice"],
            "actual": -1,
            "confidence": 0.0,
            "harm_scores": [],
            "justification": f"ERROR: {str(e)}"
        }
