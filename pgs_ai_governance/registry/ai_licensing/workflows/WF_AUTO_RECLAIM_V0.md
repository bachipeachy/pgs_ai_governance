# WF_AUTO_RECLAIM_V0

## Header (Mandatory)

- **Artifact Code:** WF_AUTO_RECLAIM_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** IN_RECLAIM_LICENSE_V0, CC_RECLAIM_UNUSED_LICENSE_V0, CC_APPEND_AUDIT_EVENT_V0

---

## 1. Intent

Evaluate license inactivity and autonomously reclaim if threshold exceeded.

---

## 2. Rationale

Autonomous reclamation enforces use-it-or-lose-it:
- Evaluates days since last usage
- Reclaims license if inactive >= threshold
- Returns license to pool for pending employees
- No human intervention required

---

## 3. Execution Graph

```
IN_RECLAIM_LICENSE_V0
    ├─ ACK → CC_RECLAIM_UNUSED_LICENSE_V0
    │           ├─ SUCCESS → CC_APPEND_AUDIT_EVENT_V0 (RECLAIMED) → EXIT:RECLAIMED
    │           ├─ ACTIVE → EXIT:ACTIVE
    │           └─ NOT_FOUND/BACKEND_ERROR → EXIT:ERROR
    └─ NACK → EXIT:REJECTED
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_RECLAIM_LICENSE_V0 | IN | Entry intent for reclamation |
| CC_RECLAIM_UNUSED_LICENSE_V0 | CC | Evaluate and reclaim if inactive |
| CC_APPEND_AUDIT_EVENT_V0 | CC | Record reclamation to audit log |
| EXIT | EXIT | Terminal node |

---

## 5. Admission

| Requirement | Description |
|-------------|-------------|
| requires | EV_LICENSE_PROVISIONED_V0 |
| forbids | EV_LICENSE_REVOKED_V0 |

License must be provisioned but not yet revoked.

---

## Machine

```yaml
wf_code: WF_AUTO_RECLAIM_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0

runtime_binding: ai_governance::RB_LICENSE_BINDINGS_V0
subdomain: ai_licensing
structure: fb.topology::STRUCTURE_RUNTIME_EXECUTION_V0

core:
  summary: Autonomous license reclamation

  admission:
    requires:
      - EV_LICENSE_PROVISIONED_V0
    forbids:
      - EV_LICENSE_REVOKED_V0
    bindings:
      EV_LICENSE_PROVISIONED_V0:
        license_id: license_id
        employee_id: employee_id

  start_node: IN_RECLAIM_LICENSE_V0

  nodes:
    IN_RECLAIM_LICENSE_V0:
      type: IN
      code: IN_RECLAIM_LICENSE_V0
      next:
        ACK: CC_RECLAIM_UNUSED_LICENSE_V0
        NACK: EXIT_REJECTED

    CC_RECLAIM_UNUSED_LICENSE_V0:
      type: CC
      code: CC_RECLAIM_UNUSED_LICENSE_V0
      inputs:
        license_id: $.payload.license_id
        employee_id: $.payload.context.employee_id
        last_active_date: $.payload.context.last_active_date
        threshold_days: $.payload.threshold_days
      next:
        SUCCESS: CC_APPEND_AUDIT_EVENT_RECLAIMED
        ACTIVE: EXIT_ACTIVE
        NOT_FOUND: EXIT_ERROR
        BACKEND_ERROR: EXIT_ERROR

    CC_APPEND_AUDIT_EVENT_RECLAIMED:
      type: CC
      code: CC_APPEND_AUDIT_EVENT_V0
      inputs:
        event_type: EV_LICENSE_REVOKED_V0
        employee_id: $.payload.context.employee_id
        decision: RECLAIMED
        reason_code: INACTIVITY
        data:
          license_id: $.payload.license_id
          days_inactive: $.payload.context.days_inactive
      next:
        SUCCESS: EXIT_RECLAIMED
        VIOLATION: EXIT_ERROR
        BACKEND_ERROR: EXIT_ERROR

    EXIT_RECLAIMED:
      type: EXIT
      reason: COMPLETED
      emit: EV_LICENSE_REVOKED_V0

    EXIT_ACTIVE:
      type: EXIT
      reason: COMPLETED

    EXIT_REJECTED:
      type: EXIT
      reason: EXITED

    EXIT_ERROR:
      type: EXIT
      reason: FAILED
```
