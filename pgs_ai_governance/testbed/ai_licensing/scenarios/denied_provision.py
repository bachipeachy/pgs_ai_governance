"""
denied_provision.py — Scenario: Provision denied due to incomplete training.

Narrative:
  A new employee joins and immediately requests an AI license.
  The protocol denies the request because training is not yet complete.
  This is a first-class outcome, not an error.

Timeline:
  T+0h: Employee registered (onboarding)
  T+2h: License cap established by IT
  T+4h: Employee requests AI license (eager)
  T+4h: Protocol denies — training incomplete
"""


import argparse
from pathlib import Path

from pgs_ai_governance.testbed.ai_licensing.scenarios.base import FactStream


def generate(seed: int = 42) -> FactStream:
    """Generate denied provision scenario."""
    stream = FactStream(seed=seed)

    # T+0: Monday morning — new employee registered
    employee = stream.generate_employee()
    stream.emit_ev_employee_registered(employee)

    # T+2h: IT configures license cap
    stream.advance_time(hours=2)
    stream.emit_ev_license_cap_set(cap=10)

    # T+4h: Employee requests license (before completing training)
    stream.advance_time(hours=2)
    stream.emit_in_provision_ai_license(employee["employee_id"])

    # T+4h: Protocol denies — training not complete
    # This is the protocol's response, not a user action
    stream.emit_ev_provision_denied(
        employee_id=employee["employee_id"],
        reason_code="TRAINING_INCOMPLETE"
    )

    return stream


def main():
    parser = argparse.ArgumentParser(description="Generate denied_provision scenario")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent.parent / "generated" / "denied_provision.jsonl",
    )
    args = parser.parse_args()

    stream = generate(seed=args.seed)
    stream.write_jsonl(args.output)

    print(f"\n[scenario] denied_provision")
    print(f"[scenario] Seed: {args.seed}")
    print(f"[scenario] Facts: {len(stream.facts())}")
    for fact in stream.facts():
        print(f"  {fact['timestamp']} | {fact['event_type']}")


if __name__ == "__main__":
    main()
