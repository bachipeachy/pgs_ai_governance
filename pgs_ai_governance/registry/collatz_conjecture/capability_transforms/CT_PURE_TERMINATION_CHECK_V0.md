# CT_PURE_TERMINATION_CHECK_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_TERMINATION_CHECK_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## Human

### 1. Intent

Verify that every Collatz sequence in the input terminates at 1.

Inspects the final element of each sequence. If any sequence does not end at 1,
that seed is flagged as non-terminating. Returns a boolean verdict and the list
of non-terminating seeds.

---

### 2. Rationale

Termination verification is a protocol gate for conjecture demonstration.
This transform is deliberately separated from sequence computation (CT_COLLATZ_STEP_V0)
so that the verification logic is independently auditable.

This transform provides:
- Binary verdict: all_terminate (bool)
- Evidence list: non_terminating seeds
- Deterministic, replay-safe check

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_TERMINATION_CHECK_V0 (full versioned identifier)
- **Operation:** TERMINATION_CHECK (execution opcode)

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases
- Verifying conjecture holds for computed sequences
- Input to CC_VERIFY_TERMINATION_V0

#### 4.2 Invalid Use Cases
- Computing sequences (use CT_COLLATZ_STEP_V0)
- Making claims beyond the input set (conjecture is universally unproven)

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same sequences → same verdict |
| Purity Class | ct_pure | No side effects, no state |
| Side Effects | NONE | Fully pure computation |
| Replay Safe | YES | Identical inputs produce identical output |

---

### 6. Structural Checklist

- [x] Single responsibility
- [x] No implicit state
- [x] No domain semantics beyond termination check
- [x] Inputs fully declared
- [x] Outputs fully declared
- [x] No hidden control flow

---

### 7. Composition Rules (Atom-Specific)

As an **atom**, this CT:
- MUST NOT invoke other CTs
- MUST perform exactly one atomic operation
- MAY be composed by molecules

---

### 8. Validation Expectations

**Static validation MUST fail if:**
- `ct_kind` is not `atom`
- `ct_purity` is not `ct_pure`
- Required input `sequences` is not declared
- Outputs `all_terminate` and `non_terminating` are not declared

**Runtime validation MUST fail if:**
- `sequences` is not a dict
- Any sequence entry is not a list

---

### 9. Observability

This atom does NOT emit traces.

**Rationale:** Pure computation with no side effects or state changes.

---

### 10. Minimal Usage Shape

```
sequences → CT_PURE_TERMINATION_CHECK_V0 → all_terminate, non_terminating
```

---

## Machine

```yaml
ct_code: CT_PURE_TERMINATION_CHECK_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Verify all Collatz sequences terminate at 1
  description: Inspects last element of each sequence. Returns all_terminate boolean and list of non-terminating seeds.
  inputs:
    sequences:
      type: object
      required: true
      description: "Mapping from str(n) to Collatz sequence list"

  outputs:
    all_terminate:
      type: boolean
      required: true
      description: "True if every sequence ends at 1"
    non_terminating:
      type: array
      required: true
      description: "List of seeds whose sequences did not end at 1"
machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: PURE_TERMINATION_CHECK
  implementation:
    module: pgs_ai_governance.implementation.capability_transforms.atoms.ct_pure_termination_check_v0
    callable: execute
```
