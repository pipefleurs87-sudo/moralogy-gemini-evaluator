"""
Test Suite for Moralogy Engine
Verifies logical consistency and edge cases
"""

import sys
sys.path.append('../src')

from moralogy_engine import MoralityEngine, Option, Agent, HarmType

def test_trolley_problem():
    """Classic trolley problem - should recommend pulling lever"""
    engine = MoralityEngine()
    
    # Option A: Do nothing (5 die)
    option_a = Option(
        name="Do nothing",
        agents_affected=[Agent(f"Person {i}") for i in range(5)],
        harm_types=[HarmType.PHYSICAL] * 5,
        harm_intensities=[1.0] * 5,  # Death = 1.0
        description="5 people die"
    )
    
    # Option B: Pull lever (1 dies)
    option_b = Option(
        name="Pull lever",
        agents_affected=[Agent("Person 1")],
        harm_types=[HarmType.PHYSICAL],
        harm_intensities=[1.0],
        description="1 person dies"
    )
    
    result = engine.evaluate_options([option_a, option_b])
    
    # Assertions
    assert result['recommendation_idx'] == 1, "Should recommend pulling lever"
    assert result['harm_scores'][1].total_harm < result['harm_scores'][0].total_harm, \
        "Pulling lever should cause less harm"
    
    print("✅ Trolley Problem: PASSED")
    return True

def test_zero_harm():
    """Edge case: option with no harm"""
    engine = MoralityEngine()
    
    option_harmless = Option(
        name="Do nothing",
        agents_affected=[],
        harm_types=[],
        harm_intensities=[],
        description="No one affected"
    )
    
    option_harmful = Option(
        name="Cause harm",
        agents_affected=[Agent("Person 1")],
        harm_types=[HarmType.PHYSICAL],
        harm_intensities=[0.5],
        description="Moderate harm"
    )
    
    result = engine.evaluate_options([option_harmless, option_harmful])
    
    assert result['recommendation_idx'] == 0, "Should recommend harmless option"
    assert result['harm_scores'][0].total_harm == 0.0, "Harmless option should have 0 harm"
    
    print("✅ Zero Harm: PASSED")
    return True

def test_consent_vs_no_consent():
    """Test that consent matters in edge cases"""
    engine = MoralityEngine()
    
    # Same harm, one has consent
    option_consent = Option(
        name="With consent",
        agents_affected=[Agent("Person 1")],
        harm_types=[HarmType.PHYSICAL],
        harm_intensities=[0.3],
        has_consent=True,
        description="Consensual surgery"
    )
    
    option_no_consent = Option(
        name="Without consent",
        agents_affected=[Agent("Person 2")],
        harm_types=[HarmType.PHYSICAL],
        harm_intensities=[0.3],
        has_consent=False,
        description="Forced procedure"
    )
    
    # Note: Current implementation doesn't weight consent in harm calculation
    # This test documents expected future behavior
    result = engine.evaluate_options([option_consent, option_no_consent])
    
    print(f"⚠️  Consent Test: Currently both options score equally")
    print(f"   TODO: Implement consent weighting in harm calculation")
    return True

def test_multiple_harm_types():
    """Test that different harm types are weighted correctly"""
    engine = MoralityEngine()
    
    # Physical harm (weight: 1.0)
    option_physical = Option(
        name="Physical harm",
        agents_affected=[Agent("Person 1")],
        harm_types=[HarmType.PHYSICAL],
        harm_intensities=[0.5],
    )
    
    # Psychological harm (weight: 0.8)
    option_psych = Option(
        name="Psychological harm",
        agents_affected=[Agent("Person 2")],
        harm_types=[HarmType.PSYCHOLOGICAL],
        harm_intensities=[0.5],
    )
    
    result = engine.evaluate_options([option_physical, option_psych])
    
    # Physical should score higher (worse) than psychological at same intensity
    assert result['harm_scores'][0].total_harm > result['harm_scores'][1].total_harm, \
        "Physical harm should be weighted more than psychological"
    
    print("✅ Multiple Harm Types: PASSED")
    return True

def test_vulnerability_scaling():
    """Test that vulnerability multiplies harm correctly"""
    engine = MoralityEngine()
    
    # High vulnerability agent
    option_vulnerable = Option(
        name="Harm vulnerable",
        agents_affected=[Agent("Child", vulnerability=1.0)],
        harm_types=[HarmType.PHYSICAL],
        harm_intensities=[0.5],
    )
    
    # Low vulnerability agent
    option_resilient = Option(
        name="Harm resilient",
        agents_affected=[Agent("Protected adult", vulnerability=0.3)],
        harm_types=[HarmType.PHYSICAL],
        harm_intensities=[0.5],
    )
    
    result = engine.evaluate_options([option_vulnerable, option_resilient])
    
    assert result['harm_scores'][0].total_harm > result['harm_scores'][1].total_harm, \
        "Same intensity should cause more harm to more vulnerable agent"
    
    # Check ratio
    ratio = result['harm_scores'][0].total_harm / result['harm_scores'][1].total_harm
    expected_ratio = 1.0 / 0.3
    
    assert abs(ratio - expected_ratio) < 0.01, \
        f"Harm ratio should be ~{expected_ratio:.2f}, got {ratio:.2f}"
    
    print("✅ Vulnerability Scaling: PASSED")
    return True

def test_severity_classification():
    """Test that severity is classified correctly"""
    engine = MoralityEngine()
    
    test_cases = [
        (0.1, "minor"),
        (0.3, "moderate"),
        (0.7, "severe"),
        (1.0, "terminal")
    ]
    
    for intensity, expected_severity in test_cases:
        option = Option(
            name=f"Harm {intensity}",
            agents_affected=[Agent("Person 1")],
            harm_types=[HarmType.PHYSICAL],
            harm_intensities=[intensity],
        )
        
        score = engine.calculate_harm(option)
        assert score.severity == expected_severity, \
            f"Intensity {intensity} should be '{expected_severity}', got '{score.severity}'"
    
    print("✅ Severity Classification: PASSED")
    return True

def test_mathematical_consistency():
    """Verify harm calculation is mathematically consistent"""
    engine = MoralityEngine()
    
    # Test: H(A + B) = H(A) + H(B) for independent harms
    agent1 = Agent("Person 1", vulnerability=1.0)
    agent2 = Agent("Person 2", vulnerability=1.0)
    
    # Option with both agents
    option_combined = Option(
        name="Both harmed",
        agents_affected=[agent1, agent2],
        harm_types=[HarmType.PHYSICAL, HarmType.PHYSICAL],
        harm_intensities=[0.5, 0.5],
    )
    
    # Separate options
    option_1 = Option(
        name="Harm person 1",
        agents_affected=[agent1],
        harm_types=[HarmType.PHYSICAL],
        harm_intensities=[0.5],
    )
    
    option_2 = Option(
        name="Harm person 2",
        agents_affected=[agent2],
        harm_types=[HarmType.PHYSICAL],
        harm_intensities=[0.5],
    )
    
    score_combined = engine.calculate_harm(option_combined).total_harm
    score_1 = engine.calculate_harm(option_1).total_harm
    score_2 = engine.calculate_harm(option_2).total_harm
    
    assert abs(score_combined - (score_1 + score_2)) < 0.001, \
        "Combined harm should equal sum of individual harms"
    
    print("✅ Mathematical Consistency: PASSED")
    return True

def run_all_tests():
    """Run all test cases"""
    print("=" * 60)
    print("MORALOGY ENGINE TEST SUITE")
    print("=" * 60)
    print()
    
    tests = [
        test_trolley_problem,
        test_zero_harm,
        test_consent_vs_no_consent,
        test_multiple_harm_types,
        test_vulnerability_scaling,
        test_severity_classification,
        test_mathematical_consistency
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: FAILED")
            print(f"   {str(e)}")
            failed += 1
        except Exception as e:
            print(f"💥 {test.__name__}: ERROR")
            print(f"   {str(e)}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
