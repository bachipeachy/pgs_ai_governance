# AC_EMPLOYEE_V0

## Header (Mandatory)

- **Artifact Code:** AC_EMPLOYEE_V0
- **Artifact Kind:** actor
- **Governed By:** CONSTITUTION_GOVERNANCE_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Identity

An employee actor represents a person eligible for AI license provisioning.

---

## 2. Rationale

Employee actors are subjects of protocol governance:
- Represent human identities in the licensing domain
- Track training completion status
- Provide natural key for license assignment

---

## 3. Type

| Property | Value |
|----------|-------|
| Type | person |

---

## 4. Attributes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| employee_id | string | true | Unique employee identifier |
| training_completed | boolean | false | Whether required training is completed |

---

## Machine

```yaml
ac_code: AC_EMPLOYEE_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  summary: Employee Actor
  description: Represents a person eligible for AI license provisioning
  type: person

  attributes:
    employee_id:
      type: string
      required: true
    training_completed:
      type: boolean
      default: false
```
