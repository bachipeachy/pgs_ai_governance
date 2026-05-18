# EV_LICENSE_PROVISIONED_V0

## Header (Mandatory)

- **Artifact Code:** EV_LICENSE_PROVISIONED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A license has been successfully provisioned to an employee.

---

## 2. Rationale

License provisioning is a protocol-governed transition:
- Only occurs when all prerequisites satisfied
- Records assignment for audit trail
- Increments assigned count toward cap

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_PROVISION_AI_LICENSING_V0 | CC_PROVISION_LICENSE_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| employee_id | string | true | Employee who received license |
| license_id | string | true | Unique license identifier |
| timestamp | string (date-time) | true | When provisioning occurred |

---

## Machine

```yaml
ev_code: EV_LICENSE_PROVISIONED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: License Provisioned
  description: Emitted when a license is successfully provisioned

  schema:
    employee_id:
      type: string
      required: true
    license_id:
      type: string
      required: true
    timestamp:
      type: string
      format: date-time
      required: true
```
