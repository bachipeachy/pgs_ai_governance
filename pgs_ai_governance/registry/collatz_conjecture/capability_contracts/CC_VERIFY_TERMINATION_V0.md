# CC_VERIFY_TERMINATION_V0

## Header (Mandatory)

- **Artifact Code:** CC_VERIFY_TERMINATION_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_TERMINATION_CHECK_V0

---

## 1. Intent

Verify that every computed Collatz sequence terminates at 1.

---

## 2. Rationale

Termination verification is the conjecture gate:
- Checks the final element of each sequence
- Returns SUCCESS if all sequences end at 1 (conjecture holds)
- Returns VIOLATION if any sequence does not end at 1 (conjecture violated)

A VIOLATION here is a first-class protocol outcome, not an error.
It means the conjecture was tested and failed — a historic event.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_TERMINATION_CHECK_V0 | CT | TERMINATION_CHECK |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| sequences | object | true | Mapping from str(n) to Collatz sequence list |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| all_terminate | boolean | True if all sequences end at 1 |
| non_terminating | array | Seeds that did not terminate |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Conjecture holds — all sequences terminated at 1 |
| VIOLATION | Conjecture violated — at least one sequence did not reach 1 |

---

## Machine

```yaml
cc_code: CC_VERIFY_TERMINATION_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Verify all Collatz sequences terminate at 1

  inputs:
    sequences:
      type: object
      required: true

  outputs:
    all_terminate:
      type: boolean
    non_terminating:
      type: array

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]
    on_input_failure: VIOLATION

  pipeline:
    - step: check_termination
      transform: ai_governance::CT_PURE_TERMINATION_CHECK_V0
      inputs:
        sequences: $.inputs.sequences
      outputs:
        all_terminate: $.capability_result.all_terminate
        non_terminating: $.capability_result.non_terminating
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: evaluate_conjecture
        VIOLATION: exit

  evaluation:
    evaluate_conjecture:
      condition: $.capability_result.all_terminate == true
      on_true: SUCCESS
      on_false: VIOLATION

extensions:
  description: Protocol gate for Collatz Conjecture — SUCCESS means conjecture holds for this input set
```
