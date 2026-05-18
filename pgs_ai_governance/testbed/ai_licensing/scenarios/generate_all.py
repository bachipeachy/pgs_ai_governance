"""
generate_all.py — Generate all scenario fact streams.

Usage:
    python generate_all.py [--seed 42]

Generates JSONL files in ../generated/ for each scenario.
Same seed produces identical fact streams — reproducible demos.
"""


import argparse
from pathlib import Path

from pgs_ai_governance.testbed.ai_licensing.scenarios.denied_provision import generate as gen_denied
from pgs_ai_governance.testbed.ai_licensing.scenarios.hard_cap import generate as gen_hard_cap
from pgs_ai_governance.testbed.ai_licensing.scenarios.reclaim_inactive import generate as gen_reclaim
from pgs_ai_governance.testbed.ai_licensing.scenarios.self_healing import generate as gen_self_healing


def main():
    parser = argparse.ArgumentParser(description="Generate all scenario fact streams")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for all scenarios")
    args = parser.parse_args()

    output_dir = Path(__file__).parent.parent / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    scenarios = [
        ("denied_provision", gen_denied),
        ("self_healing", gen_self_healing),
        ("hard_cap", gen_hard_cap),
        ("reclaim_inactive", gen_reclaim),
    ]

    print(f"[generate_all] Seed: {args.seed}")
    print(f"[generate_all] Output: {output_dir}")
    print()

    total_facts = 0
    for name, generator in scenarios:
        stream = generator(seed=args.seed)
        output_path = output_dir / f"{name}.jsonl"
        stream.write_jsonl(output_path)
        total_facts += len(stream.facts())

    print()
    print(f"[generate_all] Complete: {len(scenarios)} scenarios, {total_facts} facts")


if __name__ == "__main__":
    main()
