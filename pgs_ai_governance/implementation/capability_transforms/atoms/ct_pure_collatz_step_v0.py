"""
CT_PURE_COLLATZ_STEP_V0

Pure Capability Transform (Atom)

Purpose:
    Compute the full Collatz sequence for each number in the input list.

Implementation:
    - Pure iteration: n → n/2 (even), 3n+1 (odd), until reaching 1
    - Entire sequence is captured per number
    - No side effects, no external state

Purity Class: ct_pure
"""

from typing import Dict, Any, List

from pgs_runtime.ct_executor import CTExecutionError


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Execute CT_PURE_COLLATZ_STEP_V0.

    Inputs:
        numbers (list[int]): List of positive integers for which to compute sequences

    Outputs:
        sequences (dict): Mapping from str(n) → list of integers (full Collatz sequence)
    """
    if "numbers" not in inputs:
        raise CTExecutionError(
            "CT_PURE_COLLATZ_STEP_V0: missing required input 'numbers'"
        )

    numbers = inputs["numbers"]

    if not isinstance(numbers, list):
        raise CTExecutionError(
            f"CT_PURE_COLLATZ_STEP_V0: 'numbers' must be a list, got {type(numbers).__name__}"
        )

    sequences: Dict[str, List[int]] = {}

    for n in numbers:
        if not isinstance(n, int) or isinstance(n, bool):
            raise CTExecutionError(
                f"CT_PURE_COLLATZ_STEP_V0: each number must be a positive integer, got {type(n).__name__}"
            )
        if n < 1:
            raise CTExecutionError(
                f"CT_PURE_COLLATZ_STEP_V0: each number must be >= 1, got {n}"
            )

        seq: List[int] = [n]
        current = n
        while current != 1:
            if current % 2 == 0:
                current = current // 2
            else:
                current = 3 * current + 1
            seq.append(current)

        sequences[str(n)] = seq

    return {"sequences": sequences}
