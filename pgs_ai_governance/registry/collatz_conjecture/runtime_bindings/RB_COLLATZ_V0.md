# RB_COLLATZ_V0

## Header (Mandatory)

- **Artifact Code:** RB_COLLATZ_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0, STRUCTURE_COLLATZ_STORAGE_V0

---

## 1. Purpose

Bind capability side effects to concrete host implementations for the Collatz demonstration domain.

---

## 2. Rationale

Runtime bindings provide environment-specific execution wiring:
- Maps CS_MUTABLE_JSON_V0 to its host class
- Configures storage path via parameters
- Keeps protocol artifacts environment-agnostic

---

## 3. Bindings

| CS Artifact | Host | Purpose |
|-------------|---------|---------|
| CS_MUTABLE_JSON_V0 | MutableJsonRuntime | Collatz result storage |

---

## 4. Parameters

| Parameter | Description |
|-----------|-------------|
| module_data_root | Base path for module runtime data (resolved from env_facts) |

---

## Machine

```yaml
rb_code: RB_COLLATZ_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

parameters:
  - module_data_root

core:
  summary: Runtime binding for Collatz demonstration storage
  description: Binds CS_MUTABLE_JSON_V0 to MutableJsonRuntime for persisting Collatz computation results.
  storage_structure: ai_governance::STRUCTURE_COLLATZ_STORAGE_V0

  bindings:
    capability_side_effects::CS_MUTABLE_JSON_V0:
      type: CS
      host: MutableJsonRuntime
      operation: READ_WRITE
      policy: {}

extensions:
  notes:
    - This binding is specific to the collatz_conjecture sub-domain.
    - Storage path is resolved via template parameters at runtime.
    - Changing the binding does not require modifying workflow or CC artifacts.
```
