# WF_PROVISION_AI_LICENSING_V0

## Header (Mandatory)

- **Artifact Code:** WF_PROVISION_AI_LICENSING_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** IN_PROVISION_AI_LICENSE_V0, CC_VALIDATE_ELIGIBILITY_V0, CC_PROVISION_LICENSE_V0, CC_APPEND_AUDIT_EVENT_V0

---

## 1. Intent

Process an AI license provisioning request with eligibility validation and cap enforcement.

---

## 2. Rationale

License provisioning is protocol-governed:
- Validates training completion
- Enforces hard license cap
- Records all decisions (success or denial)
- Denial is a first-class terminal state

---

## 3. Execution Graph

```
IN_PROVISION_AI_LICENSE_V0
    ├─ ACK → CC_VALIDATE_ELIGIBILITY_V0
    │           ├─ SUCCESS → CC_PROVISION_LICENSE_V0
    │           │               ├─ SUCCESS → CC_APPEND_AUDIT_EVENT_V0 (PROVISIONED) → EXIT:PROVISIONED
    │           │               └─ ALREADY_EXISTS/BACKEND_ERROR → EXIT:ERROR
    │           └─ VIOLATION → CC_APPEND_AUDIT_EVENT_V0 (DENIED) → EXIT:DENIED
    └─ NACK → EXIT:REJECTED
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_PROVISION_AI_LICENSE_V0 | IN | Entry intent for provisioning |
| CC_VALIDATE_ELIGIBILITY_V0 | CC | Validate training + cap availability |
| CC_ENFORCE_LICENSE_CAP_V0 | CC | Enforce hard cap limit |
| CC_PROVISION_LICENSE_V0 | CC | Register license assignment |
| CC_APPEND_AUDIT_EVENT_V0 | CC | Record decision to audit log |
| EXIT | EXIT | Terminal node |

---

## 5. Admission

No admission requirements - test exception to allow provisioning without employee registration.

---

## Machine

```yaml
wf_code: WF_PROVISION_AI_LICENSING_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0

runtime_binding: ai_governance::RB_LICENSE_BINDINGS_V0
structure: fb.topology::STRUCTURE_RUNTIME_EXECUTION_V0

core:
  summary: Process AI license provisioning request

  start_node: IN_PROVISION_AI_LICENSE_V0

  nodes:
    IN_PROVISION_AI_LICENSE_V0:
      type: IN
      code: IN_PROVISION_AI_LICENSE_V0
      next:
        ACK: CC_VALIDATE_ELIGIBILITY_V0
        NACK: EXIT_REJECTED

    CC_VALIDATE_ELIGIBILITY_V0:
      type: CC
      code: CC_VALIDATE_ELIGIBILITY_V0
      inputs:
        employee_id: $.payload.employee_id
        training_completed: $.payload.context.training_completed
        assigned_count: $.payload.context.assigned_count
        cap: $.payload.context.cap
      next:
        SUCCESS: CC_PROVISION_LICENSE_V0
        VIOLATION: CC_APPEND_AUDIT_EVENT_DENIED

    CC_PROVISION_LICENSE_V0:
      type: CC
      code: CC_PROVISION_LICENSE_V0
      inputs:
        employee_id: $.payload.employee_id
        license_id: $.payload.generated.license_id
      next:
        SUCCESS: CC_APPEND_AUDIT_EVENT_SUCCESS
        ALREADY_EXISTS: EXIT_ERROR
        VIOLATION: EXIT_ERROR
        BACKEND_ERROR: EXIT_ERROR

    CC_APPEND_AUDIT_EVENT_SUCCESS:
      type: CC
      code: CC_APPEND_AUDIT_EVENT_V0
      inputs:
        event_type: EV_LICENSE_PROVISIONED_V0
        employee_id: $.payload.employee_id
        decision: PROVISIONED
        reason_code: ""
        license_id: $.payload.generated.license_id
        data: {}
      next:
        SUCCESS: EXIT_PROVISIONED
        VIOLATION: EXIT_ERROR
        BACKEND_ERROR: EXIT_ERROR

    CC_APPEND_AUDIT_EVENT_DENIED:
      type: CC
      code: CC_APPEND_AUDIT_EVENT_V0
      inputs:
        event_type: EV_PROVISION_DENIED_V0
        employee_id: $.payload.employee_id
        decision: DENIED
        reason_code: $.payload.context.reason_code
        data: {}
      next:
        SUCCESS: EXIT_DENIED
        VIOLATION: EXIT_ERROR
        BACKEND_ERROR: EXIT_ERROR

    EXIT_PROVISIONED:
      type: EXIT
      reason: COMPLETED
      emit: EV_LICENSE_PROVISIONED_V0

    EXIT_DENIED:
      type: EXIT
      reason: COMPLETED
      emit: EV_PROVISION_DENIED_V0

    EXIT_REJECTED:
      type: EXIT
      reason: EXITED

    EXIT_ERROR:
      type: EXIT
      reason: FAILED
```
