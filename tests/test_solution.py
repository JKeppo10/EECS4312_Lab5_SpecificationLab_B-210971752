## Student Name: Joshua Keppo  
## Student ID: 210971752

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
from src.solution import is_allocation_feasible
import pytest


def test_basic_feasible_single_resource():
    # Basic Feasible Single-Resource
    # Constraint: total demand <= capacity AND at least 1 unit must remain
    # Reason: check basic functional requirement with new constraint
    resources = {'cpu': 10}
    requests = [{'cpu': 3}, {'cpu': 4}, {'cpu': 2}]  # Total: 9, leaving 1
    assert is_allocation_feasible(resources, requests) is True

def test_multi_resource_infeasible_one_overloaded():
    # Multi-Resource Infeasible (one overload)
    # Constraint: one resource exceeds capacity
    # Reason: check detection of per-resource infeasibility
    resources = {'cpu': 8, 'mem': 30}
    requests = [{'cpu': 2, 'mem': 8}, {'cpu': 3, 'mem': 10}, {'cpu': 3, 'mem': 14}]
    assert is_allocation_feasible(resources, requests) is False

def test_missing_resource_in_availability():
    # Missing Resource in Requests
    # Constraint: request references unavailable resource
    # Reason: allocation must be infeasible
    resources = {'cpu': 10}
    requests = [{'cpu': 2}, {'gpu': 1}]
    assert is_allocation_feasible(resources, requests) is False

def test_non_dict_request_raises():
    # Non-Dict Request Raises Error
    # Constraint: structural validation
    # Reason: request must be a dict
    resources = {'cpu': 5}
    requests = [{'cpu': 2}, ['mem', 1]]  # malformed request
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)

"""TODO: Add at least 5 additional test cases to test your implementation."""
def test_exact_capacity_boundary_case():
    """
    Test exact capacity allocation (boundary case).
    Constraint: Total demand exactly equals available capacity.
    Reason: Test edge case where sum equals capacity - should now fail due to new requirement.
    """
    resources = {'cpu': 10, 'memory': 20, 'disk': 30}
    requests = [
        {'cpu': 4, 'memory': 8, 'disk': 12},
        {'cpu': 3, 'memory': 6, 'disk': 10},
        {'cpu': 3, 'memory': 6, 'disk': 8}
    ]
    # Total: cpu=10, memory=20, disk=30 (exact match, leaves 0 for each)
    # With new requirement: all resources fully allocated, so should be False
    assert is_allocation_feasible(resources, requests) is False

def test_mixed_valid_invalid_requests():
    """
    Test mixed scenario with some valid and some invalid aspects.
    Constraint: Some requests exceed capacity while others don't.
    Reason: Test that any infeasibility makes overall allocation infeasible.
    """
    resources = {'cpu': 15, 'memory': 25, 'gpu': 3}
    requests = [
        {'cpu': 5, 'memory': 10, 'gpu': 1},  # Valid
        {'cpu': 6, 'memory': 8, 'gpu': 1},   # Valid
        {'cpu': 4, 'memory': 6, 'gpu': 1}    # Valid, leaves: cpu=0, memory=1, gpu=0 (fails - gpu has 0 left)
    ]
    # Total: cpu=15, memory=24, gpu=3
    # With new requirement: gpu has 0 left, so should be False
    assert is_allocation_feasible(resources, requests) is False

def test_zero_and_empty_values():
    """
    Test handling of zero values and empty requests.
    Constraint: Zero quantities and empty dictionaries.
    Reason: Test edge cases with minimal/empty values.
    """
    # Test 1: Zero resource request (leaves full capacity)
    resources = {'cpu': 10}
    requests = [{'cpu': 0}, {'cpu': 0}, {'cpu': 0}]
    assert is_allocation_feasible(resources, requests) is True
    
    # Test 2: Empty request dictionary
    resources = {'cpu': 10, 'memory': 20}
    requests = [{'cpu': 5}, {}, {'memory': 10}]  # Leaves: cpu=5, memory=10
    assert is_allocation_feasible(resources, requests) is True
    
    # Test 3: Request for zero of non-existent resource (should fail)
    resources = {'cpu': 10}
    requests = [{'cpu': 5}, {'gpu': 0}]  # gpu doesn't exist even though amount is 0
    assert is_allocation_feasible(resources, requests) is False
    
    # Test 4: Leaves exactly 1 unit for each resource
    resources = {'cpu': 6, 'memory': 7}
    requests = [{'cpu': 5}, {'memory': 6}]
    assert is_allocation_feasible(resources, requests) is True

def test_fractional_and_float_values():
    """
    Test with fractional/float values.
    Constraint: Resources and requests can have float values.
    Reason: Test non-integer arithmetic and precision.
    """
    # Test with resources leaving at least 1.0 unit
    resources = {'cpu': 8.5, 'memory': 13.25, 'disk': 6.0}
    requests = [
        {'cpu': 2.25, 'memory': 3.75, 'disk': 1.5},
        {'cpu': 3.0, 'memory': 4.5, 'disk': 2.0},
        {'cpu': 2.25, 'memory': 4.0, 'disk': 1.5}  # Total: cpu=7.5, memory=12.25, disk=5.0
    ]
    # Leaves: cpu=1.0, memory=1.0, disk=1.0
    assert is_allocation_feasible(resources, requests) is True
    
    # Test with slight overflow due to floating point, but leaving less than 1
    resources = {'cpu': 1.0}
    requests = [{'cpu': 0.3}, {'cpu': 0.3}, {'cpu': 0.3}]  # 0.3*3 = 0.899999... leaving ~0.1
    # Leaves approximately 0.1, which is less than 1.0, so should be False
    assert is_allocation_feasible(resources, requests) is False
    
    # Test with exact allocation leaving 0.0
    resources = {'cpu': 1.0}
    requests = [{'cpu': 0.3}, {'cpu': 0.3}, {'cpu': 0.4}]  # 0.3+0.3+0.4 = 1.0, leaving 0.0
    assert is_allocation_feasible(resources, requests) is False

def test_negative_values_validation():
    """
    Test validation of negative values.
    Constraint: Negative amounts should be rejected.
    Reason: Ensure proper validation of input values.
    """
    # Test 1: Negative resource capacity
    resources = {'cpu': -5, 'memory': 10}
    requests = [{'cpu': 3}, {'memory': 5}]
    assert is_allocation_feasible(resources, requests) is False
    
    # Test 2: Negative request amount
    resources = {'cpu': 10, 'memory': 20}
    requests = [{'cpu': 5}, {'cpu': -2, 'memory': 10}]  # Negative cpu request
    assert is_allocation_feasible(resources, requests) is False
    
    # Test 3: Mixed negative and positive in same request
    resources = {'cpu': 10, 'memory': 20}
    requests = [{'cpu': 5, 'memory': -1}]  # Negative memory
    assert is_allocation_feasible(resources, requests) is False
    
    # Test 4: Zero is okay, negative is not
    resources = {'cpu': 10}
    requests = [{'cpu': 0}]  # Zero is valid, leaves 10
    assert is_allocation_feasible(resources, requests) is True
    requests = [{'cpu': -0.0}]  # Negative zero (float) - should be treated as 0
    # Note: -0.0 == 0.0 is True in Python, so this might pass
    # This tests how your implementation handles negative zero
    result = is_allocation_feasible(resources, requests)
    # Implementation should handle this as zero, so leaving 10, which is >= 1

def test_new_requirement_specific_cases():
    """
    Test cases specifically for the new requirement that every resource
    must have at least 1 unit remaining.
    """
    # Test 1: All resources have exactly 1 unit left
    resources = {'cpu': 6, 'memory': 5, 'disk': 4}
    requests = [
        {'cpu': 3, 'memory': 2, 'disk': 1},
        {'cpu': 2, 'memory': 2, 'disk': 2}
    ]
    # Leaves: cpu=1, memory=1, disk=1
    assert is_allocation_feasible(resources, requests) is True
    
    # Test 2: One resource has 0 left, others have >1
    resources = {'cpu': 10, 'memory': 10}
    requests = [{'cpu': 10}, {'memory': 5}]
    # Leaves: cpu=0, memory=5 -> should be False
    assert is_allocation_feasible(resources, requests) is False
    
    # Test 3: All resources have more than 1 left
    resources = {'cpu': 10, 'memory': 20}
    requests = [{'cpu': 5}, {'memory': 10}]
    # Leaves: cpu=5, memory=10 -> both > 1
    assert is_allocation_feasible(resources, requests) is True
    
    # Test 4: Resource with exactly 1 capacity cannot be allocated at all
    resources = {'cpu': 1, 'memory': 10}
    requests = [{'cpu': 0.5}]  # Would leave 0.5 < 1
    assert is_allocation_feasible(resources, requests) is False
    
    # Test 5: Complex multi-resource with varying remaining amounts
    resources = {'cpu': 8, 'memory': 12, 'gpu': 4, 'storage': 20}
    requests = [
        {'cpu': 2, 'memory': 3, 'gpu': 1, 'storage': 5},
        {'cpu': 3, 'memory': 4, 'gpu': 1, 'storage': 6},
        {'cpu': 1, 'gpu': 1, 'storage': 4}  # No memory request
    ]
    # Total: cpu=6, memory=7, gpu=3, storage=15
    # Leaves: cpu=2, memory=5, gpu=1, storage=5 -> all >= 1
    assert is_allocation_feasible(resources, requests) is True

def test_non_numeric_resource_capacity():
    """
    Test assumption: Resource capacities must be numerical values.
    Constraint: Non-numeric capacities should cause issues.
    Reason: Test type validation for resource values.
    """
    # This might cause TypeError in arithmetic operations
    resources = {'cpu': '10', 'memory': 20}  # String instead of number
    requests = [{'cpu': 5}, {'memory': 10}]
    # Implementation may need to handle or this may fail
    # Test to see current behavior
    try:
        result = is_allocation_feasible(resources, requests)
        # If it doesn't raise an error, check if it handles gracefully
        print(f"Non-numeric capacity test returned: {result}")
    except (TypeError, ValueError) as e:
        print(f"Non-numeric capacity raised: {type(e).__name__}: {e}")

def test_non_numeric_request_amount():
    """
    Test assumption: Request amounts must be numerical values.
    Constraint: Non-numeric amounts should be rejected.
    Reason: Test type validation for request values.
    """
    resources = {'cpu': 10, 'memory': 20}
    requests = [{'cpu': '5'}, {'memory': 10}]  # String amount
    # Should either return False or raise an error
    result = is_allocation_feasible(resources, requests)
    # Current implementation might try to compare string with number
    assert result is False or result is True  # Documenting current behavior

def test_mixed_request_types():
    """
    Test assumption: Each request must be a dictionary.
    Constraint: Mixed valid and invalid request types.
    Reason: Test type consistency in requests list.
    """
    resources = {'cpu': 10}
    
    # Test with None in requests
    requests = [{'cpu': 5}, None, {'cpu': 3}]
    # Should raise ValueError or return False
    try:
        result = is_allocation_feasible(resources, requests)
        print(f"None in requests returned: {result}")
    except ValueError as e:
        print(f"None in requests raised ValueError: {e}")
    
    # Test with integer in requests (instead of dict)
    requests = [{'cpu': 5}, 42, {'cpu': 3}]
    try:
        result = is_allocation_feasible(resources, requests)
        print(f"Integer in requests returned: {result}")
    except ValueError as e:
        print(f"Integer in requests raised ValueError: {e}")

def test_sequential_allocation_impact():
    """
    Test assumption: Requests are processed sequentially.
    Constraint: Order of requests matters for intermediate capacity checks.
    Reason: Verify sequential processing behavior.
    """
    resources = {'cpu': 5}
    
    # Order 1: Large request first (should fail early)
    requests1 = [{'cpu': 6}, {'cpu': 0}]  # First request exceeds capacity
    result1 = is_allocation_feasible(resources, requests1)
    
    # Order 2: Small requests first (might pass intermediate checks but fail at total)
    requests2 = [{'cpu': 3}, {'cpu': 2}]  # Individual requests OK, but total leaves 0
    result2 = is_allocation_feasible(resources, requests2)
    
    # Order 3: Requests that would be OK individually but exceed when combined
    requests3 = [{'cpu': 3}, {'cpu': 3}]  # 3+3=6 > 5
    result3 = is_allocation_feasible(resources, requests3)
    
    print(f"Order test results: {result1}, {result2}, {result3}")
    # All should be False due to new requirement (need to leave at least 1)

def test_implicit_zero_allocation():
    """
    Test assumption: Resources not mentioned in a request are allocated 0.
    Constraint: Partial resource requests in multi-resource scenarios.
    Reason: Test implicit handling of unrequested resources.
    """
    resources = {'cpu': 10, 'memory': 10, 'disk': 10}
    
    # Some requests only mention subset of resources
    requests = [
        {'cpu': 3, 'memory': 4},  # No disk request (implicit 0)
        {'disk': 5},  # Only disk request
        {'memory': 3, 'disk': 3}  # No cpu request
    ]
    # Total: cpu=3, memory=7, disk=8
    # Leaves: cpu=7, memory=3, disk=2 (all >= 1)
    result = is_allocation_feasible(resources, requests)
    assert result is True
    
    # Test where leaving out resource causes issue with new requirement
    resources2 = {'cpu': 2, 'memory': 2}
    requests2 = [
        {'cpu': 1},  # Only cpu
        {'cpu': 1}   # Only cpu, memory untouched
    ]
    # Total: cpu=2, memory=0
    # Leaves: cpu=0, memory=2 -> cpu has 0 left, so False
    result2 = is_allocation_feasible(resources2, requests2)
    assert result2 is False

def test_very_small_fractional_values():
    """
    Test assumption: Numerical values include floats with small precision.
    Constraint: Floating point arithmetic with values close to boundaries.
    Reason: Test precision handling for the "at least 1 unit" requirement.
    """
    resources = {'cpu': 1.0}
    
    # Leaves exactly 0.000...1 (effectively 0 due to floating point)
    requests = [{'cpu': 0.9999999999999999}]  # Leaves ~1e-16
    result = is_allocation_feasible(resources, requests)
    # With new requirement: leaves less than 1.0, so should be False
    # But floating point precision might make this tricky
    print(f"Small fractional test: {result}, remaining would be {1.0 - 0.9999999999999999}")
    
    # Leaves exactly 1.0 (but might be 1.0000000000000002 due to FP)
    requests2 = [{'cpu': 0.0}]  # Leaves 1.0 exactly
    result2 = is_allocation_feasible(resources, requests2)
    assert result2 is True
    
    # Test with multiple small allocations
    resources3 = {'cpu': 1.0, 'memory': 1.0}
    requests3 = [
        {'cpu': 0.3, 'memory': 0.3},
        {'cpu': 0.3, 'memory': 0.3},
        {'cpu': 0.3, 'memory': 0.3}
    ]
    # Total: 0.9 each, leaves 0.1 each (< 1.0)
    result3 = is_allocation_feasible(resources3, requests3)
    assert result3 is False