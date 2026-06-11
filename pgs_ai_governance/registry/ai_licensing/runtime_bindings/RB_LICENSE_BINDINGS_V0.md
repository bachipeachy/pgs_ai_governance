# RB_LICENSE_BINDINGS_V0

## Header (Mandatory)

- **Artifact Code:** RB_LICENSE_BINDINGS_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_REGISTRY_V0, CS_APPENDONLY_JSONL_V0

---

## 1. Purpose

Bind capability side effects to concrete host implementations for license management execution.

---

## 2. Rationale

Runtime bindings provide environment-specific execution wiring:
- Maps CS artifacts to host classes
- Configures storage paths via parameters
- Keeps protocol artifacts environment-agnostic

---

## 3. Bindings

| CS Artifact | Host | Purpose |
|-------------|---------|---------|
| CS_REGISTRY_V0 | RegistryRuntime | License assignment registry |
| CS_APPENDONLY_JSONL_V0 | AppendOnlyJsonlRuntime | Immutable audit trail |

---

## 4. Parameters

| Parameter | Description |
|-----------|-------------|
| module_data_root | Base path for module runtime data (resolved from env_facts) |

---

## Machine

```yaml
rb_code: RB_LICENSE_BINDINGS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

parameters:
  - module_data_root

core:
  summary: Runtime binding of license management capability side effects
  description: Declares which concrete host implementations are used to satisfy capability pipelines during license management execution.
  storage_structure: ai_governance::STRUCTURE_AGENT_GOVERNANCE_STORAGE_V0

  bindings:
    capability_side_effects::CS_REGISTRY_V0:
      policy:
        path: "{{module_data_root}}/ai_governance/ai_licensing/license_registry.json"

    capability_side_effects::CS_APPENDONLY_JSONL_V0:
      policy: {}

extensions:
  notes:
    - This artifact performs no discovery and no inference.
    - All capability runtimes must be explicitly bound.
    - Storage paths are resolved via template parameters.
    - Changing bindings does not require regenerating workflows or capability contracts.
```
