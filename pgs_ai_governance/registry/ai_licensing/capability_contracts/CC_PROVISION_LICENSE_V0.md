# CC_PROVISION_LICENSE_V0

## Header (Mandatory)

- **Artifact Code:** CC_PROVISION_LICENSE_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_REGISTRY_V0

---

## 1. Intent

Register a license assignment for an employee.

---

## 2. Rationale

License provisioning is a protocol-governed transition:
- Registers employee in license registry
- Generates unique license ID
- Creates immutable assignment record

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_REGISTRY_V0 | CS | REGISTER |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| employee_id | string | true | Employee to provision |
| license_id | string | true | Unique license identifier |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | Operation result |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | License registered successfully |
| ALREADY_EXISTS | Employee already has a license |
| VIOLATION | Invalid input format |
| BACKEND_ERROR | Registry unavailable |

---

## Machine

```yaml
cc_code: CC_PROVISION_LICENSE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Register license assignment for employee

  inputs:
    employee_id:
      type: string
      required: true
    license_id:
      type: string
      required: true

  outputs:
    result_status:
      type: string

  result_status_contract:
    allowed: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: register_license
      side_effect: capability_side_effects::CS_REGISTRY_V0
      op: REGISTER
      inputs:
        key: $.inputs.employee_id
        target_cs: CS_REGISTRY_V0
        target_ref: $.inputs.license_id
      outputs:
        result_status: $.result_status
      result_surface: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        ALREADY_EXISTS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  description: Registers employee license assignment in registry
```
