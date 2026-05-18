# EV_USAGE_RECORDED_V0

## Header (Mandatory)

- **Artifact Code:** EV_USAGE_RECORDED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

License usage activity has been recorded.

---

## 2. Rationale

Usage tracking enables autonomous reclamation:
- Injected from telemetry system
- Tracks last active date per license
- Triggers reclamation when inactivity threshold exceeded

---

## 3. Emitted By

| Source | Description |
|--------|-------------|
| Fact Injection | Telemetry system declares usage activity |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| license_id | string | true | License being tracked |
| last_active_date | string (date-time) | true | When license was last used |

---

## Machine

```yaml
ev_code: EV_USAGE_RECORDED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Usage Recorded
  description: Emitted when license usage activity is recorded

  schema:
    license_id:
      type: string
      required: true
    last_active_date:
      type: string
      format: date-time
      required: true
```
