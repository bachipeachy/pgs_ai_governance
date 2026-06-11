# CC_VALIDATE_AGENT_TOOL_PARAMETERS_V0

## Header (Mandatory)

- **Artifact Code:** CC_VALIDATE_AGENT_TOOL_PARAMETERS_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_LOOKUP_V0, CT_PURE_VALIDATE_PARAMETER_RULES_V0

---

## 1. Intent

Enforce declared parameter constraints for authorized agent tools before the action is admitted.

---

## 2. Rationale

Parameter validation is the fifth governance gate in the admission workflow:
- Each agent tool declares required fields that must be present and non-null
- Constraints are per-tool: web_search requires query; read_file requires path; write_file requires path and content
- Cannot reuse CC_VALIDATE_TOOL_PARAMETERS_V0 — that CC declares constraints for licensing operation fields
- Two-step pipeline: lookup per-tool rules, then validate submitted parameters against them
- Phase 1 constraints are required-field-only; path traversal constraints (.. restriction) are deferred to V1

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_LOOKUP_V0 | CT | LOOKUP |
| 2 | CT_PURE_VALIDATE_PARAMETER_RULES_V0 | CT | VALIDATE_PARAMETER_RULES |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tool_name | string | true | Requested tool identifier (used to look up rule set) |
| parameters | object | true | Tool-specific parameter key-value map submitted by the agent |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| rules | array | Parameter rule set for the requested tool |
| validation_result | object | Detailed result from parameter rules validation |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | All declared parameter constraints satisfied |
| VIOLATION | One or more required parameters are absent or null |

---

## Machine

```yaml
cc_code: CC_VALIDATE_AGENT_TOOL_PARAMETERS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Enforce declared parameter constraints for authorized agent tools

  inputs:
    tool_name:
      type: string
      required: true
    parameters:
      type: object
      required: true

  outputs:
    rules:
      type: array
    validation_result:
      type: object

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]
    on_input_failure: VIOLATION

  pipeline:
    - step: lookup_parameter_rules
      transform: capability_transforms::CT_PURE_LOOKUP_V0
      inputs:
        key: $.inputs.tool_name
        map:
          web_search:
            - field: query
              op: not_null
          read_file:
            - field: path
              op: not_null
          write_file:
            - field: path
              op: not_null
            - field: content
              op: not_null
      outputs:
        rules: $.capability_result.result
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: validate_parameters
      transform: capability_transforms::CT_PURE_VALIDATE_PARAMETER_RULES_V0
      inputs:
        parameters: $.inputs.parameters
        rules: $.results.lookup_parameter_rules.rules
      outputs:
        validation_result: $.capability_result.value
        rules: $.results.lookup_parameter_rules.rules
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

extensions:
  description: Phase 1 constraints — required fields only; path traversal constraints deferred to V1
```
