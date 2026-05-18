# EV_AGENT_ACTION_DENIED_V0

## Header (Mandatory)

- **Artifact Code:** EV_AGENT_ACTION_DENIED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

An agent-proposed action has been denied by governance.

---

## 2. Rationale

Denial events record structural governance rejections:
- Agent action failed at a governance check
- Denial reason is deterministic and classified
- Symmetric with authorization — every decision is audited

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_GOVERN_AGENT_ACTION_V0 | CC_RECORD_DENIED_ACTION_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| action_id | string | true | Governance action identifier |
| tool_name | string | true | Requested tool |
| requesting_user_id | string | true | User the agent acts for |
| denial_reason | string | true | Structural denial reason code |
| decision | string | true | DENIED |
| timestamp | string (date-time) | true | When denied |

---

## Machine

```yaml
ev_code: EV_AGENT_ACTION_DENIED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Agent action denied by governance
  description: Emitted when an agent-proposed action is structurally denied at any governance stage

  schema:
    action_id:
      type: string
      required: true
    tool_name:
      type: string
      required: true
    requesting_user_id:
      type: string
      required: true
    denial_reason:
      type: string
      required: true
    decision:
      type: string
      required: true
    timestamp:
      type: string
      format: date-time
      required: true
```
