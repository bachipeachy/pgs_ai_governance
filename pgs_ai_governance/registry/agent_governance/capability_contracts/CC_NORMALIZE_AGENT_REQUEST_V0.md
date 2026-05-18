# CC_NORMALIZE_AGENT_REQUEST_V0

## Header (Mandatory)

- **Artifact Code:** CC_NORMALIZE_AGENT_REQUEST_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_GENERATE_ID_V0

---

## 1. Intent

Validate request schema and generate a deterministic intent hash.

---

## 2. Rationale

Normalization is the first governance gate:
- Generates a deterministic identifier from request content
- Ensures all downstream processing operates on a canonical representation
- Intent hash enables replay detection and audit correlation

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_GENERATE_ID_V0 | CT | GENERATE_ID |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tool_name | string | true | Requested tool identifier |
| requesting_user_id | string | true | User the agent acts on behalf of |
| domain_context | string | true | Domain context for the request |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| intent_hash | string | Deterministic hash of normalized intent |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Intent hash generated |
| VIOLATION | Invalid input |

---

## Machine

```yaml
cc_code: CC_NORMALIZE_AGENT_REQUEST_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Validate request schema and generate deterministic intent hash

  inputs:
    tool_name:
      type: string
      required: true
    requesting_user_id:
      type: string
      required: true
    domain_context:
      type: string
      required: true

  outputs:
    intent_hash:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]
    on_input_failure: VIOLATION

  pipeline:
    - step: generate_intent_hash
      transform: capability_transforms::CT_PURE_GENERATE_ID_V0
      inputs:
        prefix: "AREQ"
        data:
          tool_name: $.inputs.tool_name
          requesting_user_id: $.inputs.requesting_user_id
          domain_context: $.inputs.domain_context
      outputs:
        intent_hash: $.capability_result.id
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

extensions:
  description: Normalizes agent request and generates deterministic intent hash
```
