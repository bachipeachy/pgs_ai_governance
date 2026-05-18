# CC_STORE_RESULTS_V0

## Header (Mandatory)

- **Artifact Code:** CC_STORE_RESULTS_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0

---

## 1. Intent

Persist Collatz computation results to mutable JSON storage.

---

## 2. Rationale

Result persistence is the final protocol step:
- Stores sequences and conjecture verdict under a declared key
- Uses last-write-wins semantics (results are overwritten on re-run)
- Idempotent: re-running with same input produces same stored state

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | WRITE |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| sequences | object | true | Computed Collatz sequences |
| all_terminate | boolean | true | Conjecture verdict |
| non_terminating | array | false | Seeds that did not terminate |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | Storage operation result |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Results stored successfully |
| VIOLATION | Invalid input or storage constraint violated |
| BACKEND_ERROR | Storage unavailable |

---

## Machine

```yaml
cc_code: CC_STORE_RESULTS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Store Collatz results to mutable JSON storage

  inputs:
    sequences:
      type: object
      required: true
    all_terminate:
      type: boolean
      required: true
    non_terminating:
      type: array

  outputs:
    result_status:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: store_results
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      op: WRITE
      store: COLLATZ_RESULTS
      inputs:
        key: "collatz_results"
        value:
          sequences: $.inputs.sequences
          all_terminate: $.inputs.all_terminate
          non_terminating: $.inputs.non_terminating
          timestamp: "{{timestamp}}"
      outputs:
        result_status: $.result_status
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  description: Persists conjecture results with last-write-wins semantics
```
