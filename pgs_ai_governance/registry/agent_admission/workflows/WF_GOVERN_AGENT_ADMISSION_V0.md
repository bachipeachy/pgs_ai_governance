# WF_GOVERN_AGENT_ADMISSION_V0

## Header (Mandatory)

- **Artifact Code:** WF_GOVERN_AGENT_ADMISSION_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** IN_AGENT_ADMISSION_REQUESTED_V0, CC_NORMALIZE_AGENT_REQUEST_V0, CC_CHECK_AGENT_TOOL_DECLARED_V0, CC_RESOLVE_LICENSE_TIER_V0, CC_BIND_AGENT_LICENSE_TO_TOOL_SURFACE_V0, CC_VALIDATE_AGENT_TOOL_PARAMETERS_V0, CC_RECORD_GOVERNED_ACTION_V0, CC_RECORD_DENIED_ACTION_V0, RB_AGENT_ADMISSION_BINDINGS_V0

---

## 1. Intent

Protocol-governed admission of autonomous agent tool proposals with license-tier authority binding.

---

## 2. Rationale

Agent admission is structurally governed — not operationally supervised:
- All agent tool proposals enter through IN_AGENT_ADMISSION_REQUESTED_V0 (no ambient authority)
- Five sequential governance gates: normalize, tool check, license resolve, tool bind, parameter validate
- All authorized actions and all denied actions produce symmetric audit trails via CC_RECORD_GOVERNED_ACTION_V0 / CC_RECORD_DENIED_ACTION_V0
- Four distinct denial exits: UNDECLARED_TOOL, UNAUTHORIZED_ACTOR, UNAUTHORIZED_TOOL, PARAMETER_VIOLATION
- DAG topology is identical to WF_GOVERN_AGENT_ACTION_V0; CC references are the agent_admission variants

---

## 3. Execution Graph

```
IN_AGENT_ADMISSION_REQUESTED_V0
    ├─ ACK → CC_NORMALIZE_AGENT_REQUEST_V0
    │           ├─ SUCCESS → CC_CHECK_AGENT_TOOL_DECLARED_V0
    │           │               ├─ SUCCESS → CC_RESOLVE_LICENSE_TIER_V0
    │           │               │               ├─ SUCCESS → CC_BIND_AGENT_LICENSE_TO_TOOL_SURFACE_V0
    │           │               │               │               ├─ SUCCESS → CC_VALIDATE_AGENT_TOOL_PARAMETERS_V0
    │           │               │               │               │               ├─ SUCCESS → CC_RECORD_GOVERNED_ACTION_V0 → EXIT_SUCCESS
    │           │               │               │               │               └─ VIOLATION → CC_AUDIT_PARAMETER_VIOLATION → EXIT_PARAMETER_VIOLATION
    │           │               │               │               └─ VIOLATION → CC_AUDIT_UNAUTHORIZED_TOOL → EXIT_UNAUTHORIZED_TOOL
    │           │               │               ├─ NOT_FOUND → CC_AUDIT_UNAUTHORIZED_ACTOR → EXIT_UNAUTHORIZED_ACTOR
    │           │               │               └─ VIOLATION → CC_AUDIT_UNAUTHORIZED_ACTOR → EXIT_UNAUTHORIZED_ACTOR
    │           │               └─ VIOLATION → CC_AUDIT_UNDECLARED_TOOL → EXIT_UNDECLARED_TOOL
    │           └─ VIOLATION → EXIT_ERROR
    └─ NACK → EXIT_REJECTED
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_AGENT_ADMISSION_REQUESTED_V0 | IN | Entry intent for agent admission governance |
| CC_NORMALIZE_AGENT_REQUEST_V0 | CC | Generate deterministic intent hash |
| CC_CHECK_AGENT_TOOL_DECLARED_V0 | CC | Verify tool in closed agent tool registry |
| CC_RESOLVE_LICENSE_TIER_V0 | CC | Read license facts, validate active status |
| CC_BIND_AGENT_LICENSE_TO_TOOL_SURFACE_V0 | CC | Map tier to agent tool surface, verify authorization |
| CC_VALIDATE_AGENT_TOOL_PARAMETERS_V0 | CC | Enforce parameter constraints for agent tools |
| CC_RECORD_GOVERNED_ACTION_V0 | CC | Record authorized action + audit |
| CC_AUDIT_UNDECLARED_TOOL | CC | Record denial: tool not in agent registry |
| CC_AUDIT_UNAUTHORIZED_ACTOR | CC | Record denial: no license or inactive license |
| CC_AUDIT_UNAUTHORIZED_TOOL | CC | Record denial: tool not permitted for tier |
| CC_AUDIT_PARAMETER_VIOLATION | CC | Record denial: parameter constraint failed |
| EXIT_SUCCESS | EXIT | Action admitted — authorized |
| EXIT_UNDECLARED_TOOL | EXIT | Tool not in closed agent registry |
| EXIT_UNAUTHORIZED_ACTOR | EXIT | No license or inactive license |
| EXIT_UNAUTHORIZED_TOOL | EXIT | Tool not authorized for resolved tier |
| EXIT_PARAMETER_VIOLATION | EXIT | Parameter constraints failed |
| EXIT_ERROR | EXIT | Internal error |
| EXIT_REJECTED | EXIT | Intent admission rejected |

---

## 5. Admission

| Requirement | Description |
|-------------|-------------|
| requires | — |
| forbids | — |

No admission constraints in v0.

---

## Machine

```yaml
wf_code: WF_GOVERN_AGENT_ADMISSION_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0
runtime_binding: ai_governance::RB_AGENT_ADMISSION_BINDINGS_V0
subdomain: agent_admission

core:
  summary: Protocol-governed admission of autonomous agent tool proposals

  start_node: IN_AGENT_ADMISSION_REQUESTED_V0

  nodes:
    IN_AGENT_ADMISSION_REQUESTED_V0:
      type: IN
      code: IN_AGENT_ADMISSION_REQUESTED_V0
      next:
        ACK: CC_NORMALIZE_AGENT_REQUEST_V0
        NACK: EXIT_REJECTED

    CC_NORMALIZE_AGENT_REQUEST_V0:
      type: CC
      code: CC_NORMALIZE_AGENT_REQUEST_V0
      inputs:
        tool_name: $.payload.tool_name
        requesting_user_id: $.payload.requesting_user_id
        domain_context: $.payload.domain_context
      next:
        SUCCESS: CC_CHECK_AGENT_TOOL_DECLARED_V0
        VIOLATION: EXIT_ERROR

    CC_CHECK_AGENT_TOOL_DECLARED_V0:
      type: CC
      code: CC_CHECK_AGENT_TOOL_DECLARED_V0
      inputs:
        tool_name: $.payload.tool_name
      next:
        SUCCESS: CC_RESOLVE_LICENSE_TIER_V0
        VIOLATION: CC_AUDIT_UNDECLARED_TOOL

    CC_RESOLVE_LICENSE_TIER_V0:
      type: CC
      code: CC_RESOLVE_LICENSE_TIER_V0
      inputs:
        requesting_user_id: $.payload.requesting_user_id
      next:
        SUCCESS: CC_BIND_AGENT_LICENSE_TO_TOOL_SURFACE_V0
        NOT_FOUND: CC_AUDIT_UNAUTHORIZED_ACTOR
        VIOLATION: CC_AUDIT_UNAUTHORIZED_ACTOR
        BACKEND_ERROR: EXIT_ERROR

    CC_BIND_AGENT_LICENSE_TO_TOOL_SURFACE_V0:
      type: CC
      code: CC_BIND_AGENT_LICENSE_TO_TOOL_SURFACE_V0
      inputs:
        tool_name: $.payload.tool_name
        license_tier: $.results.CC_RESOLVE_LICENSE_TIER_V0.license_tier
      next:
        SUCCESS: CC_VALIDATE_AGENT_TOOL_PARAMETERS_V0
        VIOLATION: CC_AUDIT_UNAUTHORIZED_TOOL

    CC_VALIDATE_AGENT_TOOL_PARAMETERS_V0:
      type: CC
      code: CC_VALIDATE_AGENT_TOOL_PARAMETERS_V0
      inputs:
        tool_name: $.payload.tool_name
        parameters: $.payload.parameters
      next:
        SUCCESS: CC_RECORD_GOVERNED_ACTION_V0
        VIOLATION: CC_AUDIT_PARAMETER_VIOLATION

    CC_RECORD_GOVERNED_ACTION_V0:
      type: CC
      code: CC_RECORD_GOVERNED_ACTION_V0
      inputs:
        tool_name: $.payload.tool_name
        parameters: $.payload.parameters
        requesting_user_id: $.payload.requesting_user_id
        license_tier: $.results.CC_RESOLVE_LICENSE_TIER_V0.license_tier
        domain_context: $.payload.domain_context
        intent_hash: $.results.CC_NORMALIZE_AGENT_REQUEST_V0.intent_hash
      next:
        SUCCESS: EXIT_SUCCESS
        ALREADY_EXISTS: EXIT_SUCCESS
        VIOLATION: EXIT_ERROR
        BACKEND_ERROR: EXIT_ERROR

    CC_AUDIT_UNDECLARED_TOOL:
      type: CC
      code: CC_RECORD_DENIED_ACTION_V0
      inputs:
        tool_name: $.payload.tool_name
        requesting_user_id: $.payload.requesting_user_id
        domain_context: $.payload.domain_context
        denial_reason: UNDECLARED_TOOL
      next:
        SUCCESS: EXIT_UNDECLARED_TOOL
        VIOLATION: EXIT_ERROR
        BACKEND_ERROR: EXIT_ERROR

    CC_AUDIT_UNAUTHORIZED_ACTOR:
      type: CC
      code: CC_RECORD_DENIED_ACTION_V0
      inputs:
        tool_name: $.payload.tool_name
        requesting_user_id: $.payload.requesting_user_id
        domain_context: $.payload.domain_context
        denial_reason: UNAUTHORIZED_ACTOR
      next:
        SUCCESS: EXIT_UNAUTHORIZED_ACTOR
        VIOLATION: EXIT_ERROR
        BACKEND_ERROR: EXIT_ERROR

    CC_AUDIT_UNAUTHORIZED_TOOL:
      type: CC
      code: CC_RECORD_DENIED_ACTION_V0
      inputs:
        tool_name: $.payload.tool_name
        requesting_user_id: $.payload.requesting_user_id
        domain_context: $.payload.domain_context
        denial_reason: UNAUTHORIZED_TOOL
      next:
        SUCCESS: EXIT_UNAUTHORIZED_TOOL
        VIOLATION: EXIT_ERROR
        BACKEND_ERROR: EXIT_ERROR

    CC_AUDIT_PARAMETER_VIOLATION:
      type: CC
      code: CC_RECORD_DENIED_ACTION_V0
      inputs:
        tool_name: $.payload.tool_name
        requesting_user_id: $.payload.requesting_user_id
        domain_context: $.payload.domain_context
        denial_reason: PARAMETER_VIOLATION
      next:
        SUCCESS: EXIT_PARAMETER_VIOLATION
        VIOLATION: EXIT_ERROR
        BACKEND_ERROR: EXIT_ERROR

    EXIT_SUCCESS:
      type: EXIT
      reason: COMPLETED
      emit: EV_AGENT_ACTION_AUTHORIZED_V0

    EXIT_UNDECLARED_TOOL:
      type: EXIT
      reason: COMPLETED
      emit: EV_AGENT_ACTION_DENIED_V0

    EXIT_UNAUTHORIZED_ACTOR:
      type: EXIT
      reason: COMPLETED
      emit: EV_AGENT_ACTION_DENIED_V0

    EXIT_UNAUTHORIZED_TOOL:
      type: EXIT
      reason: COMPLETED
      emit: EV_AGENT_ACTION_DENIED_V0

    EXIT_PARAMETER_VIOLATION:
      type: EXIT
      reason: COMPLETED
      emit: EV_AGENT_ACTION_DENIED_V0

    EXIT_ERROR:
      type: EXIT
      reason: FAILED

    EXIT_REJECTED:
      type: EXIT
      reason: EXITED
```
