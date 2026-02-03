## Student Name:Joshua Keppo
## Student ID: 210971752

"""
Stub file for the is allocation feasible exercise.

Implement the function `is_allocation_feasible` to  Determine whether a set of resource requests can be satisfied 
given limited capacities. Take int account any possible constraints. See the lab handout
for full requirements.
"""
    
from typing import Dict, List, Union

Number = Union[int, float]


def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    # Validate that all requests are dictionaries
    for i, request in enumerate(requests):
        if not isinstance(request, dict):
            raise ValueError(f"Request at index {i} is not a dictionary")
    
    # Check that all resource capacities are non-negative
    for resource, capacity in resources.items():
        if capacity < 0:
            return False
    
    # Initialize usage tracker
    total_used = {resource: 0 for resource in resources}
    
    # Process each request
    for request in requests:
        for resource, amount in request.items():
            # Check if the resource exists
            if resource not in resources:
                return False
            
            # Check if amount is valid (non-negative, including -0.0)
            if amount < 0 or (amount == 0 and str(amount).startswith('-')):
                return False
            
            # Update total and check capacity
            total_used[resource] += amount
            if total_used[resource] > resources[resource]:
                return False
    
    return True