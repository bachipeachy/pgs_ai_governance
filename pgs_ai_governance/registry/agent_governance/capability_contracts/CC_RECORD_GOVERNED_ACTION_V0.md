# CC_RECORD_GOVERNED_ACTION_V0

## Header (Mandatory)

- **Artifact Code:** CC_RECORD_GOVERNED_ACTION_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_GENERATE_ID_V0, CS_REGISTRY_V0, CS_APPENDONLY_JSONL_V0

---

## 1. Intent

Record an authorized governance decision and emit an audit trail.

---

## 2. Rationale

Authorization recording completes the governance pipeline:
- Generates a unique governance action identifier
- Registers the action in the governance actions registry
- Appends an audit record for compliance and provability
- Enforces Invariant I-A6 (Deterministic Trace)

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_GENERATE_ID_V0 | CT | GENERATE_ID |
| 2 | CS_REGISTRY_V0 | CS | REGISTER |
| 3 | CS_APPENDONLY_JSONL_V0 | CS | APPEND |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tool_name | string | true | Authorized tool |
| parameters | object | true | Tool parameters |
| requesting_user_id | string | true | User the agent acts for |
| license_tier | string | true | License tier that authorized the action |
| domain_context | string | true | Domain context |
| intent_hash | string | true | Deterministic intent hash |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| action_id | string | Generated governance action identifier |
| result_status | string | Operation result |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Action recorded and audited |
| VIOLATION | Invalid input |
| BACKEND_ERROR | Storage unavailable |

---

## Machine

```yaml
cc_code: CC_RECORD_GOVERNED_ACTION_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Record authorized governance decision and emit audit trail

  inputs:
    tool_name:
      type: string
      required: true
    parameters:
      type: object
      required: true
    requesting_user_id:
      type: string
      required: true
    license_tier:
      type: string
      required: true
    domain_context:
      type: string
      required: true
    intent_hash:
      type: string
      required: true

  outputs:
    action_id:
      type: string
    result_status:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: generate_action_id
      transform: capability_transforms::CT_PURE_GENERATE_ID_V0
      inputs:
        prefix: "AGOV"
        data:
          tool_name: $.inputs.tool_name
          requesting_user_id: $.inputs.requesting_user_id
          intent_hash: $.inputs.intent_hash
      outputs:
        action_id: $.capability_result.id
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: register_action
      side_effect: capability_side_effects::CS_REGISTRY_V0
      op: REGISTER
      inputs:
        key: $.results.generate_action_id.action_id
        target_ref: $.inputs.tool_name
        metadata:
          requesting_user_id: $.inputs.requesting_user_id
          license_tier: $.inputs.license_tier
          parameters: $.inputs.parameters
          domain_context: $.inputs.domain_context
          intent_hash: $.inputs.intent_hash
          decision: "AUTHORIZED"
      outputs:
        result_status: $.capability_result.result_status
      result_surface: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: continue
        ALREADY_EXISTS: continue
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: append_audit_record
      side_effect: capability_side_effects::CS_APPENDONLY_JSONL_V0
      op: APPEND
      inputs:
        record:
          event_code: "EV_AGENT_ACTION_AUTHORIZED_V0"
          action_id: $.results.generate_action_id.action_id
          tool_name: $.inputs.tool_name
          requesting_user_id: $.inputs.requesting_user_id
          license_tier: $.inputs.license_tier
          parameters: $.inputs.parameters
          decision: "AUTHORIZED"
          timestamp: "{{timestamp}}"
      outputs:
        result_status: $.capability_result.result_status
        action_id: $.results.generate_action_id.action_id
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: continue
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  description: Records authorized governance decision with symmetric audit
```
