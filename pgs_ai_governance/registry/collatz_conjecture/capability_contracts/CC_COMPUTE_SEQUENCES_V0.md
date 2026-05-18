# CC_COMPUTE_SEQUENCES_V0

## Header (Mandatory)

- **Artifact Code:** CC_COMPUTE_SEQUENCES_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_COLLATZ_STEP_V0

---

## 1. Intent

Compute Collatz sequences for all numbers in the input list.

---

## 2. Rationale

Sequence computation is the first analytical step:
- Applies the Collatz rule iteratively to each input number
- Captures the complete path from n to 1
- Output feeds the termination verification step

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_COLLATZ_STEP_V0 | CT | COLLATZ_STEP |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| numbers | array | true | List of positive integers from the admission-validated payload |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| sequences | object | Mapping from str(n) to full Collatz sequence |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | All sequences computed successfully |
| VIOLATION | Input invalid (non-positive, non-integer, or transform error) |

---

## Machine

```yaml
cc_code: CC_COMPUTE_SEQUENCES_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Compute Collatz sequences for all input numbers

  inputs:
    numbers:
      type: array
      required: true

  outputs:
    sequences:
      type: object

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]
    on_input_failure: VIOLATION

  pipeline:
    - step: compute_sequences
      transform: ai_governance::CT_PURE_COLLATZ_STEP_V0
      inputs:
        numbers: $.inputs.numbers
      outputs:
        sequences: $.capability_result.sequences
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit

extensions:
  description: Computes full Collatz iteration path for each input integer
```
