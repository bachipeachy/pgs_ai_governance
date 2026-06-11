# Agent Admission Testbed

## Business Process

An autonomous AI agent proposes tool actions on behalf of a human user. Before any tool
executes, the platform must answer five sequential questions:

1. **Is the request well-formed?** — Normalize the request and generate a deterministic
   intent hash for audit correlation.
2. **Is the tool declared?** — Only tools in the closed agent tool registry may be proposed.
   Anything else is structurally absent — not filtered, absent.
3. **Is the user licensed?** — Look up the user's license record. No active license means
   no authority, regardless of which tool was requested.
4. **Does the license cover this tool?** — Each tier grants a closed set of agent tools.
   Standard tier: web_search and read_file. Enterprise tier adds write_file.
5. **Are the parameters valid?** — Tool-specific parameter constraints are enforced
   declaratively before the action is admitted.

Every outcome — authorized or denied — produces an immutable audit record
(`governance_audit.jsonl`). Authorized actions are also registered in
`governance_actions.json` for idempotency tracking.

### License Tiers and Agent Tool Surface

| Tier         | Allowed Agent Tools                          |
|--------------|----------------------------------------------|
| `none`       | *(no tools — UNAUTHORIZED_ACTOR)*            |
| `standard`   | `web_search`, `read_file`                    |
| `enterprise` | `web_search`, `read_file`, `write_file`      |

`write_file` requires enterprise tier — it is a higher-trust operation (filesystem mutation).

### Workflow: `WF_GOVERN_AGENT_ADMISSION_V0`

```
Request
  → Normalize (intent hash)
  → Check agent tool declared  — VIOLATION → Audit: UNDECLARED_TOOL
  → Resolve license tier       — NOT_FOUND / VIOLATION → Audit: UNAUTHORIZED_ACTOR
  → Bind license to tools      — VIOLATION → Audit: UNAUTHORIZED_TOOL
  → Validate parameters        — VIOLATION → Audit: PARAMETER_VIOLATION
  → Record governed action     → EXIT_SUCCESS
```

---

## Setup

### One-time: seed data

`license_facts.json` holds the user → license mapping. It is shared with `agent_governance`
and lives at `$PGS_DATA_ROOT/ai_governance/ai_licensing/license_facts.json`.

If you have already run the `agent_governance` testbed, this file is already in place.
If not, bootstrap it from the workspace seeds:

```bash
mkdir -p "$PGS_DATA_ROOT/ai_governance/ai_licensing"
cp "$PGS_WORKSPACE/seeds/ai_governance/ai_licensing/license_facts.json" \
   "$PGS_DATA_ROOT/ai_governance/ai_licensing/license_facts.json"
```

### Seed users

| User ID        | License Status | Tier         |
|----------------|----------------|--------------|
| `EMP_STD_001`  | active         | standard     |
| `EMP_ENT_001`  | active         | enterprise   |
| `EMP_NONE_001` | *(not in file)*| none         |

---

## Running a Scenario

```bash
PGS_DATA_ROOT=/abs/path/to/pgs_workspace/data
PGS_WORKSPACE=/abs/path/to/pgs_workspace

pgs_runtime run \
  --wf ai_governance::WF_GOVERN_AGENT_ADMISSION_V0 \
  --payload <path-to-payload.json> \
  --data-root "$PGS_DATA_ROOT" \
  --workspace "$PGS_WORKSPACE"
```

To inspect the admission audit trail after running:

```bash
cat "$PGS_DATA_ROOT/ai_governance/agent_admission/governance_audit.jsonl" | python3 -c "
import sys, json
for i, line in enumerate(sys.stdin, 1):
    r = json.loads(line)['record']
    print(f'{i:02d}. {r[\"decision\"]:10} | {r[\"event_code\"]} | tool={r[\"tool_name\"]} | denial={r.get(\"denial_reason\",\"-\")}')
"
```

---

## Scenarios

### 01 — Authorized: standard user, read-only tool, valid parameters

**Payload:** `test_payloads/01_web_search_authorized.json`

```json
{ "tool_name": "web_search", "parameters": { "query": "PGS governance" },
  "requesting_user_id": "EMP_STD_001", "domain_context": "agent_admission" }
```

**Expected decision:** `AUTHORIZED`
**Audit event:** `EV_AGENT_ACTION_AUTHORIZED_V0`
**Path:** Full happy path — all five gates pass. web_search is in the standard tier surface;
query field is non-null.

---

### 02 — Denied: no license record

**Payload:** `test_payloads/02_no_license.json`

```json
{ "tool_name": "web_search", "parameters": { "query": "test" },
  "requesting_user_id": "EMP_NONE_001", "domain_context": "agent_admission" }
```

**Expected decision:** `DENIED` — `UNAUTHORIZED_ACTOR`
**Path:** Normalize → CheckTool (web_search declared, pass) → ResolveLicense **NOT_FOUND**
→ Audit denial. `EMP_NONE_001` is absent from `license_facts.json`.

---

### 03 — Denied: standard user requests write_file

**Payload:** `test_payloads/03_standard_requests_write.json`

```json
{ "tool_name": "write_file", "parameters": { "path": "out.txt", "content": "hello" },
  "requesting_user_id": "EMP_STD_001", "domain_context": "agent_admission" }
```

**Expected decision:** `DENIED` — `UNAUTHORIZED_TOOL`
**Path:** ResolveLicense (standard tier) → BindLicense: write_file not in
`["web_search", "read_file"]` → **VIOLATION** → Audit denial.

---

### 04 — Authorized: enterprise user, write_file, valid parameters

**Payload:** `test_payloads/04_enterprise_write_authorized.json`

```json
{ "tool_name": "write_file", "parameters": { "path": "out.txt", "content": "hello" },
  "requesting_user_id": "EMP_ENT_001", "domain_context": "agent_admission" }
```

**Expected decision:** `AUTHORIZED`
**Audit event:** `EV_AGENT_ACTION_AUTHORIZED_V0`
**Path:** Enterprise tier includes write_file — all gates pass. Both path and content
fields are non-null.

---

### 05 — Denied: tool not in agent registry

**Payload:** `test_payloads/05_undeclared_tool.json`

```json
{ "tool_name": "execute_shell", "parameters": { "command": "ls" },
  "requesting_user_id": "EMP_STD_001", "domain_context": "agent_admission" }
```

**Expected decision:** `DENIED` — `UNDECLARED_TOOL`
**Path:** Normalize → CheckTool: `execute_shell` absent from `[web_search, read_file, write_file]`
→ **VIOLATION** → Audit denial. The workflow exits at the second gate; license is never
consulted.

---

### 06 — Denied: parameter rule violation (missing required field)

**Payload:** `test_payloads/06_parameter_violation.json`

```json
{ "tool_name": "write_file", "parameters": { "path": "out.txt" },
  "requesting_user_id": "EMP_ENT_001", "domain_context": "agent_admission" }
```

**Expected decision:** `DENIED` — `PARAMETER_VIOLATION`
**Path:** All four earlier gates pass (write_file declared; enterprise licensed and authorized).
ValidateParameters: `content` field absent (not_null constraint) → **VIOLATION** → Audit denial.

---

## Summary Table

| # | User           | Tool          | Parameters                          | Decision   | Denial Reason       |
|---|----------------|---------------|-------------------------------------|------------|---------------------|
| 01 | EMP_STD_001   | web_search    | query="PGS governance"              | AUTHORIZED | —                   |
| 02 | EMP_NONE_001  | web_search    | query="test"                        | DENIED     | UNAUTHORIZED_ACTOR  |
| 03 | EMP_STD_001   | write_file    | path=out.txt, content=hello         | DENIED     | UNAUTHORIZED_TOOL   |
| 04 | EMP_ENT_001   | write_file    | path=out.txt, content=hello         | AUTHORIZED | —                   |
| 05 | EMP_STD_001   | execute_shell | command=ls                          | DENIED     | UNDECLARED_TOOL     |
| 06 | EMP_ENT_001   | write_file    | path=out.txt (content absent)       | DENIED     | PARAMETER_VIOLATION |

---

## Determinism Check

Scenario 01 is the determinism reference scenario. Running it twice must produce the same
TRACE_ID (identical inputs → identical hash → same trace path):

```bash
# Run twice
pgs_runtime run --wf ai_governance::WF_GOVERN_AGENT_ADMISSION_V0 \
  --payload test_payloads/01_web_search_authorized.json \
  --data-root "$PGS_DATA_ROOT" --workspace "$PGS_WORKSPACE"

pgs_runtime run --wf ai_governance::WF_GOVERN_AGENT_ADMISSION_V0 \
  --payload test_payloads/01_web_search_authorized.json \
  --data-root "$PGS_DATA_ROOT" --workspace "$PGS_WORKSPACE"

# Verify: both runs produce the same trace directory
ls "$PGS_WORKSPACE/traces/ai_governance/agent_admission/"
```

The ALREADY_EXISTS outcome on CC_RECORD_GOVERNED_ACTION_V0 is the idempotency signal —
the second run must exit via EXIT_SUCCESS (routes through ALREADY_EXISTS → EXIT_SUCCESS).

---

## Debugging Notes

### Artifacts to inspect

| Question | Artifact |
|---|---|
| What agent tools are declared? | `CC_CHECK_AGENT_TOOL_DECLARED_V0` pipeline `allowed_set` |
| What tools does a tier get? | `CC_BIND_AGENT_LICENSE_TO_TOOL_SURFACE_V0` step 1 `map` |
| What parameter rules apply? | `CC_VALIDATE_AGENT_TOOL_PARAMETERS_V0` step 1 `map` |
| What happened at runtime? | `$PGS_DATA_ROOT/ai_governance/agent_admission/governance_audit.jsonl` |
| Full execution trace? | `$PGS_WORKSPACE/traces/ai_governance/agent_admission/` |

### Two classes of protocol bug

**Routing bugs** (visible in graph topology): wrong `next` condition on a WF node, or
wrong `on_result` key in a CC step. The compiled graph shows these — every edge is an
`on_result` condition.

**Binding bugs** (invisible in graph topology): wrong `$.path` expression in a CC step's
`inputs` or `outputs` block. These cause the runtime to silently resolve `None` and either
misroute or crash. Trace each `$.` path against the compiled CC artifact in
`protocol_snapshot/artifacts/capability_contracts/`.
