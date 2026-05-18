# CC_RESOLVE_LICENSE_TIER_V0

## Header (Mandatory)

- **Artifact Code:** CC_RESOLVE_LICENSE_TIER_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0, CT_PURE_VALIDATE_SET_MEMBERSHIP_V0

---

## 1. Intent

Read license facts for the requesting user and validate that the license is active.

---

## 2. Rationale

License resolution is the third governance gate:
- Retrieves license tier and status from the fact feed
- Validates that the license is active (not inactive or missing)
- Enforces Invariant I-A5 (Domain Isolation) — read-only access to license facts

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | READ |
| 2 | CT_PURE_VALIDATE_SET_MEMBERSHIP_V0 | CT | VALIDATE_SET_MEMBERSHIP |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| requesting_user_id | string | true | User to look up in license facts |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| license_status | string | License status (active, inactive) |
| license_tier | string | License tier (none, standard, enterprise) |
| org_unit | string | Organizational unit |
| is_active | boolean | Whether license is active |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | License found and active |
| NOT_FOUND | No license record for user |
| VIOLATION | License found but inactive |
| BACKEND_ERROR | License facts store unavailable |

---

## Machine

```yaml
cc_code: CC_RESOLVE_LICENSE_TIER_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Read license facts for requesting user and validate license is active

  inputs:
    requesting_user_id:
      type: string
      required: true

  outputs:
    license_status:
      type: string
    license_tier:
      type: string
    org_unit:
      type: string
    is_active:
      type: boolean

  result_status_contract:
    allowed: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: read_license_record
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      op: READ
      store: LICENSE_FACTS
      inputs:
        key: $.inputs.requesting_user_id
      outputs:
        license_status: $.capability_result.value.license_status
        license_tier: $.capability_result.value.license_tier
        org_unit: $.capability_result.value.org_unit
      result_surface: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: continue
        NOT_FOUND: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: validate_active_status
      transform: capability_transforms::CT_PURE_VALIDATE_SET_MEMBERSHIP_V0
      inputs:
        value: $.results.read_license_record.license_status
        allowed_set:
          - active
      outputs:
        is_active: $.capability_result.is_member
        license_status: $.results.read_license_record.license_status
        license_tier: $.results.read_license_record.license_tier
        org_unit: $.results.read_license_record.org_unit
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

extensions:
  description: Resolves license tier and validates active status from immutable fact feed
```
