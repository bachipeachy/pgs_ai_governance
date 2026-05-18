"""
CT_TERMINATION_CHECK_V0

Pure Capability Transform (Atom)

Purpose:
    Verify that every Collatz sequence in the input terminates at 1.

Implementation:
    - Inspects last element of each sequence
    - Collects any sequences that do not end at 1
    - Returns all_terminate flag and list of non-terminating seeds

Purity Class: ct_pure
"""

from typing import Dict, Any, List

from omnibachi.implementation.execution.machine.transforms.ct_executor import CTExecutionError


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Execute CT_TERMINATION_CHECK_V0.

    Inputs:
        sequences (dict): Mapping from str(n) → list of integers (Collatz sequences)

    Outputs:
        all_terminate (bool): True if every sequence ends at 1
        non_terminating (list): Seeds whose sequences did not end at 1
    """
    if "sequences" not in inputs:
        raise CTExecutionError(
            "CT_TERMINATION_CHECK_V0: missing required input 'sequences'"
        )

    sequences = inputs["sequences"]

    if not isinstance(sequences, dict):
        raise CTExecutionError(
            f"CT_TERMINATION_CHECK_V0: 'sequences' must be a dict, got {type(sequences).__name__}"
        )

    non_terminating: List[str] = []

    for seed, seq in sequences.items():
        if not isinstance(seq, list) or len(seq) == 0:
            non_terminating.append(seed)
            continue
        if seq[-1] != 1:
            non_terminating.append(seed)

    all_terminate = len(non_terminating) == 0

    return {
        "all_terminate": all_terminate,
        "non_terminating": non_terminating,
    }
