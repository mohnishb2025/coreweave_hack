# Architecture

`RepairLoop` is the deterministic orchestrator. It owns state, budgets,
handoffs, concurrency, checkpoints, quality gates, and stop conditions. LLM
agents can recommend actions but cannot execute commands or bypass a failed
gate.

The handoff sequence is:

1. The Codespace dispatches a baseline job to GitHub Actions.
2. The Diagnoser receives the failure and a bounded, secret-filtered repository
   snapshot.
3. The Manager turns the diagnosis into a repair plan.
4. Two Fixers independently produce unified diffs using different strategies.
5. Patch safety rejects test edits, traversal, binary content, oversized diffs,
   and paths outside the benchmark allowlist.
6. A disposable GitHub-hosted runner independently revalidates the payload and
   launches a remote container with no network, no capabilities, fixed
   resources, a read-only root, and an unprivileged user.
7. The Critic compares each patch with executable evidence.
8. QA assesses maintainability after deterministic verification succeeds.
9. A passing patch is returned for human approval. Failed evidence becomes the
   next iteration's Reflexion memory.

Fixers never communicate directly. Every handoff is a strict Pydantic schema
mediated by the orchestrator. On retries, the Diagnoser and Manager receive
prior critiques, public verifier output, withheld hidden-suite status, and QA
feedback before issuing new assignments.

This is verifier-guided Reflexion and best-of-N search, not model-weight
training. Improvement occurs in inference-time state: failed hypotheses and
patches alter the next prompt and candidate search. Loop variants can disable
diagnosis, criticism, retries, or parallel candidates for controlled ablations.

W&B Serverless Inference supplies role models. Weave traces the root loop and
each agent operation. Checkpoints under `.repair-loop/runs` record typed state,
usage, estimated cost, candidates, critiques, and verification evidence.
The notebook imports the same `repair_loop` package as the CLI. It calls the
orchestrator directly, while `GitHubActionsVerifier` converts baseline and
candidate requests into bounded workflow-dispatch data. It correlates the
resulting run, downloads `result.json`, validates its schema and request ID,
and returns a normal `VerificationResult`. This keeps the agent loop independent
of execution location.

W&B and GitHub credentials remain in Codespaces. They are never passed to the
remote test container, persisted in checkpoints, or included in workflow
inputs. Generated repository code executes neither on Windows nor in the
Codespace.
