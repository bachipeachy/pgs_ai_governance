# EV_TRAINING_COMPLETED_V0

## Header (Mandatory)

- **Artifact Code:** EV_TRAINING_COMPLETED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

An employee has completed required training.

---

## 2. Rationale

Training completion is a protocol gate:
- Injected from LMS system
- Enables previously blocked provisioning
- Protocol responds automatically (self-healing)

---

## 3. Emitted By

| Source | Description |
|--------|-------------|
| Fact Injection | LMS system declares training completion |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| employee_id | string | true | Employee who completed training |
| completion_date | string (date-time) | true | When training was completed |

---

## Machine

```yaml
ev_code: EV_TRAINING_COMPLETED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Training Completed
  description: Emitted when an employee completes required training

  schema:
    employee_id:
      type: string
      required: true
    completion_date:
      type: string
      format: date-time
      required: true
```
