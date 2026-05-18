# CC_CHECK_TOOL_DECLARED_V0

## Header (Mandatory)

- **Artifact Code:** CC_CHECK_TOOL_DECLARED_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_VALIDATE_SET_MEMBERSHIP_V0

---

## 1. Intent

Verify that the requested tool exists in the closed tool registry.

---

## 2. Rationale

Tool declaration is the second governance gate:
- Only declared tools may be referenced
- The tool surface is closed — undeclared tools are structurally absent
- This enforces Invariant I-A2 (Closed Tool Surface)

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_VALIDATE_SET_MEMBERSHIP_V0 | CT | VALIDATE_SET_MEMBERSHIP |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tool_name | string | true | Requested tool identifier |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| is_declared | boolean | Whether tool is in the closed registry |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Tool is declared |
| VIOLATION | Tool is not declared |

---

## Machine

```yaml
cc_code: CC_CHECK_TOOL_DECLARED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Verify requested tool exists in closed tool registry

  inputs:
    tool_name:
      type: string
      required: true

  outputs:
    is_declared:
      type: boolean

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]
    on_input_failure: VIOLATION

  pipeline:
    - step: check_tool_declared
      transform: capability_transforms::CT_PURE_VALIDATE_SET_MEMBERSHIP_V0
      inputs:
        value: $.inputs.tool_name
        allowed_set:
          - READ_RECORD
          - PROVISION_STANDARD_LICENSE
          - PROVISION_PREMIUM_LICENSE
      outputs:
        is_declared: $.capability_result.is_member
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

extensions:
  description: Enforces closed tool surface — only declared tools may be referenced
```
