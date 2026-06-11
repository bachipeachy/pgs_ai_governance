# IN_AGENT_ADMISSION_REQUESTED_V0

## Header (Mandatory)

- **Artifact Code:** IN_AGENT_ADMISSION_REQUESTED_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_GOVERN_AGENT_ADMISSION_V0

---

## 1. Intent

Request governance admission of an autonomous agent tool proposal.

---

## 2. Rationale

All autonomous agent tool proposals must pass structural governance before any tool executes:
- No ambient authority — agents cannot invoke tools directly
- Every tool proposal enters the governance pipeline through this intent
- The intent declares the full input surface required for admission evaluation
- Schema is identical to IN_AGENT_ACTION_REQUESTED_V0; the only difference is the workflow binding
- 1:1 IN_→WF_ binding is a governance invariant — a new workflow always requires a new intent

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_GOVERN_AGENT_ADMISSION_V0 | Admission workflow that governs this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tool_name | string | true | Requested tool identifier from closed agent tool registry |
| parameters | object | true | Tool-specific parameter key-value map |
| requesting_user_id | string | true | Identity of the user on whose behalf the agent acts |
| domain_context | string | true | Domain context for the request |
| request_id | string | false | Client-provided request correlation ID |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Admission request accepted for governance evaluation |
| NACK | Admission request rejected at intent gate |

---

## 6. Domain

- **Domain:** pgs.governance.agent.admission

---

## Machine

```yaml
in_code: IN_AGENT_ADMISSION_REQUESTED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Request governance admission of an autonomous agent tool proposal
  workflow: WF_GOVERN_AGENT_ADMISSION_V0

  inputs:
    tool_name:
      type: string
      required: true
      description: Requested tool identifier from closed agent tool registry
    parameters:
      type: object
      required: true
      description: Tool-specific parameter key-value map
    requesting_user_id:
      type: string
      required: true
      description: Identity of the user on whose behalf the agent acts
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
      description: Admission request accepted for governance evaluation
    NACK:
      description: Admission request rejected at intent gate

extensions:
  domain: pgs.governance.agent.admission
```
