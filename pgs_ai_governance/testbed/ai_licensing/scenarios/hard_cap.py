"""
hard_cap.py — Scenario: License cap enforced as hard limit.

Narrative:
  IT sets a license cap of 3.
  Three employees complete training and receive licenses.
  A fourth employee completes training and requests a license.
  The protocol denies — cap is a hard limit, not a soft warning.
  The denial is recorded as a first-class outcome.

Timeline:
  T+0h:   License cap set to 3
  T+1d:   Employee A registered, trained, provisioned
  T+2d:   Employee B registered, trained, provisioned
  T+3d:   Employee C registered, trained, provisioned
  T+4d:   Employee D registered, trained
  T+4d+1h: Employee D requests license
  T+4d+1h: Protocol denies — CAP_REACHED
"""


import argparse
from pathlib import Path

from pgs_ai_governance.testbed.ai_licensing.scenarios.base import FactStream


def generate(seed: int = 42) -> FactStream:
    """Generate hard cap enforcement scenario."""
    stream = FactStream(seed=seed)

    # T+0: IT sets restrictive cap
    stream.emit_ev_license_cap_set(cap=3)

    # Days 1-3: Three employees successfully provision
    licensed_employees = []
    for day in range(1, 4):
        stream.advance_time(days=1)

        # Morning: Employee registered
        employee = stream.generate_employee()
        stream.emit_ev_employee_registered(employee)

        # Afternoon: Training completed
        stream.advance_time(hours=4)
        stream.emit_ev_training_completed(employee["employee_id"])

        # Later: License provisioned
        stream.advance_time(hours=1)
        license_id = f"lic-{employee['employee_id'].split('-')[1]}"
        stream.emit_ev_license_provisioned(
            employee_id=employee["employee_id"],
            license_id=license_id
        )
        licensed_employees.append((employee, license_id))

    # Day 4: Fourth employee — the one who hits the cap
    stream.advance_time(days=1)
    employee_d = stream.generate_employee()
    stream.emit_ev_employee_registered(employee_d)

    # Training completed (they did everything right)
    stream.advance_time(hours=4)
    stream.emit_ev_training_completed(employee_d["employee_id"])

    # Request license
    stream.advance_time(hours=1)
    stream.emit_in_provision_ai_license(employee_d["employee_id"])

    # Protocol denies — hard cap reached
    stream.emit_ev_provision_denied(
        employee_id=employee_d["employee_id"],
        reason_code="CAP_REACHED"
    )

    return stream


def main():
    parser = argparse.ArgumentParser(description="Generate hard_cap scenario")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent.parent / "generated" / "hard_cap.jsonl",
    )
    args = parser.parse_args()

    stream = generate(seed=args.seed)
    stream.write_jsonl(args.output)

    print(f"\n[scenario] hard_cap")
    print(f"[scenario] Seed: {args.seed}")
    print(f"[scenario] Facts: {len(stream.facts())}")
    for fact in stream.facts():
        print(f"  {fact['timestamp']} | {fact['event_type']}")


if __name__ == "__main__":
    main()
