# WF_DEMO_COLLATZ_CONJECTURE_V0

## Header (Mandatory)

- **Artifact Code:** WF_DEMO_COLLATZ_CONJECTURE_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** IN_COLLATZ_INPUT_VALIDATED_V0, IN_CONJECTURE_HELD_V0, CC_COMPUTE_SEQUENCES_V0, CC_VERIFY_TERMINATION_V0, CC_STORE_RESULTS_V0

---

## 1. Intent

Demonstrate that PGS executes a mathematically-grounded protocol workflow
with no domain knowledge in the runtime.

The Collatz Conjecture states: every positive integer eventually reaches 1
under the rule n → n/2 (even) or n → 3n+1 (odd).

This workflow:
1. Validates the input set (admission gate)
2. Computes the complete sequence for each number
3. Verifies that every sequence terminates at 1
4. Stores the results

The runtime is domain-blind. It traverses this graph identically to any other
PGS workflow. The only thing that changed is the protocol artifact.

---

## 2. Rationale

This workflow proves execution is semantic-agnostic:
- The runtime does not know what "Collatz" means
- The conjecture is a protocol invariant, not application logic
- VIOLATION is a first-class terminal state (conjecture failed — not a bug)
- The trace is a verifiable proof of what was computed

---

## 3. Execution Graph

```
IN_COLLATZ_INPUT_VALIDATED_V0
    ├─ ACK  → CC_COMPUTE_SEQUENCES_V0
    │            ├─ SUCCESS   → CC_VERIFY_TERMINATION_V0
    │            │                ├─ SUCCESS   → CC_STORE_RESULTS_V0
    │            │                │                ├─ SUCCESS      → EXIT:CONJECTURE_PROVEN
    │            │                │                ├─ VIOLATION    → EXIT:ERROR
    │            │                │                └─ BACKEND_ERROR → EXIT:ERROR
    │            │                └─ VIOLATION → EXIT:CONJECTURE_VIOLATED
    │            └─ VIOLATION → EXIT:ERROR
    └─ NACK → EXIT:REJECTED
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_COLLATZ_INPUT_VALIDATED_V0 | IN | Admission gate — validates list of positive integers < 100 |
| CC_COMPUTE_SEQUENCES_V0 | CC | Compute full Collatz sequence for each input number |
| CC_VERIFY_TERMINATION_V0 | CC | Verify all sequences terminate at 1 |
| CC_STORE_RESULTS_V0 | CC | Persist results to mutable JSON storage |
| EXIT | EXIT | Terminal nodes |

---

## 5. Admission

Input must be a non-empty list of positive integers, each in [1, 99].
The conjecture is well-studied for all n < 2^68; the bound of 99 keeps
sequences tractable for demonstration purposes.

---

## Machine

```yaml
wf_code: WF_DEMO_COLLATZ_CONJECTURE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0

runtime_binding: ai_governance::RB_COLLATZ_V0
structure: fb.topology::STRUCTURE_RUNTIME_EXECUTION_V0

core:
  summary: Compute and verify Collatz sequences — demonstrates domain-blind PGS execution

  start_node: IN_COLLATZ_INPUT_VALIDATED_V0

  nodes:
    IN_COLLATZ_INPUT_VALIDATED_V0:
      type: IN
      code: IN_COLLATZ_INPUT_VALIDATED_V0
      next:
        ACK: CC_COMPUTE_SEQUENCES_V0
        NACK: EXIT_REJECTED

    CC_COMPUTE_SEQUENCES_V0:
      type: CC
      code: CC_COMPUTE_SEQUENCES_V0
      inputs:
        numbers: $.payload.numbers
      next:
        SUCCESS: CC_VERIFY_TERMINATION_V0
        VIOLATION: EXIT_ERROR

    CC_VERIFY_TERMINATION_V0:
      type: CC
      code: CC_VERIFY_TERMINATION_V0
      inputs:
        sequences: $.results.CC_COMPUTE_SEQUENCES_V0.sequences
      next:
        SUCCESS: CC_STORE_RESULTS_V0
        VIOLATION: EXIT_CONJECTURE_VIOLATED

    CC_STORE_RESULTS_V0:
      type: CC
      code: CC_STORE_RESULTS_V0
      inputs:
        sequences: $.results.CC_COMPUTE_SEQUENCES_V0.sequences
        all_terminate: $.results.CC_VERIFY_TERMINATION_V0.all_terminate
        non_terminating: $.results.CC_VERIFY_TERMINATION_V0.non_terminating
      next:
        SUCCESS: EXIT_CONJECTURE_PROVEN
        VIOLATION: EXIT_ERROR
        BACKEND_ERROR: EXIT_ERROR

    EXIT_CONJECTURE_PROVEN:
      type: EXIT
      reason: COMPLETED

    EXIT_CONJECTURE_VIOLATED:
      type: EXIT
      reason: COMPLETED

    EXIT_REJECTED:
      type: EXIT
      reason: EXITED

    EXIT_ERROR:
      type: EXIT
      reason: FAILED
```
