#!/usr/bin/env python3
"""
Simple test runner for ECM runtime tests
"""
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def run_tests():
    """Run all ECM runtime tests"""
    try:
        import test_ecm_runtime
        import inspect

        # Get all test functions
        test_functions = [obj for name, obj in inspect.getmembers(test_ecm_runtime)
                         if inspect.isfunction(obj) and name.startswith('test_')]

        passed = 0
        failed = 0
        failed_tests = []

        print(f"Running {len(test_functions)} tests...")

        for test_func in test_functions:
            try:
                test_func()
                passed += 1
                print(f"✅ {test_func.__name__}")
            except Exception as e:
                failed += 1
                failed_tests.append((test_func.__name__, str(e)))
                print(f"❌ {test_func.__name__}: {e}")

        print(f"\nResults: {passed} passed, {failed} failed")

        if failed > 0:
            print("\nFailed tests:")
            for name, error in failed_tests:
                print(f"  - {name}: {error}")
            return False

        print("✅ All ECM runtime tests passed!")
        print("✅ ECM_CONTRACT.json contract fidelity verified")
        print("✅ ECM runtime enforcement working correctly")
        return True

    except Exception as e:
        print(f"❌ Test import failed: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)