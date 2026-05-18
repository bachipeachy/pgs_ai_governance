"""
reclaim_inactive.py — Scenario: Autonomous reclamation of inactive license.

Narrative:
  An employee receives an AI license and uses it actively for a month.
  Then usage stops completely.
  After 31 days of inactivity, the protocol autonomously reclaims the license.
  The license returns to the pool — available for waiting employees.
  No human intervention required.

Timeline:
  T+0h:     Employee registered
  T+1h:     Training completed
  T+2h:     License provisioned
  T+1d:     Usage recorded (active)
  T+7d:     Usage recorded (still active)
  T+14d:    Usage recorded (last activity)
  T+45d:    Reclamation check triggered (31 days inactive)
  T+45d:    Protocol reclaims license
"""


import argparse
from pathlib import Path

from pgs_ai_governance.testbed.ai_licensing.scenarios.base import FactStream


def generate(seed: int = 42) -> FactStream:
    """Generate inactive reclamation scenario."""
    stream = FactStream(seed=seed)

    # T+0: Employee onboarding
    employee = stream.generate_employee()
    stream.emit_ev_employee_registered(employee)

    # T+1h: Training completed
    stream.advance_time(hours=1)
    stream.emit_ev_training_completed(employee["employee_id"])

    # T+2h: License provisioned
    stream.advance_time(hours=1)
    license_id = f"lic-{employee['employee_id'].split('-')[1]}"
    stream.emit_ev_license_provisioned(
        employee_id=employee["employee_id"],
        license_id=license_id
    )

    # T+1d: First usage
    stream.advance_time(days=1)
    stream.emit_ev_usage_recorded(license_id)

    # T+7d: Week 1 usage
    stream.advance_time(days=6)
    stream.emit_ev_usage_recorded(license_id)

    # T+14d: Last usage (then employee goes quiet)
    stream.advance_time(days=7)
    stream.emit_ev_usage_recorded(license_id)

    # --- 31 days of silence ---

    # T+45d: Reclamation check triggered (31 days after last use)
    stream.advance_time(days=31)
    stream.emit_in_reclaim_license(
        license_id=license_id,
        threshold_days=30
    )

    # Protocol autonomously reclaims
    stream.emit_ev_license_revoked(
        license_id=license_id,
        employee_id=employee["employee_id"],
        reason="INACTIVITY"
    )

    return stream


def main():
    parser = argparse.ArgumentParser(description="Generate reclaim_inactive scenario")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent.parent / "generated" / "reclaim_inactive.jsonl",
    )
    args = parser.parse_args()

    stream = generate(seed=args.seed)
    stream.write_jsonl(args.output)

    print(f"\n[scenario] reclaim_inactive")
    print(f"[scenario] Seed: {args.seed}")
    print(f"[scenario] Facts: {len(stream.facts())}")
    for fact in stream.facts():
        print(f"  {fact['timestamp']} | {fact['event_type']}")


if __name__ == "__main__":
    main()
