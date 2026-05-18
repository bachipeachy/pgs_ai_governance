# EV_LICENSE_CAP_SET_V0

## Header (Mandatory)

- **Artifact Code:** EV_LICENSE_CAP_SET_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A license cap has been established for the system.

---

## 2. Rationale

License cap is a hard constraint:
- Injected from Finance/procurement
- Enforces maximum concurrent licenses
- Oversubscription impossible by construction

---

## 3. Emitted By

| Source | Description |
|--------|-------------|
| Fact Injection | Finance system declares license cap |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| cap_count | integer | true | Maximum number of concurrent licenses |
| effective_date | string (date-time) | true | When cap becomes effective |

---

## Machine

```yaml
ev_code: EV_LICENSE_CAP_SET_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: License Cap Set
  description: Emitted when a license cap is established

  schema:
    cap_count:
      type: integer
      required: true
    effective_date:
      type: string
      format: date-time
      required: true
```
