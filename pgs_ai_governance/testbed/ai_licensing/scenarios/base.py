"""
base.py — Shared utilities for scenario generation.

Provides deterministic, realistic fact generation.
"""


import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


# Realistic name pools (deterministic selection via seed)
FIRST_NAMES = [
    "Anita", "Marcus", "Priya", "James", "Sofia", "Chen", "Fatima", "David",
    "Yuki", "Omar", "Elena", "Raj", "Amara", "Luis", "Mei", "Aleksandr",
    "Zara", "Kofi", "Ingrid", "Tariq", "Nadia", "Kenji", "Olga", "Emmanuel",
]

LAST_NAMES = [
    "Rao", "Johnson", "Patel", "Williams", "Garcia", "Chen", "Hassan", "Kim",
    "Okonkwo", "Müller", "Svensson", "Nakamura", "Kowalski", "Santos", "Ivanov",
    "Osei", "Johansson", "Yamamoto", "Schmidt", "Fernandez", "Novak", "Park",
]

DEPARTMENTS = [
    "Product Engineering", "Data Science", "Platform", "Security",
    "Infrastructure", "Machine Learning", "DevOps", "Research",
    "Quality Assurance", "Architecture", "Mobile", "Cloud Services",
]


class FactStream:
    """Deterministic fact stream generator."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        self._counter = 0
        self._base_time = datetime(2025, 1, 6, 9, 0, 0)  # Monday morning
        self._current_time = self._base_time
        self._facts: list[dict[str, Any]] = []

    def _deterministic_choice(self, items: list, salt: str = "") -> Any:
        """Select item deterministically based on seed and counter."""
        key = f"{self.seed}:{self._counter}:{salt}"
        h = int(hashlib.sha256(key.encode()).hexdigest(), 16)
        return items[h % len(items)]

    def _generate_id(self, prefix: str) -> str:
        """Generate realistic ID with prefix."""
        key = f"{self.seed}:{self._counter}:{prefix}"
        h = int(hashlib.sha256(key.encode()).hexdigest(), 16)
        return f"{prefix}-{(h % 9000) + 1000}"

    def advance_time(self, days: int = 0, hours: int = 0, minutes: int = 0) -> datetime:
        """Advance current time by offset."""
        self._current_time += timedelta(days=days, hours=hours, minutes=minutes)
        return self._current_time

    def generate_employee(self) -> dict[str, Any]:
        """Generate a realistic employee record."""
        self._counter += 1
        first = self._deterministic_choice(FIRST_NAMES, "first")
        last = self._deterministic_choice(LAST_NAMES, "last")
        dept = self._deterministic_choice(DEPARTMENTS, "dept")
        emp_id = self._generate_id("e")

        return {
            "employee_id": emp_id,
            "name": f"{first} {last}",
            "email": f"{first.lower()}.{last.lower()}@corp.example",
            "department": dept,
        }

    def emit(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Emit a fact with current timestamp."""
        fact = {
            "event_type": event_type,
            "timestamp": self._current_time.isoformat() + "Z",
            **payload,
        }
        self._facts.append(fact)
        return fact

    def emit_ev_employee_registered(self, employee: dict[str, Any]) -> dict[str, Any]:
        """Emit employee registration fact."""
        return self.emit("EV_EMPLOYEE_REGISTERED_V0", {
            "employee_id": employee["employee_id"],
            "name": employee["name"],
            "email": employee["email"],
            "department": employee["department"],
        })

    def emit_ev_training_completed(self, employee_id: str) -> dict[str, Any]:
        """Emit training completion fact."""
        return self.emit("EV_TRAINING_COMPLETED_V0", {
            "employee_id": employee_id,
            "course_id": "AI-SAFETY-101",
            "score": 92,
        })

    def emit_ev_license_cap_set(self, cap: int) -> dict[str, Any]:
        """Emit license cap configuration fact."""
        return self.emit("EV_LICENSE_CAP_SET_V0", {
            "cap_count": cap,
            "effective_date": self._current_time.isoformat() + "Z",
        })

    def emit_in_provision_ai_license(self, employee_id: str) -> dict[str, Any]:
        """Emit provisioning intent."""
        return self.emit("IN_PROVISION_AI_LICENSE_V0", {
            "employee_id": employee_id,
            "requested_by": "system",
        })

    def emit_ev_license_provisioned(self, employee_id: str, license_id: str) -> dict[str, Any]:
        """Emit license provisioned fact."""
        return self.emit("EV_LICENSE_PROVISIONED_V0", {
            "employee_id": employee_id,
            "license_id": license_id,
        })

    def emit_ev_provision_denied(self, employee_id: str, reason_code: str) -> dict[str, Any]:
        """Emit provision denied fact."""
        return self.emit("EV_PROVISION_DENIED_V0", {
            "employee_id": employee_id,
            "reason_code": reason_code,
        })

    def emit_ev_usage_recorded(self, license_id: str) -> dict[str, Any]:
        """Emit usage activity fact."""
        return self.emit("EV_USAGE_RECORDED_V0", {
            "license_id": license_id,
            "action": "model_invocation",
        })

    def emit_in_reclaim_license(self, license_id: str, threshold_days: int) -> dict[str, Any]:
        """Emit reclamation intent."""
        return self.emit("IN_RECLAIM_LICENSE_V0", {
            "license_id": license_id,
            "threshold_days": threshold_days,
        })

    def emit_ev_license_revoked(self, license_id: str, employee_id: str, reason: str) -> dict[str, Any]:
        """Emit license revoked fact."""
        return self.emit("EV_LICENSE_REVOKED_V0", {
            "license_id": license_id,
            "employee_id": employee_id,
            "reason": reason,
        })

    def facts(self) -> list[dict[str, Any]]:
        """Return all emitted facts."""
        return self._facts

    def write_jsonl(self, path: Path) -> None:
        """Write facts to JSONL file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for fact in self._facts:
                f.write(json.dumps(fact) + "\n")
        print(f"[generator] Wrote {len(self._facts)} facts to {path}")
