# CC_VALIDATE_ELIGIBILITY_V0

## Header (Mandatory)

- **Artifact Code:** CC_VALIDATE_ELIGIBILITY_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_CHECK_TRAINING_STATUS_V0, CT_PURE_CHECK_QUOTA_AVAILABLE_V0

---

## 1. Intent

Validate employee eligibility for AI license provisioning.

---

## 2. Rationale

Eligibility validation is a protocol gate:
- Checks training completion status
- Checks license cap availability
- Both must pass for provisioning to proceed

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_CHECK_TRAINING_STATUS_V0 | CT | Check training |
| 2 | CT_PURE_CHECK_QUOTA_AVAILABLE_V0 | CT | Check quota |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| employee_id | string | true | Employee to validate |
| training_completed | boolean | true | Training status from employee record |
| assigned_count | integer | true | Current assigned license count |
| cap | integer | true | Maximum license cap |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | Validation result |
| reason_code | string | Failure reason if not eligible |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Both training and cap checks pass |
| VIOLATION | Training incomplete or cap reached |

---

## Machine

```yaml
cc_code: CC_VALIDATE_ELIGIBILITY_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Validate employee eligibility for license provisioning

  inputs:
    employee_id:
      type: string
      required: true
    training_completed:
      type: boolean
      required: true
    assigned_count:
      type: integer
      required: true
    cap:
      type: integer
      required: true

  outputs:
    result_status:
      type: string
    reason_code:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]
    on_input_failure: VIOLATION

  pipeline:
    - step: check_training_status
      transform: capability_transforms::CT_PURE_CHECK_TRAINING_STATUS_V0
      inputs:
        training_completed: $.inputs.training_completed
      outputs:
        is_eligible: $.training_eligible
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: check_quota_available
      transform: capability_transforms::CT_PURE_CHECK_QUOTA_AVAILABLE_V0
      inputs:
        assigned_count: $.inputs.assigned_count
        quota: $.inputs.cap
      outputs:
        quota_available: $.quota_available
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit

extensions:
  description: Validates training completion and license cap availability
```
