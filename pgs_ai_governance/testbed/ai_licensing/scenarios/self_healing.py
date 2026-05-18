"""
self_healing.py — Scenario: Protocol self-heals after training completion.

Narrative:
  An employee requests an AI license but is denied (training incomplete).
  Three days later, the employee completes training.
  The protocol detects the prerequisite is now satisfied and auto-provisions.
  No human intervention required — the system self-heals.

Timeline:
  T+0h:  Employee registered
  T+1h:  License cap established
  T+3h:  Employee requests AI license
  T+3h:  Protocol denies — training incomplete
  T+3d:  Employee completes AI safety training
  T+3d:  Protocol auto-provisions license (self-healing)
"""


import argparse
from pathlib import Path

from pgs_ai_governance.testbed.ai_licensing.scenarios.base import FactStream


def generate(seed: int = 42) -> FactStream:
    """Generate self-healing provision scenario."""
    stream = FactStream(seed=seed)

    # T+0: Employee onboarding
    employee = stream.generate_employee()
    stream.emit_ev_employee_registered(employee)

    # T+1h: IT configures license cap
    stream.advance_time(hours=1)
    stream.emit_ev_license_cap_set(cap=10)

    # T+3h: Employee requests license (premature)
    stream.advance_time(hours=2)
    stream.emit_in_provision_ai_license(employee["employee_id"])

    # T+3h: Denied — training incomplete
    stream.emit_ev_provision_denied(
        employee_id=employee["employee_id"],
        reason_code="TRAINING_INCOMPLETE"
    )

    # T+3d: Employee completes training (3 days later)
    stream.advance_time(days=3)
    stream.emit_ev_training_completed(employee["employee_id"])

    # T+3d: Protocol detects prerequisite satisfied, auto-provisions
    # This is the self-healing moment
    license_id = f"lic-{employee['employee_id'].split('-')[1]}"
    stream.emit_ev_license_provisioned(
        employee_id=employee["employee_id"],
        license_id=license_id
    )

    return stream


def main():
    parser = argparse.ArgumentParser(description="Generate self_healing scenario")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent.parent / "generated" / "self_healing.jsonl",
    )
    args = parser.parse_args()

    stream = generate(seed=args.seed)
    stream.write_jsonl(args.output)

    print(f"\n[scenario] self_healing")
    print(f"[scenario] Seed: {args.seed}")
    print(f"[scenario] Facts: {len(stream.facts())}")
    for fact in stream.facts():
        print(f"  {fact['timestamp']} | {fact['event_type']}")


if __name__ == "__main__":
    main()
