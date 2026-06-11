# RB_AGENT_ADMISSION_BINDINGS_V0

## Header (Mandatory)

- **Artifact Code:** RB_AGENT_ADMISSION_BINDINGS_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0, CS_REGISTRY_V0, CS_APPENDONLY_JSONL_V0, STRUCTURE_AGENT_ADMISSION_STORAGE_V0

---

## 1. Purpose

Bind capability side effects to concrete host implementations for agent admission workflow execution.

---

## 2. Rationale

Runtime bindings provide environment-specific execution wiring:
- Maps CS artifacts to host classes
- Configures storage paths via parameters
- Keeps protocol artifacts environment-agnostic
- GOVERNANCE_ACTIONS path is scoped to agent_admission — separate from agent_governance
- CS_APPENDONLY_JSONL_V0 uses entity-based policy: entity store path resolved from STRUCTURE at runtime

---

## 3. Bindings

| CS Artifact | Host | Purpose |
|-------------|------|---------|
| CS_MUTABLE_JSON_V0 | MutableJsonRuntime | Read-only license fact feed (LICENSE_FACTS) |
| CS_REGISTRY_V0 | RegistryRuntime | Governance action registry (GOVERNANCE_ACTIONS) |
| CS_APPENDONLY_JSONL_V0 | AppendOnlyJsonlRuntime | Immutable admission audit trail (GOVERNANCE_AUDIT) |

---

## 4. Parameters

| Parameter | Description |
|-----------|-------------|
| module_data_root | Base path for module runtime data (resolved from env_facts) |

---

## Machine

```yaml
rb_code: RB_AGENT_ADMISSION_BINDINGS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

parameters:
  - module_data_root

core:
  summary: Runtime bindings for agent admission workflow
  storage_structure: ai_governance::STRUCTURE_AGENT_ADMISSION_STORAGE_V0

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
        path: "{{module_data_root}}/ai_governance/agent_admission/governance_actions.json"
        strict: true

    capability_side_effects::CS_APPENDONLY_JSONL_V0:
      policy: {}

extensions:
  notes:
    - CS_MUTABLE_JSON_V0 (license_facts.json) is READ-ONLY — agent_admission may not mutate license facts
    - GOVERNANCE_ACTIONS path is scoped to agent_admission — separate from agent_governance
```
