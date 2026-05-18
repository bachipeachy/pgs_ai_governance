# IN_COLLATZ_INPUT_VALIDATED_V0

## Header (Mandatory)

- **Artifact Code:** IN_COLLATZ_INPUT_VALIDATED_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_DEMO_COLLATZ_CONJECTURE_V0

---

## 1. Intent

Admission gate for the Collatz demonstration workflow.

Accepts a list of positive integers, each strictly less than 100.
Rejects payloads that contain non-positive values, non-integers, or numbers >= 100.

---

## 2. Rationale

Input validation is a protocol gate:
- Constrains the domain to integers the conjecture is well-understood for
- Prevents unbounded sequences from entering the execution graph
- Ensures the conjecture demonstration is reproducible and termination-finite

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_DEMO_COLLATZ_CONJECTURE_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| numbers | array | true | List of positive integers, each in range [1, 99] |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Input is valid — workflow execution proceeds |
| NACK | Input is invalid — payload rejected before execution |

---

## 6. Domain

- **Domain:** pgs.collatz_conjecture

---

## Machine

```yaml
in_code: IN_COLLATZ_INPUT_VALIDATED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Validate Collatz input — list of positive integers < 100
  workflow: WF_DEMO_COLLATZ_CONJECTURE_V0

  inputs:
    numbers:
      type: array
      required: true
      description: "List of positive integers in [1, 1000000]"

  outcomes:
    ACK:
      description: Input valid — execution proceeds
    NACK:
      description: Input invalid — execution rejected

extensions:
  domain: pgs.collatz_conjecture
  admission_rules:
    - "numbers must be a non-empty array"
    - "each element must be a positive integer"
    - "each element must be < 1000000"
```
