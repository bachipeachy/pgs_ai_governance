# CC_BIND_LICENSE_TO_TOOL_SURFACE_V0

## Header (Mandatory)

- **Artifact Code:** CC_BIND_LICENSE_TO_TOOL_SURFACE_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_LOOKUP_V0, CT_PURE_VALIDATE_SET_MEMBERSHIP_V0

---

## 1. Intent

Map the user's license tier to an allowed tool set and verify the requested tool is authorized.

---

## 2. Rationale

License-to-tool binding is the fourth governance gate:
- Declarative tier-to-tool mapping defines the authority surface
- Each license tier grants access to a specific, closed set of tools
- Enforces Invariant I-A3 (License-Bound Authority)

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_LOOKUP_V0 | CT | LOOKUP |
| 2 | CT_PURE_VALIDATE_SET_MEMBERSHIP_V0 | CT | VALIDATE_SET_MEMBERSHIP |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tool_name | string | true | Requested tool identifier |
| license_tier | string | true | Resolved license tier |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| allowed_tools | array | Tools authorized for this tier |
| is_authorized | boolean | Whether requested tool is authorized |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Tool is authorized for license tier |
| VIOLATION | Tool is not authorized for license tier |

---

## Machine

```yaml
cc_code: CC_BIND_LICENSE_TO_TOOL_SURFACE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Map license tier to allowed tool set and verify tool authorization

  inputs:
    tool_name:
      type: string
      required: true
    license_tier:
      type: string
      required: true

  outputs:
    allowed_tools:
      type: array
    is_authorized:
      type: boolean

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]
    on_input_failure: VIOLATION

  pipeline:
    - step: lookup_tier_tools
      transform: capability_transforms::CT_PURE_LOOKUP_V0
      inputs:
        key: $.inputs.license_tier
        map:
          none:
            - READ_RECORD
          standard:
            - READ_RECORD
            - PROVISION_STANDARD_LICENSE
          enterprise:
            - READ_RECORD
            - PROVISION_STANDARD_LICENSE
            - PROVISION_PREMIUM_LICENSE
      outputs:
        allowed_tools: $.capability_result.result
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: validate_tool_membership
      transform: capability_transforms::CT_PURE_VALIDATE_SET_MEMBERSHIP_V0
      inputs:
        value: $.inputs.tool_name
        allowed_set: $.results.lookup_tier_tools.allowed_tools
      outputs:
        is_authorized: $.capability_result.is_member
        allowed_tools: $.results.lookup_tier_tools.allowed_tools
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

extensions:
  description: Enforces license-bound authority — tier determines tool surface
```
