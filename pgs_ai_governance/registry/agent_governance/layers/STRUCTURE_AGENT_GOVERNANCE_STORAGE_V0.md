# STRUCTURE_AGENT_GOVERNANCE_STORAGE_V0

## Header (Mandatory)

- **Artifact Code:** STRUCTURE_AGENT_GOVERNANCE_STORAGE_V0
- **Artifact Kind:** structure
- **Governed By:** CONSTITUTION_STRUCTURE_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE

---

## 1. Intent

Declare storage topology for agent governance domain entities. Maps entity types to storage implementations and paths.

---

## 2. Rationale

Storage paths are a governance concern, not a runtime implementation detail. This STRUCTURE artifact:
- Centralizes storage topology (single source of truth)
- Decouples CC artifacts from filesystem layout
- Enforces entity-level isolation

---

## 3. Storage Model

**Principle:** One store per domain entity type.

**Entity Types:**
- LICENSE_FACTS: Read-only license tier and status feed

---

## Machine

```yaml
structure_code: STRUCTURE_AGENT_GOVERNANCE_STORAGE_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

core:
  summary: Agent governance domain storage topology
  description: Maps entity types to storage implementations and paths

  layer: DOMAINS
  domain: ai_governance

  storage_roots:
    base_path: "{{module_data_root}}"
    description: "Root path for all agent governance storage (resolved at runtime)"

  entity_stores:
    LICENSE_FACTS:
      description: "Read-only license tier and status fact feed (user_id → license record)"
      path: "license_facts.json"

  resolution:
    description: "Runtime path resolution strategy"
    algorithm: "base_path / entity_stores[entity_type].path"
    example: "{{module_data_root}}/license_facts.json"

  isolation:
    description: "Entity storage isolation constraints"
    rules:
      - "Each entity type has dedicated storage"
      - "LICENSE_FACTS is read-only — agent governance may not mutate license facts"
      - "Storage paths resolved via STRUCTURE only"
```
