# AC_SYSTEM_GOVERNOR_V0

## Header (Mandatory)

- **Artifact Code:** AC_SYSTEM_GOVERNOR_V0
- **Artifact Kind:** actor
- **Governed By:** CONSTITUTION_GOVERNANCE_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Identity

The governance execution authority that mediates agent-proposed actions.

---

## 2. Rationale

The system governor enforces protocol governance:
- Evaluates agent requests against declared policy
- Binds license authority to tool surfaces
- Records all governance decisions (authorization and denial)

---

## 3. Type

| Property | Value |
|----------|-------|
| Type | system |

---

## 4. Attributes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| governor_id | string | true | Governance authority identifier |

---

## Machine

```yaml
ac_code: AC_SYSTEM_GOVERNOR_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  summary: Governance execution authority
  description: Mediates agent-proposed actions with constitutional policy enforcement
  type: system

  attributes:
    governor_id:
      type: string
      required: true
```
