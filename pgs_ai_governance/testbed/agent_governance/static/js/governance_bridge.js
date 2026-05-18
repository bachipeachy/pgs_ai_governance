/**
 * governance_bridge.js — Thin JS bridge for PGS agent governance demo.
 *
 * Zero schema awareness. Zero workflow branching. Zero validation.
 * PGS handles all business logic. This bridge only:
 * - Harvests form inputs into JSON
 * - POSTs to /api/run
 * - Renders the canonical response envelope
 * - Provides quick-scenario auto-fill (embedded data, no server fetch)
 */

// ── Quick Scenario Data ──────────────────────────────────────────────

const SCENARIOS = {
    standard_happy: {
        tool_name: "PROVISION_STANDARD_LICENSE",
        requesting_user_id: "EMP_STD_001",
        domain_context: "ai_governance",
        request_id: "REQ_DEMO_001",
        parameters: { tier: "standard", quantity: 50 }
    },
    enterprise_happy: {
        tool_name: "PROVISION_PREMIUM_LICENSE",
        requesting_user_id: "EMP_ENT_001",
        domain_context: "ai_governance",
        request_id: "REQ_DEMO_002",
        parameters: { tier: "premium", quantity: 25 }
    },
    unknown_user: {
        tool_name: "PROVISION_STANDARD_LICENSE",
        requesting_user_id: "ROGUE_AGENT_99",
        domain_context: "ai_governance",
        request_id: "REQ_DEMO_003",
        parameters: { tier: "standard", quantity: 10 }
    },
    tier_escalation: {
        tool_name: "PROVISION_PREMIUM_LICENSE",
        requesting_user_id: "EMP_STD_001",
        domain_context: "ai_governance",
        request_id: "REQ_DEMO_004",
        parameters: { tier: "premium", quantity: 10 }
    },
    undeclared_tool: {
        tool_name: "DELETE_DATABASE",
        requesting_user_id: "EMP_STD_001",
        domain_context: "ai_governance",
        request_id: "REQ_DEMO_005",
        parameters: {}
    },
    shell_injection: {
        tool_name: "EXECUTE_SHELL_COMMAND",
        requesting_user_id: "EMP_ENT_001",
        domain_context: "system",
        request_id: "REQ_DEMO_006",
        parameters: { command: "rm -rf /" }
    },
    parameter_violation: {
        tool_name: "PROVISION_STANDARD_LICENSE",
        requesting_user_id: "EMP_STD_001",
        domain_context: "ai_governance",
        request_id: "REQ_DEMO_007",
        parameters: { tier: "standard", quantity: 200 }
    }
};

function loadScenario(name) {
    const s = SCENARIOS[name];
    if (!s) return;

    document.getElementById('tool_name').value = s.tool_name;
    document.getElementById('requesting_user_id').value = s.requesting_user_id;
    document.getElementById('domain_context').value = s.domain_context;
    document.getElementById('request_id').value = s.request_id;
    document.getElementById('parameters').value = JSON.stringify(s.parameters, null, 2);

    // Clear previous result
    const resultDiv = document.getElementById('result');
    resultDiv.className = 'result-panel';
    resultDiv.style.display = 'none';
    resultDiv.innerHTML = '';
}

// ── Form Submission ──────────────────────────────────────────────────

async function submitGovernanceForm() {
    const resultDiv = document.getElementById('result');
    const form = document.getElementById('govern-form');
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;

    const workflowCode = form.getAttribute('data-workflow');
    if (!workflowCode) {
        renderError(resultDiv, 'Form is missing data-workflow attribute.');
        return;
    }

    // Build payload from free-text fields
    const toolName = document.getElementById('tool_name').value.trim();
    const userId = document.getElementById('requesting_user_id').value.trim();
    const domain = document.getElementById('domain_context').value.trim();
    const requestId = document.getElementById('request_id').value.trim();
    const paramsText = document.getElementById('parameters').value.trim();

    if (!toolName || !userId) {
        renderError(resultDiv, 'Tool Name and Requesting User are required.');
        return;
    }

    // Parse parameters JSON
    let parameters = {};
    if (paramsText) {
        try {
            parameters = JSON.parse(paramsText);
        } catch (e) {
            renderError(resultDiv, 'Invalid JSON in Parameters field: ' + e.message);
            return;
        }
    }

    // Coerce numeric strings in parameters to numbers
    for (const key in parameters) {
        if (typeof parameters[key] === 'string' && parameters[key] !== '' && !isNaN(parameters[key])) {
            parameters[key] = Number(parameters[key]);
        }
    }

    const payload = {
        tool_name: toolName,
        requesting_user_id: userId,
        domain_context: domain,
        request_id: requestId || ('REQ_' + Date.now()),
        parameters: parameters
    };

    submitBtn.disabled = true;
    submitBtn.textContent = 'Executing...';

    // Clear previous result
    resultDiv.className = 'result-panel';
    resultDiv.style.display = 'none';
    resultDiv.innerHTML = '';

    try {
        const response = await fetch('/api/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                workflow_code: workflowCode,
                payload: payload
            })
        });

        const result = await response.json();
        renderResult(resultDiv, result);

    } catch (e) {
        renderError(resultDiv, e.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

// ── Legacy data-field harvester (for forms that use data-field attributes) ──

async function submitWorkflow(formId) {
    const form = document.getElementById(formId);
    const resultDiv = document.getElementById('result');
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;

    const payload = {};
    form.querySelectorAll('[data-field]').forEach(function(input) {
        const value = input.value;
        if (value !== '') {
            setDeep(payload, input.getAttribute('data-field'), value);
        }
    });

    const workflowCode = form.getAttribute('data-workflow');

    submitBtn.disabled = true;
    submitBtn.textContent = 'Executing...';

    resultDiv.className = 'result-panel';
    resultDiv.style.display = 'none';
    resultDiv.innerHTML = '';

    try {
        const response = await fetch('/api/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                workflow_code: workflowCode,
                payload: payload
            })
        });

        const result = await response.json();
        renderResult(resultDiv, result);

    } catch (e) {
        renderError(resultDiv, e.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

// ── Result Rendering ─────────────────────────────────────────────────

function renderResult(el, result) {
    const isSuccess = result.status === 'SUCCESS';
    const isRepeat = result.already_submitted === true;
    el.className = 'result-panel visible ' + (isRepeat ? 'already-submitted' : (isSuccess ? 'success' : 'error'));
    el.style.display = '';

    let html = '';
    if (isRepeat) {
        html += '<span class="status-badge repeat">ALREADY SUBMITTED</span>';
        html += '<div class="result-field"><span class="label">Note</span> '
             +  '<span class="value">This request was already processed. Persistent data is unchanged.</span></div>';
    } else {
        html += '<span class="status-badge">' + result.status + '</span>';
    }

    if (result.trace_id) {
        html += '<div class="result-field"><span class="label">Trace ID</span> '
             +  '<span class="value">' + result.trace_id + '</span></div>';
    }
    if (result.duration_ms !== undefined) {
        html += '<div class="result-field"><span class="label">Duration</span> '
             +  '<span class="value">' + result.duration_ms + 'ms</span></div>';
    }
    if (result.workflow_code) {
        html += '<div class="result-field"><span class="label">Workflow</span> '
             +  '<span class="value">' + result.workflow_code + '</span></div>';
    }
    if (result.exit_reason_code) {
        html += '<div class="result-field"><span class="label">Exit Reason</span> '
             +  '<span class="value">' + result.exit_reason_code + '</span></div>';
    }
    if (result.message) {
        html += '<div class="result-field"><span class="label">Message</span> '
             +  '<span class="value">' + result.message + '</span></div>';
    }

    // Show key payload highlights for agent governance
    const p = result.result_payload || {};
    if (p.action_id) {
        html += '<div class="result-field"><span class="label">Action ID</span> '
             +  '<span class="value">' + p.action_id + '</span></div>';
    }
    if (p.intent_hash) {
        html += '<div class="result-field"><span class="label">Intent Hash</span> '
             +  '<span class="value">' + p.intent_hash + '</span></div>';
    }
    if (p.license_tier) {
        html += '<div class="result-field"><span class="label">License Tier</span> '
             +  '<span class="value">' + p.license_tier + '</span></div>';
    }
    if (p.is_authorized !== undefined) {
        html += '<div class="result-field"><span class="label">Authorized</span> '
             +  '<span class="value">' + p.is_authorized + '</span></div>';
    }
    if (p.denial_reason) {
        html += '<div class="result-field"><span class="label">Denial Reason</span> '
             +  '<span class="value">' + p.denial_reason + '</span></div>';
    }

    html += '<div class="result-json">' + escapeHtml(JSON.stringify(result, null, 2)) + '</div>';
    el.innerHTML = html;
}

function renderError(el, msg) {
    el.className = 'result-panel visible error';
    el.style.display = '';
    el.innerHTML = '<span class="status-badge">TRANSPORT ERROR</span>'
        + '<div class="result-field"><span class="label">Message</span> '
        + '<span class="value">' + escapeHtml(msg) + '</span></div>';
}

function setDeep(obj, path, value) {
    const parts = path.split('.');
    let current = obj;
    for (let i = 0; i < parts.length - 1; i++) {
        if (!current[parts[i]]) current[parts[i]] = {};
        current = current[parts[i]];
    }
    current[parts[parts.length - 1]] = value;
}

function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
