# Demo

1. Show `repair-loop models` and `repair-loop cases`.
2. In the Codespace, open `uv run marimo run --host 0.0.0.0 --port 2718
   notebooks/repair_lab.py` and select a case, model, and conservative budget.
3. Start the repair from the notebook, or run
   `repair-loop repair CASE --model MODEL --variant full_team --max-attempts 3`.
4. Follow the linked disposable GitHub Actions run and narrate the failing test,
   candidate diff, remote container validation, feedback, and budget changes.
5. Show the final structured result and persisted checkpoint.
6. Follow the Weave URL to inspect nested agent and verification spans.
7. Run `repair-loop benchmark benchmarks/suite.json -m MODEL -v single_pass
   -v diagnose_fix -v full_team` and compare success, attempts, cost, and
   latency in the generated leaderboard.
8. Demonstrate `repair-loop resume RUN_ID` from a deliberately interrupted run.

Use synthetic fixtures and low-privilege Codespaces credentials. Before
presenting, run the complete remote path once. Keep a recorded trace and result
artifacts as a fallback for provider or venue connectivity failures.
