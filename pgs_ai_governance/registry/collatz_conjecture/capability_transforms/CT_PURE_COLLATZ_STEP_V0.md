# CT_PURE_COLLATZ_STEP_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_COLLATZ_STEP_V0
- **Artifact Kind:** atom
- **Governed By:** fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## Human

### 1. Intent

Compute the full Collatz sequence for each number in the input list.

For each n, iterate: if n is even → n/2; if n is odd → 3n+1. Continue until reaching 1.
Capture the complete path as a sequence.

---

### 2. Rationale

The Collatz iteration is pure: given n, the sequence is entirely deterministic.
No external state, no branching beyond the mathematical rule.

This transform provides:
- Complete sequence per seed value
- Deterministic, replay-safe computation
- No coupling to conjecture validity (that is verified separately)

---

### 3. Naming Convention                                                                                                                                                                                                                                                                                                                                                                                                                       

- **Artifact Code:** CT_PURE_COLLATZ_STEP_V0 (full versioned identifier)
- **Operation:** COLLATZ_STEP (execution opcode)

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases
- Computing Collatz sequences for protocol-governed demonstration
- Input to termination verification transforms

#### 4.2 Invalid Use Cases
- Verifying conjecture validity (use CT_TERMINATION_CHECK_V0)
- Generating sequences for numbers ≥ 1000000 (domain contract: inputs < 1000000)
- Any operation with side effects

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same input yields same sequence |
| Purity Class | ct_pure | No side effects, no state |
| Side Effects | NONE | Fully pure computation |
| Replay Safe | YES | Identical inputs produce identical output |

---

### 6. Structural Checklist

- [x] Single responsibility
- [x] No implicit state
- [x] No domain semantics beyond Collatz rule
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
- Required input `numbers` is not declared
- Output `sequences` is not declared

**Runtime validation MUST fail if:**
- `numbers` is not a list
- Any element is not a positive integer

---

### 9. Observability

This atom does NOT emit traces.

**Rationale:** Pure computation with no side effects or state changes.

---

### 10. Minimal Usage Shape

```
numbers → CT_PURE_COLLATZ_STEP_V0 → sequences
```

---

## Machine

```yaml
ct_code: CT_PURE_COLLATZ_STEP_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Compute full Collatz sequence for each input number
  description: For each n in numbers, iterates the Collatz rule until reaching 1. Returns mapping of n → sequence.

  inputs:
    numbers:
      type: array
      required: true
      description: "List of positive integers for which to compute sequences"

  outputs:
    sequences:
      type: object
      required: true
      description: "Mapping from str(n) to full Collatz sequence as list of integers"

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: PURE_COLLATZ_STEP
  implementation:
    module: pgs_ai_governance.implementation.capability_transforms.atoms.ct_pure_collatz_step_v0
    callable: execute
```
