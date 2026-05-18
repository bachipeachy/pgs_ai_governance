# IN_AGENT_ACTION_REQUESTED_V0

## Header (Mandatory)

- **Artifact Code:** IN_AGENT_ACTION_REQUESTED_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_GOVERN_AGENT_ACTION_V0

---

## 1. Intent

Request governance mediation of an agent-proposed action.

---

## 2. Rationale

All agent actions normalize to a single governed intent:
- No ambient authority — agents cannot invoke tools directly
- Every proposed action enters the governance pipeline through this intent
- The intent declares the full input surface for governance evaluation

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_GOVERN_AGENT_ACTION_V0 | Workflow that mediates this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tool_name | string | true | Requested tool identifier from closed registry |
| parameters | object | true | Tool-specific parameter key-value map |
| requesting_user_id | string | true | Identifier of the user the agent acts on behalf of |
| domain_context | string | true | Domain context for the request |
| request_id | string | false | Client-provided request correlation ID |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Governance request accepted for processing |
| NACK | Governance request rejected at admission |

---

## 6. Domain

- **Domain:** pgs.governance.agent

---

## Machine

```yaml
in_code: IN_AGENT_ACTION_REQUESTED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Request governance mediation of agent-proposed action
  workflow: WF_GOVERN_AGENT_ACTION_V0

  inputs:
    tool_name:
      type: string
      required: true
      description: Requested tool identifier from closed registry
    parameters:
      type: object
      required: true
      description: Tool-specific parameter key-value map
    requesting_user_id:
      type: string
      required: true
      description: Identifier of the user the agent acts on behalf of
    domain_context:
      type: string
      required: true
      description: Domain context for the request
    request_id:
      type: string
      required: false
      description: Client-provided request correlation ID

  outcomes:
    ACK:
      description: Governance request accepted for processing
    NACK:
      description: Governance request rejected at admission

extensions:
  domain: pgs.governance.agent
```
