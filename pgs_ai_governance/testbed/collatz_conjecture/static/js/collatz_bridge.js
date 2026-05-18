/**
 * collatz_bridge.js — Thin JS bridge for PGS Collatz Conjecture demo.
 *
 * Zero schema awareness. Zero workflow branching. Zero validation.
 * PGS handles all business logic. This bridge only:
 * - Builds a single-number payload and POSTs to /api/run
 * - Renders the Collatz sequence chain from the canonical response envelope
 */

// Maximum sequence steps to render inline before truncating for performance
const MAX_DISPLAY_STEPS = 300;

function setPick(n) {
    document.getElementById('seed_number').value = n;
    const resultDiv = document.getElementById('result');
    resultDiv.className = 'result-panel';
    resultDiv.style.display = 'none';
    resultDiv.innerHTML = '';
}

async function submitCollatz() {
    const resultDiv = document.getElementById('result');
    const form = document.getElementById('collatz-form');
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    const workflowCode = form.getAttribute('data-workflow');

    const rawValue = document.getElementById('seed_number').value.trim();
    const n = parseInt(rawValue, 10);

    if (!rawValue || isNaN(n) || n < 1 || n > 999999) {
        renderError(resultDiv, 'Enter a whole number between 1 and 999,999.');
        return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Computing...';

    resultDiv.className = 'result-panel';
    resultDiv.style.display = 'none';
    resultDiv.innerHTML = '';

    try {
        const response = await fetch('/api/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                workflow_code: workflowCode,
                payload: { numbers: [n] }
            })
        });

        const result = await response.json();
        renderCollatzResult(resultDiv, result, n);

    } catch (e) {
        renderError(resultDiv, e.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

function renderCollatzResult(el, result, n) {
    const isSuccess = result.status === 'SUCCESS';
    const isRepeat  = result.already_submitted === true;

    el.className = 'result-panel visible ' + (isSuccess ? 'success' : 'error');
    el.style.display = '';

    let html = '';

    if (isRepeat) {
        html += '<span class="status-badge repeat">CACHED</span>';
    } else {
        html += '<span class="status-badge">' + escapeHtml(result.status) + '</span>';
    }

    if (result.trace_id) {
        html += '<div class="result-field"><span class="label">Trace ID</span> '
             +  '<span class="value">' + escapeHtml(result.trace_id) + '</span></div>';
    }
    if (result.duration_ms !== undefined) {
        html += '<div class="result-field"><span class="label">Duration</span> '
             +  '<span class="value">' + result.duration_ms + 'ms</span></div>';
    }
    if (result.exit_reason_code) {
        html += '<div class="result-field"><span class="label">Exit</span> '
             +  '<span class="value">' + escapeHtml(result.exit_reason_code) + '</span></div>';
    }
    if (result.message) {
        html += '<div class="result-field"><span class="label">Message</span> '
             +  '<span class="value">' + escapeHtml(result.message) + '</span></div>';
    }

    // ── Sequence display ──────────────────────────────────────────────
    if (isSuccess) {
        const p = result.result_payload || {};
        const sequences = p.sequences || {};
        const key = String(n);
        const seq = sequences[key];

        if (seq && Array.isArray(seq) && seq.length > 0) {
            const steps = seq.length - 1;   // steps to reach 1
            const peak  = Math.max(...seq);

            html += '<div class="seq-stats">'
                 +  '  <div class="seq-stat"><span class="stat-label">Seed</span><span class="stat-value">' + n + '</span></div>'
                 +  '  <div class="seq-stat"><span class="stat-label">Steps to 1</span><span class="stat-value">' + steps + '</span></div>'
                 +  '  <div class="seq-stat"><span class="stat-label">Peak value</span><span class="stat-value peak">' + peak.toLocaleString() + '</span></div>'
                 +  '</div>';

            html += '<div class="seq-chain-wrap">';
            html += '<div class="seq-chain-label">Sequence</div>';
            html += '<div class="seq-chain">';

            const display = seq.length > MAX_DISPLAY_STEPS ? seq.slice(0, MAX_DISPLAY_STEPS) : seq;
            for (let i = 0; i < display.length; i++) {
                const v = display[i];
                let cls = 'seq-num';
                if (i === 0)                  cls += ' seed';
                else if (v === peak && i > 0) cls += ' peak';
                if (v === 1)                  cls  = 'seq-num one';

                html += '<span class="' + cls + '">' + v.toLocaleString() + '</span>';
                if (i < display.length - 1) {
                    html += '<span class="seq-arrow">&#8594;</span>';
                }
            }
            if (seq.length > MAX_DISPLAY_STEPS) {
                html += '<span class="seq-arrow">&#8594;</span>';
                html += '<span class="seq-truncated">... (' + (seq.length - MAX_DISPLAY_STEPS) + ' more steps) &rarr; 1</span>';
            }

            html += '</div></div>';  // .seq-chain, .seq-chain-wrap
        }
    }

    // Raw JSON (expanded by default)
    html += '<details open style="margin-top:12px;">'
         +  '<summary style="font-size:12px;color:#64748b;cursor:pointer;padding:4px 0;">Raw response</summary>'
         +  '<div class="result-json">' + escapeHtml(JSON.stringify(result, null, 2)) + '</div>'
         +  '</details>';

    el.innerHTML = html;
}

function renderError(el, msg) {
    el.className = 'result-panel visible error';
    el.style.display = '';
    el.innerHTML = '<span class="status-badge">ERROR</span>'
        + '<div class="result-field"><span class="label">Message</span> '
        + '<span class="value">' + escapeHtml(msg) + '</span></div>';
}

function escapeHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}
