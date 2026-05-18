# IN_DENY_PROVISION_V0

## Header (Mandatory)

- **Artifact Code:** IN_DENY_PROVISION_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_DENY_PROVISION_V0

---

## 1. Intent

Handle provisioning denial by emitting denial event and recording to audit log.

---

## 2. Rationale

Denial handling intent provides first-class terminal outcome:
- Declares desired outcome (clean denial with audit)
- Protocol emits denial event
- Outcome is deterministic (DENIED or ERROR)

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_DENY_PROVISION_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| employee_id | string | true | Employee whose provision was denied |
| reason_code | string | true | Reason for denial |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Denial request accepted for processing |
| NACK | Denial request rejected |

---

## 6. Domain

- **Domain:** pgs.ai_licensing

---

## Machine

```yaml
in_code: IN_DENY_PROVISION_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Handle provision denial
  workflow: WF_DENY_PROVISION_V0

  inputs:
    employee_id:
      type: string
      required: true
      description: Employee whose provision was denied
    reason_code:
      type: string
      required: true
      description: Reason for denial

  outcomes:
    ACK:
      description: Denial request accepted for processing
    NACK:
      description: Denial request rejected

extensions:
  domain: pgs.ai_licensing
```
