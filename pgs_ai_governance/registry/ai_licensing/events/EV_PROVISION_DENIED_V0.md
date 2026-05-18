# EV_PROVISION_DENIED_V0

## Header (Mandatory)

- **Artifact Code:** EV_PROVISION_DENIED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A license provisioning request has been denied.

---

## 2. Rationale

Denial is a first-class terminal outcome:
- Not an error, but a recorded system fact
- Provides audit trail for compliance
- Proves "nothing happened" is provable

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_PROVISION_AI_LICENSING_V0 | CC_APPEND_AUDIT_EVENT_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| employee_id | string | true | Employee whose provision was denied |
| reason_code | string | true | Denial reason: TRAINING_INCOMPLETE, CAP_REACHED |
| timestamp | string (date-time) | true | When denial occurred |

---

## Machine

```yaml
ev_code: EV_PROVISION_DENIED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Provision Denied
  description: Emitted when license provisioning is denied (first-class terminal outcome)

  schema:
    employee_id:
      type: string
      required: true
    reason_code:
      type: string
      enum:
        - TRAINING_INCOMPLETE
        - CAP_REACHED
      required: true
    timestamp:
      type: string
      format: date-time
      required: true
```
