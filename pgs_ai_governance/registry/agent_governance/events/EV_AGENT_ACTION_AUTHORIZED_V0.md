# EV_AGENT_ACTION_AUTHORIZED_V0

## Header (Mandatory)

- **Artifact Code:** EV_AGENT_ACTION_AUTHORIZED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

An agent-proposed action has been authorized by governance.

---

## 2. Rationale

Authorization events record successful governance mediation:
- Agent action passed all governance checks
- Tool declaration, license binding, and parameter validation all succeeded
- Action is authorized for execution

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_GOVERN_AGENT_ACTION_V0 | CC_RECORD_GOVERNED_ACTION_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| action_id | string | true | Governance action identifier |
| tool_name | string | true | Authorized tool |
| requesting_user_id | string | true | User the agent acts for |
| license_tier | string | true | License tier that authorized the action |
| decision | string | true | AUTHORIZED |
| timestamp | string (date-time) | true | When authorized |

---

## Machine

```yaml
ev_code: EV_AGENT_ACTION_AUTHORIZED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Agent action authorized by governance
  description: Emitted when an agent-proposed action passes all governance checks and is authorized for execution

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
    license_tier:
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
