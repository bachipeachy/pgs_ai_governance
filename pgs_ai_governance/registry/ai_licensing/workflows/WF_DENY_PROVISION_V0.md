# WF_DENY_PROVISION_V0

## Header (Mandatory)

- **Artifact Code:** WF_DENY_PROVISION_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** IN_DENY_PROVISION_V0, CC_APPEND_AUDIT_EVENT_V0

---

## 1. Intent

Handle provisioning denial by emitting denial event and recording to audit log.

---

## 2. Rationale

Denial handling ensures first-class terminal outcomes:
- Emits EV_PROVISION_DENIED_V0
- Appends to audit log
- Terminates cleanly (no retries, no loops)

---

## 3. Execution Graph

```
IN_DENY_PROVISION_V0
    ├─ ACK → CC_APPEND_AUDIT_EVENT_V0
    └─ NACK → EXIT:ERROR

CC_APPEND_AUDIT_EVENT_V0
    ├─ SUCCESS → EXIT:DENIED
    └─ VIOLATION/BACKEND_ERROR → EXIT:ERROR
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_DENY_PROVISION_V0 | IN | Entry point for provision denial |
| CC_APPEND_AUDIT_EVENT_V0 | CC | Record denial to audit log |
| EXIT | EXIT | Terminal node |

---

## Machine

```yaml
wf_code: WF_DENY_PROVISION_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0

runtime_binding: ai_governance::RB_LICENSE_BINDINGS_V0
structure: fb.topology::STRUCTURE_RUNTIME_EXECUTION_V0

core:
  summary: Handle provisioning denial

  start_node: IN_DENY_PROVISION_V0

  nodes:
    IN_DENY_PROVISION_V0:
      type: IN
      code: IN_DENY_PROVISION_V0
      payload_schema:
        employee_id: string
        reason_code: string
      next:
        ACK: CC_APPEND_AUDIT_EVENT_V0
        NACK: EXIT_ERROR

    CC_APPEND_AUDIT_EVENT_V0:
      type: CC
      code: CC_APPEND_AUDIT_EVENT_V0
      inputs:
        event_type: EV_PROVISION_DENIED_V0
        employee_id: $.payload.employee_id
        decision: DENIED
        reason_code: $.payload.reason_code
      next:
        SUCCESS: EXIT_DENIED
        VIOLATION: EXIT_ERROR
        BACKEND_ERROR: EXIT_ERROR

    EXIT_DENIED:
      type: EXIT
      reason: COMPLETED
      emit: EV_PROVISION_DENIED_V0

    EXIT_ERROR:
      type: EXIT
      reason: FAILED
```
