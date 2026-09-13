# Repair Loop benchmark

This corpus contains 185 deliberately buggy, compact Python repositories. Cases
16-185 are written so a public-test-only special case still fails hidden checks.
Each
case has this layout:

```text
cases/<id>/
  manifest.json
  repo/                  # visible to the repair agent
    tests/               # public tests
  hidden_tests/          # evaluator-only regression tests
```

Every manifest uses schema version 1 and declares the visible repository,
hidden-test location, exact source paths a fixer may edit, public and hidden
test commands, difficulty, tags, and the public failure expected before repair.
Commands are run with `repo/` as the working directory. The hidden-test command
therefore deliberately points outside the fixer-visible repository.

Run `python benchmarks/build_cases.py` to regenerate the checked-in corpus.
Run `python -m pytest -q tests/test_benchmarks.py` to validate metadata and
confirm that every initial repository reproduces its declared public failure.
