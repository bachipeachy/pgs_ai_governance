# STRUCTURE_AGENT_ADMISSION_STORAGE_V0

## Header (Mandatory)

- **Artifact Code:** STRUCTURE_AGENT_ADMISSION_STORAGE_V0
- **Artifact Kind:** structure
- **Governed By:** CONSTITUTION_STRUCTURE_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE

---

## 1. Intent

Declare storage topology for the agent admission subdomain. Maps entity types to storage implementations and paths.

---

## 2. Rationale

Storage paths are a governance concern, not a runtime implementation detail. This STRUCTURE artifact:
- Centralizes storage topology for agent_admission (single source of truth)
- Decouples CC artifacts from filesystem layout
- Enforces entity-level isolation — GOVERNANCE_ACTIONS and GOVERNANCE_AUDIT are scoped to agent_admission; LICENSE_FACTS is read-only from ai_licensing

---

## 3. Storage Model

**Principle:** One store per domain entity type.

**Entity Types:**
- LICENSE_FACTS: Read-only license tier and status feed (shared with agent_governance — read-only access only)
- GOVERNANCE_ACTIONS: Mutable registry of authorized agent admission actions (idempotency tracking)
- GOVERNANCE_AUDIT: Append-only audit trail for all admission authorization and denial decisions

---

## Machine

```yaml
structure_code: STRUCTURE_AGENT_ADMISSION_STORAGE_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

core:
  summary: Agent admission subdomain storage topology
  layer: DOMAINS
  domain: ai_governance

  storage_roots:
    base_path: "{{module_data_root}}"

  entity_stores:
    LICENSE_FACTS:
      description: "Read-only license tier and status fact feed (shared with agent_governance)"
      path: "ai_governance/ai_licensing/license_facts.json"
    GOVERNANCE_ACTIONS:
      description: "Registry of authorized agent admission actions (idempotency tracking)"
      path: "ai_governance/agent_admission/governance_actions.json"
    GOVERNANCE_AUDIT:
      description: "Append-only audit trail for agent admission authorization and denial decisions"
      path: "ai_governance/agent_admission/governance_audit.jsonl"

  isolation:
    rules:
      - "LICENSE_FACTS is read-only — agent_admission may not mutate license facts"
      - "GOVERNANCE_AUDIT is append-only — admission audit records are immutable"
      - "GOVERNANCE_ACTIONS is scoped to agent_admission — no cross-subdomain writes"
```
