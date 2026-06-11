# RB_AGENT_GOVERNANCE_BINDINGS_V0

## Header (Mandatory)

- **Artifact Code:** RB_AGENT_GOVERNANCE_BINDINGS_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0, CS_REGISTRY_V0, CS_APPENDONLY_JSONL_V0

---

## 1. Purpose

Bind capability side effects to concrete host implementations for agent governance execution.

---

## 2. Rationale

Runtime bindings provide environment-specific execution wiring:
- Maps CS artifacts to host classes
- Configures storage paths via parameters
- Keeps protocol artifacts environment-agnostic

---

## 3. Bindings

| CS Artifact | Host | Purpose |
|-------------|------|---------|
| CS_MUTABLE_JSON_V0 | MutableJsonRuntime | Read-only license fact feed (immutable external facts) |
| CS_REGISTRY_V0 | RegistryRuntime | Governance action registry |
| CS_APPENDONLY_JSONL_V0 | AppendOnlyJsonlRuntime | Immutable governance audit trail |

---

## 4. Parameters

| Parameter | Description |
|-----------|-------------|
| module_data_root | Base path for module runtime data (resolved from env_facts) |

---

## Machine

```yaml
rb_code: RB_AGENT_GOVERNANCE_BINDINGS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

parameters:
  - module_data_root

core:
  summary: Runtime binding of agent governance capability side effects
  description: Declares which concrete host implementations satisfy capability pipelines during agent governance execution.
  storage_structure: ai_governance::STRUCTURE_AGENT_GOVERNANCE_STORAGE_V0

  bindings:
    capability_side_effects::CS_MUTABLE_JSON_V0:
      type: CS
      host: MutableJsonRuntime
      operation: READ_WRITE
      policy: {}

    capability_side_effects::CS_REGISTRY_V0:
      type: CS
      host: RegistryRuntime
      operation: READ_WRITE
      policy:
        path: "{{module_data_root}}/ai_governance/agent_governance/governance_actions.json"
        strict: true

    capability_side_effects::CS_APPENDONLY_JSONL_V0:
      policy: {}

extensions:
  notes:
    - CS_MUTABLE_JSON_V0 (license_facts.json) is READ-ONLY — agent governance may not mutate license facts
    - All capability runtimes must be explicitly bound
    - Storage paths are resolved via template parameters
```
