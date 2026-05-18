# CC_ENFORCE_LICENSE_CAP_V0

## Header (Mandatory)

- **Artifact Code:** CC_ENFORCE_LICENSE_CAP_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_REGISTRY_V0

---

## 1. Intent

Enforce hard license cap before provisioning.

---

## 2. Rationale

Cap enforcement is a hard limit:
- Counts current assignments in registry
- Compares against declared cap
- Oversubscription impossible by construction

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_REGISTRY_V0 | CS | COUNT |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| cap | integer | true | Maximum license cap |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | Operation result |
| assigned_count | integer | Current assignment count |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Cap not reached, provisioning may proceed |
| CAP_REACHED | No capacity available |
| BACKEND_ERROR | Registry unavailable |

---

## Machine

```yaml
cc_code: CC_ENFORCE_LICENSE_CAP_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Enforce hard license cap before provisioning

  inputs:
    cap:
      type: integer
      required: true

  outputs:
    result_status:
      type: string
    assigned_count:
      type: integer

  result_status_contract:
    allowed: [SUCCESS, CAP_REACHED, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: count_licenses
      side_effect: capability_side_effects::CS_REGISTRY_V0
      op: COUNT
      inputs: {}
      outputs:
        count: $.assigned_count
      result_surface: [SUCCESS, BACKEND_ERROR]
      on_result:
        SUCCESS: evaluate_cap
        BACKEND_ERROR: exit

  evaluation:
    evaluate_cap:
      condition: $.assigned_count < $.inputs.cap
      on_true: SUCCESS
      on_false: CAP_REACHED

extensions:
  description: Counts registry entries and enforces cap limit
```
