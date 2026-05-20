# STRUCTURE_COLLATZ_STORAGE_V0

## Header (Mandatory)

- **Artifact Code:** STRUCTURE_COLLATZ_STORAGE_V0
- **Artifact Kind:** structure
- **Governed By:** CONSTITUTION_STRUCTURE_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE

---

## 1. Intent

Declare storage topology for the Collatz conjecture demonstration domain.
Maps entity types to storage implementations and paths.

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
- COLLATZ_RESULTS: Mutable store for computed sequences and conjecture verdict

---

## Machine

```yaml
structure_code: STRUCTURE_COLLATZ_STORAGE_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

core:
  summary: Collatz conjecture domain storage topology
  description: Maps entity types to storage implementations and paths

  layer: DOMAINS
  domain: ai_governance

  storage_roots:
    base_path: "{{module_data_root}}"
    description: "Root path for all Collatz storage (resolved at runtime)"

  entity_stores:
    COLLATZ_RESULTS:
      description: "Mutable store for Collatz sequences and conjecture verdict (last-write-wins)"
      path: "ai_governance/collatz_conjecture/collatz_results.json"

  resolution:
    description: "Runtime path resolution strategy"
    algorithm: "base_path / entity_stores[entity_type].path"
    example: "{{module_data_root}}/ai_governance/collatz_conjecture/collatz_results.json"

  isolation:
    description: "Entity storage isolation constraints"
    rules:
      - "Each entity type has dedicated storage"
      - "COLLATZ_RESULTS is read-write — idempotent, last-write-wins"
      - "Storage paths resolved via STRUCTURE only"
```
