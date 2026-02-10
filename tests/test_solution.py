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