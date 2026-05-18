# EV_LICENSE_REVOKED_V0

## Header (Mandatory)

- **Artifact Code:** EV_LICENSE_REVOKED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A license has been revoked and returned to the pool.

---

## 2. Rationale

License revocation is autonomous reclamation:
- Triggered by inactivity threshold
- No human intervention required
- Returns license for pending employees

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_AUTO_RECLAIM_V0 | CC_RECLAIM_UNUSED_LICENSE_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| license_id | string | true | License that was revoked |
| reason | string | true | Revocation reason: INACTIVITY |
| timestamp | string (date-time) | true | When revocation occurred |

---

## Machine

```yaml
ev_code: EV_LICENSE_REVOKED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: License Revoked
  description: Emitted when a license is revoked and returned to pool

  schema:
    license_id:
      type: string
      required: true
    reason:
      type: string
      enum:
        - INACTIVITY
      required: true
    timestamp:
      type: string
      format: date-time
      required: true
```
