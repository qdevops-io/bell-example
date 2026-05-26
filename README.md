# bell-example

The simplest possible [QDevOps](https://qdevops.io) run: a 2-qubit Bell pair
on the simulator backend. ~25 lines of substance — read it top-to-bottom in
under a minute.

> Infrastructure trust comes from examples. If this repo's CI is green, the
> SDK, the API, the dispatcher, the worker, and the simulator are all
> healthy end-to-end.

## What it does

1. Submits the built-in `bell` circuit to the `simulator` backend with 4096 shots.
2. Polls until the run reaches a terminal state.
3. Prints the raw shot counts and the **fidelity** — the fraction of shots
   that landed on the entangled basis states (`|00>` and `|11>`).
4. Exits non-zero on the simulator if fidelity < 0.95.

A noiseless simulator returns ~50/50 `00`/`11` and a fidelity of ~1.0.

## Run it

You need a [QDevOps account](https://qdevops.io), a project, and a personal
access token with the `runs:rw` scope.

```bash
pip install -r requirements.txt

export QDEVOPS_API_TOKEN=qass_pat_...
export QDEVOPS_PROJECT_ID=42

python bell.py
```

Optional overrides:

| Variable             | Default                | Meaning                                        |
| -------------------- | ---------------------- | ---------------------------------------------- |
| `QDEVOPS_BACKEND`    | `simulator`            | `simulator`, `ibm`, or `braket`                |
| `QDEVOPS_SHOTS`      | `4096`                 | Number of shots                                |
| `QDEVOPS_BASE_URL`   | `https://qdevops.io`   | Override for self-hosted / staging deployments |

## Expected output

```
bell-example: submitting bell on simulator (shots=4096, project=42)
bell-example: queued runId=123456 — waiting…
bell-example: counts = {'00': 2031, '11': 2065}
bell-example: fidelity = 1.0000 (min acceptable on simulator: 0.95)
bell-example: duration = 42 ms
```

## CI

`.github/workflows/run.yml` runs this example against the simulator on
every push, every PR, and weekly via cron. Secrets needed in repo settings:

- `QDEVOPS_API_TOKEN`
- `QDEVOPS_PROJECT_ID`

## See also

- [ghz-example](https://github.com/qdevops-io/ghz-example) — multi-qubit entanglement
- [vqe-example](https://github.com/qdevops-io/vqe-example) — variational eigensolver
- [compare-example](https://github.com/qdevops-io/compare-example) — diff two runs side-by-side
- [reproducibility-example](https://github.com/qdevops-io/reproducibility-example) — pinned environments
- [rerun-example](https://github.com/qdevops-io/rerun-example) — re-execute a previous run

## License

Apache-2.0 — see [LICENSE](./LICENSE).
