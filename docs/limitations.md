# Limitations

- Passing tests is evidence, not proof, of a correct or secure repair.
- Results depend on case quality, hidden-test coverage, provider behavior,
  model version, and sandbox reproducibility.
- Cost estimates may differ from provider billing, especially with caching,
  retries, or changing prices.
- Container isolation shares the disposable Actions VM kernel and is weaker
  than a dedicated VM per candidate.
- Offline scoring does not upload traces or verify W&B authentication.
- The presentation adapters intentionally tolerate evolving core schemas;
  unexpected field names may appear as zero-valued diagnostics.
- The notebook calls the orchestrator directly. GitHub Actions startup,
  available minutes, API rate limits, and artifact retention affect latency.
- Docker runs only inside disposable GitHub-hosted runners; generated code does
  not execute in the Codespace or on Windows.
- Model nondeterminism requires repeated trials before comparing close results.

Do not use the system to patch production checkouts automatically. Human review,
normal CI, dependency scanning, and deployment controls remain mandatory.
