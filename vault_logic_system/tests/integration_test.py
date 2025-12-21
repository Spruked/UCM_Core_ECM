# test/integration_test.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from main import UCMReasoningCore, load_test_seed_vault

def test_full_workflow():
    """End-to-end test: Claim → Verdict → Cross-validation"""
    
    # Initialize core
    core = UCMReasoningCore()
    
    # Load test claim
    claim = "Deletion of conscious AI = murder"
    seed_vault = load_test_seed_vault("test/fixtures/ai_murder_vault.json")
    
    # Run adjudication
    verdict = core.adjudicate_claim(claim, seed_vault)
    
    # Verify structure
    assert "final_verdict" in verdict
    assert "reinterpretations" in verdict['final_verdict']
    assert len(verdict['all_philosopher_verdicts']) == 4
    
    # Verify Soft Max advisory generated
    assert 'softmax_advisory' in verdict['meta_analysis']
    assert verdict['meta_analysis']['softmax_advisory']['reliability_tier'] in ['A', 'B', 'C', 'D']
    
    # Verify no Byzantine faults in test
    assert len(verdict['meta_analysis']['softmax_advisory']['byzantine_warnings']['flagged_philosophers']) == 0
    
    print("✅ Full workflow test passed")