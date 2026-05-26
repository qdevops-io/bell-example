"""Bell-state example — the simplest possible QDevOps run.

Submits a 2-qubit Bell circuit (|00> + |11>) to the simulator backend,
waits for the result, and prints both the raw shot counts and the
fidelity (fraction of shots that landed on the entangled basis states).

On a noiseless simulator this should produce ~50/50 |00>/|11> and a
fidelity of 1.0. Run it as a smoke test that your token, project, and
the qass dispatcher are all healthy.
"""

from __future__ import annotations

import os
import sys
from typing import Any

from qdevops import APIError, Client


# A noiseless simulator should be at 1.0; depolarising noise pushes
# toward 0.5. Anything below this on `simulator` means something is
# wrong with the worker or the SDK contract.
MIN_FIDELITY = 0.95


def bell_fidelity(result: dict[str, Any]) -> float:
    """Fraction of shots that landed on |00> or |11>."""
    counts = result.get("counts") or {}
    total = sum(int(v) for v in counts.values())
    if total == 0:
        raise ValueError("run returned zero shots")
    good = int(counts.get("00", 0)) + int(counts.get("11", 0))
    return good / total


def required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        print(f"bell-example: missing env var {name}", file=sys.stderr)
        sys.exit(2)
    return value


def main() -> int:
    project_id = int(required_env("QDEVOPS_PROJECT_ID"))
    client = Client(
        api_token=required_env("QDEVOPS_API_TOKEN"),
        base_url=os.environ.get("QDEVOPS_BASE_URL") or "https://qdevops.io",
    )
    backend = os.environ.get("QDEVOPS_BACKEND", "simulator")
    shots = int(os.environ.get("QDEVOPS_SHOTS", "4096"))

    print(f"bell-example: submitting bell on {backend} (shots={shots}, project={project_id})")
    try:
        submission = client.submit_run(
            project_id=project_id,
            circuit="bell",
            backend=backend,
            params={"shots": shots},
        )
    except APIError as exc:
        print(f"bell-example: submit failed: HTTP {exc.status_code} — {exc.message}", file=sys.stderr)
        return 1

    print(f"bell-example: queued runId={submission.run_id} — waiting…")
    try:
        full = client.wait_for_run(submission.run_id, timeout=300.0, poll_interval=2)
    except Exception as exc:
        print(f"bell-example: wait failed: {exc}", file=sys.stderr)
        return 1

    if full.status != "succeeded" or full.result is None:
        reason = full.failure_reason or f"run terminated as {full.status}"
        print(f"bell-example: run did not succeed — {reason}", file=sys.stderr)
        return 1

    fidelity = bell_fidelity(full.result)
    counts = full.result.get("counts") or {}
    print(f"bell-example: counts = {counts}")
    print(f"bell-example: fidelity = {fidelity:.4f} (min acceptable on simulator: {MIN_FIDELITY})")
    print(f"bell-example: duration = {full.duration_ms} ms")

    # Only enforce the fidelity floor on the noiseless simulator. Real
    # hardware (`ibm`, `braket`) legitimately produces lower numbers and
    # the example would fail through no fault of the user.
    if backend == "simulator" and fidelity < MIN_FIDELITY:
        print(
            f"bell-example: fidelity {fidelity:.4f} < {MIN_FIDELITY} on simulator — failing.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
