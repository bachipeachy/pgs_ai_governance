# pgs_ai_governance

**Governance workflows for AI-assisted systems, expressed as executable protocol.**

This repository demonstrates how AI-assisted actions — code generation, deployment, provisioning — can be validated, constrained, and auditable using Protocol-Governed Systems (PGS).

It does not wrap or restrict AI tools directly.  
It defines what actions are allowed, under what conditions, and with what consequences.

Behavior is declared in protocol, executed by runtime, implemented in capabilities, and observed via traces and state.

> **New to PGS?** This is one of the repositories in the Protocol-Governed Systems ecosystem.
> For orientation, architecture overview, and end-to-end execution, start at [pgs_workspace](https://github.com/bachipeachy/pgs_workspace).

---

## The problem this addresses

AI systems introduce two competing forces:

```
Speed    → rapid generation, iteration, and modification
Control  → correctness, safety, and policy compliance
```

Most systems trade one for the other — either slow the AI down with approval gates, or trust it and audit after the fact.

This domain demonstrates a different approach:  
**governance encoded into execution, not applied after the fact.**

---

## Workflows

```
ai_governance::WF_GOVERN_AGENT_ACTION_V0
ai_governance::WF_PROVISION_AI_LICENSING_V0
ai_governance::WF_AUTO_RECLAIM_V0
ai_governance::WF_DENY_PROVISION_V0
```

These workflows:
- validate incoming actions through admission rules (IN_)
- apply policy decisions at named decision points (CC_)
- record all outcomes as immutable events (CS_)

They execute through the same generic runtime used by all PGS domains.

---

## Execution model

Every workflow execution follows this path:

```
IN_ → WF_ → CC_ → (CT_ / CS_) → Trace
```

| Concern | What it does |
|---------|-------------|
| `IN_` Intent | Admission gate — validates payload before anything runs |
| `WF_` Workflow | Execution graph — declares which CCs run and in what order |
| `CC_` Capability Contract | Named DAG node — declares inputs, outputs, and routing outcomes |
| `CT_` Capability Transform | Pure computation — deterministic, no side effects |
| `CS_` Capability Side Effect | Controlled state change — registry write, event append, grant, revoke |
| `RB_` Runtime Binding | Maps declared capabilities to implementations at build time |
| Trace | Append-only execution record — ground truth of what happened |

The runtime traverses this graph exactly as declared. It has no domain knowledge. All governance behavior lives in the compiled snapshot.

---

## Build lifecycle

```
compile → build → run
```

| Phase | What happens | Where |
|-------|-------------|-------|
| **compile** | Source artifacts validated against invariants | `pgs_governance` / `pgs_compiler` |
| **build** | Validated artifacts materialized into a closed snapshot | `pgs_compiler` → `pgs_workspace/protocol_snapshot/` |
| **run** | Runtime reads snapshot and executes | `pgs_workspace` (pgs_runtime CLI) |

The snapshot is sealed at build time. No behavior enters at execution time that was not in the snapshot.

---

## What is being governed

This domain models actions such as:
- provisioning AI capabilities or access
- approving or denying agent requests
- enforcing usage constraints
- reclaiming or revoking access

These are expressed as workflows with explicit outcomes — not conditional logic hidden in code.

---

## How governance works here

**1. Governance is part of execution**

Policies are not checked after an action completes. They are encoded as:

```
IN_  → admission rules (what is allowed to enter)
CC_  → decision points (where routing is determined)
CS_  → enforceable effects (grant, deny, revoke, record)
```

If an admission rule is violated, the workflow does not proceed. No exception handling. No fallback. The graph has no edge for that path.

**2. All decisions are explicit**

Every decision point returns a named outcome:
```
APPROVED
DENIED
VIOLATION
```

These outcomes determine the execution path. There is no implicit policy evaluation, no hidden fallback behavior, no silent acceptance.

**3. Speed is preserved**

AI systems can operate at full speed because governance is precompiled. Decisions are deterministic. No runtime policy interpretation is required.

This avoids the typical pattern:
```
fast generation → slow validation → delayed execution
```

Instead:
```
validated execution → immediate outcome
```

**4. Full auditability**

Every decision produces:
- a trace (complete execution path)
- an event (append-only record — the permanent history)
- a state change (if and only if the action was allowed)

No instrumentation required. Governance is observable by design.

---

## Applying this to AI-assisted coding

This domain suggests a pattern for governing AI coding assistants.

Instead of:
- letting AI tools directly modify systems
- adding ad-hoc validation layers around tool calls
- relying on manual review after generation

You define intent → governed workflow → controlled outcome:

| Action | Governed as |
|--------|-------------|
| "generate and apply a code change" | `WF_VALIDATE_CODE_CHANGE_V0` with scope assertions |
| "deploy this patch" | `WF_APPROVE_DEPLOYMENT_V0` with policy satisfaction check |
| "provision new AI capability" | `WF_PROVISION_AI_LICENSING_V0` with licensing constraints |

AI tools retain their full generative speed. Governance does not slow generation; it constrains execution. Governance is the execution substrate, not a gate in front of it.

---

## Extending governance capabilities

You extend this domain by adding protocol artifacts — no runtime changes required.

**New intents (admission rules):**
```
IN_SUBMIT_CODE_CHANGE_V0
IN_REQUEST_DEPLOYMENT_V0
IN_REQUEST_ELEVATED_ACCESS_V0
```

**New workflows:**
```
WF_VALIDATE_CODE_CHANGE_V0
WF_APPROVE_DEPLOYMENT_V0
WF_ENFORCE_SCOPE_CONSTRAINT_V0
```

**New assertions (compiled constraints):**
```
ASSERT_CODE_CHANGE_WITHIN_SCOPE_V0
ASSERT_DEPLOYMENT_POLICY_COMPLIANT_V0
ASSERT_AGENT_CAPABILITY_LICENSED_V0
```

**New side-effects:**
```
CS_GRANT_ACCESS_V0
CS_REVOKE_ACCESS_V0
CS_RECORD_DECISION_V0
CS_APPEND_AUDIT_LOG_V0
```

---

## What this is not

This repository does not:
- replace or sandbox AI tools
- guarantee correctness of generated code
- solve AI safety at a foundational level

It provides:  
a structured way to control when and how AI-initiated actions are allowed to take effect.

---

## Repo structure

```
pgs_ai_governance/
└── pgs_ai_governance/
    └── testbed/
        ├── agent_governance/  ← payloads for agent action workflows
        ├── ai_licensing/      ← payloads for licensing workflows
        └── static/            ← browser UI client
```

---

## Where this fits in the system

| Repo | Role |
|------|------|
| `pgs_governance` + `pgs_compiler` | Define and compile governance artifacts |
| `pgs_runtime` | Executes governance workflows |
| `pgs_capabilities` | Implements CT/CS effects |
| `pgs_blockchain` | Example: a full system domain using PGS |
| **`pgs_ai_governance` ← here** | **Governance domain** |
| `pgs_change_mgmt` | Governed SDLC — Change Request to Authoring Mandate (new in v0.5.0) |
| `pgs_workspace` | Entry point — run and observe |

---

## Research context

> *"Extensibility by declaration, not refactor."*

Applied to governance.

This domain shows how policies can be compiled, decisions can be deterministic, and outcomes can be fully auditable — without embedding control logic across application code.

The implication: as AI-assisted systems scale in speed and scope, governance scales with them — because it is compiled into the execution substrate, not layered on top of it.

---

## Core idea

Actions are not prevented or allowed by convention.  
They are routed through governed execution paths.

---

## Final note

If governance requires inserting conditional logic into application code, the model has been bypassed.  
Define a new workflow. Compile it. The system governs it.
---

## License

Apache-2.0. See LICENSE and NOTICE for details.
