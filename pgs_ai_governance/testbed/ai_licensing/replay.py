"""
replay.py — Replay fact streams through the protocol.

Usage:
    python -m ai_licensing.testbed.replay --all
    python -m ai_licensing.testbed.replay generated/denied_provision.jsonl
"""


import argparse
import json
import sys
from pathlib import Path

def load_facts(path: Path) -> list[dict]:
    """Load facts from JSONL file."""
    facts = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                facts.append(json.loads(line))
    return facts


def replay_scenario(jsonl_path: Path) -> None:
    """Replay a single scenario fact stream."""
    print(f"\n{'='*60}")
    print(f"[replay] Scenario: {jsonl_path.stem}")
    print(f"{'='*60}")

    facts = load_facts(jsonl_path)
    print(f"[replay] Loaded {len(facts)} facts\n")

    # Track state as facts accumulate
    context = {
        "employees": {},
        "training_completed": set(),
        "licenses": {},
        "cap": None,
        "assigned_count": 0,
    }

    for i, fact in enumerate(facts, 1):
        event_type = fact.get("event_type", "UNKNOWN")
        timestamp = fact.get("timestamp", "")[:19]  # Trim to seconds

        # Update context based on fact type
        if event_type == "EV_EMPLOYEE_REGISTERED_V0":
            emp_id = fact["employee_id"]
            context["employees"][emp_id] = fact
            print(f"  {timestamp} | {event_type}")
            print(f"               → {fact.get('name')} ({fact.get('department')})")

        elif event_type == "EV_LICENSE_CAP_SET_V0":
            context["cap"] = fact["cap_count"]
            print(f"  {timestamp} | {event_type}")
            print(f"               → Cap set to {fact['cap_count']}")

        elif event_type == "EV_TRAINING_COMPLETED_V0":
            emp_id = fact["employee_id"]
            context["training_completed"].add(emp_id)
            print(f"  {timestamp} | {event_type}")
            print(f"               → {emp_id} completed training")

        elif event_type == "IN_PROVISION_AI_LICENSE_V0":
            emp_id = fact["employee_id"]
            print(f"  {timestamp} | {event_type}")
            print(f"               → Provisioning requested for {emp_id}")

            # Show eligibility state at this moment
            trained = emp_id in context["training_completed"]
            cap_ok = context["cap"] is None or context["assigned_count"] < context["cap"]
            print(f"               → Training: {'YES' if trained else 'NO'}, Cap: {context['assigned_count']}/{context['cap'] or '∞'}")

        elif event_type == "EV_PROVISION_DENIED_V0":
            emp_id = fact["employee_id"]
            reason = fact.get("reason_code", "UNKNOWN")
            print(f"  {timestamp} | {event_type}")
            print(f"               ✗ DENIED: {reason}")

        elif event_type == "EV_LICENSE_PROVISIONED_V0":
            emp_id = fact["employee_id"]
            lic_id = fact["license_id"]
            context["licenses"][lic_id] = emp_id
            context["assigned_count"] += 1
            print(f"  {timestamp} | {event_type}")
            print(f"               ✓ License {lic_id} provisioned")

        elif event_type == "EV_USAGE_RECORDED_V0":
            lic_id = fact["license_id"]
            print(f"  {timestamp} | {event_type}")
            print(f"               → Activity on {lic_id}")

        elif event_type == "IN_RECLAIM_LICENSE_V0":
            lic_id = fact["license_id"]
            threshold = fact["threshold_days"]
            print(f"  {timestamp} | {event_type}")
            print(f"               → Reclaim check: {lic_id} (threshold: {threshold} days)")

        elif event_type == "EV_LICENSE_REVOKED_V0":
            lic_id = fact["license_id"]
            reason = fact.get("reason", "UNKNOWN")
            if lic_id in context["licenses"]:
                del context["licenses"][lic_id]
                context["assigned_count"] -= 1
            print(f"  {timestamp} | {event_type}")
            print(f"               ✗ REVOKED: {lic_id} ({reason})")

        else:
            print(f"  {timestamp} | {event_type}")

    # Summary
    print(f"\n[replay] Final state:")
    print(f"         Licenses assigned: {context['assigned_count']}")
    print(f"         Cap: {context['cap'] or 'unlimited'}")


def main():
    parser = argparse.ArgumentParser(description="Replay fact streams")
    parser.add_argument("jsonl", type=Path, nargs="?", help="Path to JSONL file")
    parser.add_argument("--all", action="store_true", help="Replay all scenarios")
    args = parser.parse_args()

    # Since we run from root, construct path from there
    _here = Path(__file__).resolve().parent
    generated_dir = _here / "generated"

    if args.all:
        for jsonl_path in sorted(generated_dir.glob("*.jsonl")):
            replay_scenario(jsonl_path)
    elif args.jsonl:
        replay_scenario(args.jsonl)
    else:
        parser.print_help()
        sys.exit(1)

    print(f"\n{'='*60}")
    print("[replay] Complete")


if __name__ == "__main__":
    main()
