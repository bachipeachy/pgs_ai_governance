# AC_SYSTEM_V0

## Header (Mandatory)

- **Artifact Code:** AC_SYSTEM_V0
- **Artifact Kind:** actor
- **Governed By:** CONSTITUTION_GOVERNANCE_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Identity

A system actor represents a protocol authority for fact injection and automated operations.

---

## 2. Rationale

System actors enable protocol automation:
- Inject facts from external systems (HR, LMS, telemetry)
- Perform autonomous reclamation
- Provide audit trail for system-initiated operations

---

## 3. Type

| Property | Value |
|----------|-------|
| Type | system |

---

## 4. Attributes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| role | string | true | System role identifier |

---

## Machine

```yaml
ac_code: AC_SYSTEM_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  summary: System Authority Actor
  description: Represents a protocol authority for fact injection and automation
  type: system

  attributes:
    role:
      type: string
      required: true
```
