
from typing import List, Tuple
from typing import List, Tuple, Union

def back_testing(values: List[Union[int, float]], drops: float) -> List[Tuple[int, int, float, float]]:
    """
    Find intervals in a list where values differ by a certain percentage or more using two pointers.
    
    Args:
        values (List[Union[int, float]]): List of numerical values to analyze
        drops (float): The percentage drop to look for (e.g., 0.15 for a 15% drop)
        
    Returns:
        list: List of tuples containing (start_index, end_index, start_value, end_value)
    """
    if not values or len(values) < 2:
        return []
    
    intervals: List[Tuple[int, int, float, float]] = []
    left = 0
    right = 1
    multiplier = 1 - drops
    threshold = values[left] * multiplier
    
    while right < len(values):
        
        if values[right] <= threshold:
            # Found a value that differs by the specified percentage or more
            intervals.append((left, right, float(values[left]), float(values[right])))
            left = right  # Move left pointer to current position
            threshold = values[left] * multiplier # Update threshold
        elif values[right] > values[left]:
            # Update threshold
            left = right
            threshold = values[left] * multiplier
        
        right += 1
    
    return intervals