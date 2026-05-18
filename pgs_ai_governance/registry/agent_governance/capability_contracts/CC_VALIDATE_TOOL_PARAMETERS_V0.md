# CC_VALIDATE_TOOL_PARAMETERS_V0

## Header (Mandatory)

- **Artifact Code:** CC_VALIDATE_TOOL_PARAMETERS_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_LOOKUP_V0, CT_PURE_VALIDATE_PARAMETER_RULES_V0

---

## 1. Intent

Enforce declared parameter constraints for the authorized tool.

---

## 2. Rationale

Parameter validation is the fifth governance gate:
- Each tool declares parameter constraints in governance
- Constraints are evaluated by a generic CT — not embedded in tool code
- Enforces Invariant I-A4 (Parameter-Bound Execution)

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
| tool_name | string | true | Authorized tool identifier |
| parameters | object | true | Tool-specific parameter key-value map |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| rules | array | Parameter constraint rules for the tool |
| validation_result | object | Validation outcome |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | All parameter constraints satisfied |
| VIOLATION | One or more parameter constraints failed |

---

## Machine

```yaml
cc_code: CC_VALIDATE_TOOL_PARAMETERS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Enforce declared parameter constraints for authorized tool

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
          READ_RECORD:
            - field: record_type
              op: in
              allowed:
                - license_pool
                - user_profile
            - field: id
              op: not_null
          PROVISION_STANDARD_LICENSE:
            - field: tier
              op: eq
              value: standard
            - field: quantity
              op: lte
              value: 100
          PROVISION_PREMIUM_LICENSE:
            - field: tier
              op: eq
              value: premium
            - field: quantity
              op: lte
              value: 50
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
  description: Evaluates declarative parameter constraints — policy in governance, evaluation in generic CT
```
