# IN_RECLAIM_LICENSE_V0

## Header (Mandatory)

- **Artifact Code:** IN_RECLAIM_LICENSE_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_AUTO_RECLAIM_V0

---

## 1. Intent

Request to evaluate and potentially reclaim an inactive license.

---

## 2. Rationale

Reclamation intent enables autonomous license management:
- Evaluates inactivity against threshold
- Reclaims if inactive, retains if active
- No human intervention required

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_AUTO_RECLAIM_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| license_id | string | true | License to evaluate |
| threshold_days | integer | false | Inactivity threshold (default: 30) |
| context | object | false | Runtime context data (employee_id, last_active_date, days_inactive) |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Reclamation request accepted for processing |
| NACK | Reclamation request rejected |

---

## 6. Domain

- **Domain:** pgs.ai_licensing

---

## Machine

```yaml
in_code: IN_RECLAIM_LICENSE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Request license reclamation evaluation
  workflow: WF_AUTO_RECLAIM_V0

  inputs:
    license_id:
      type: string
      required: true
      description: License to evaluate
    threshold_days:
      type: integer
      default: 30
      description: Inactivity threshold in days
    context:
      type: object
      required: false
      description: Runtime context data (employee_id, last_active_date, days_inactive)

  outcomes:
    ACK:
      description: Reclamation request accepted for processing
    NACK:
      description: Reclamation request rejected

extensions:
  domain: pgs.testbed
```
