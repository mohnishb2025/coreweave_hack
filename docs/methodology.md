# Evaluation methodology

Each model receives the same case revision, instructions, sandbox image,
validation commands, and budgets. Cases should include a reproducible failing
test, hidden regression tests, and metadata describing language and difficulty.
Run multiple seeded repetitions where providers permit it.

The primary metric is repair success: all required and regression tests pass.
Secondary metrics are regression-free rate, attempts to success, changed lines,
latency, token usage, and estimated cost. The leaderboard ranks success rate
first, then attempts and cost; it must not collapse correctness and cost into a
single opaque score.

Store every failed attempt, validation result, final diff, budget event, model
identifier, image digest, and code revision. Report confidence intervals and
both aggregate and per-case results. Exclude infrastructure failures from model
accuracy but report them separately.

`evaluate_records` and `build_leaderboard` run locally without Weave or network
access. Upload the same records through the explicit Weave evaluation helper
when credentials are available. Review a sample manually for test gaming,
overfitting, accidental fixture edits, and behavior not captured by tests.
