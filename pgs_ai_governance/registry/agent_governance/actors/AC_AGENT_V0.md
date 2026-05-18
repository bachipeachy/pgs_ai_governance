# AC_AGENT_V0

## Header (Mandatory)

- **Artifact Code:** AC_AGENT_V0
- **Artifact Kind:** actor
- **Governed By:** CONSTITUTION_GOVERNANCE_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Identity

An autonomous agent that proposes actions through the governance protocol.

---

## 2. Rationale

Agent actors are probabilistic intent emitters:
- Propose tool invocations on behalf of users
- Subject to governance mediation before any action executes
- May not invoke tools directly — all actions route through governance

---

## 3. Type

| Property | Value |
|----------|-------|
| Type | agent |

---

## 4. Attributes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| agent_id | string | true | Unique agent identifier |
| requesting_user_id | string | true | User the agent acts on behalf of |

---

## Machine

```yaml
ac_code: AC_AGENT_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  summary: Probabilistic intent emitter
  description: Autonomous agent that proposes actions through governance protocol
  type: agent

  attributes:
    agent_id:
      type: string
      required: true
    requesting_user_id:
      type: string
      required: true
```
