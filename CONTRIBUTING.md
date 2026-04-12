# Contributing to Kona Os

## Getting Started

```bash
git clone https://github.com/konaosdev/kona-os
cd kona-os
pip install -e ".[dev]"
```

Verify the setup:

```bash
pytest tests/ -v
```

All 74 tests should pass before you start.

## Branch Workflow

```bash
git checkout -b feature/your-feature
# work
pytest tests/ -v
git commit -m "feat(module): description"
git push origin feature/your-feature
```

Open a PR against `main`. CI runs on Python 3.10, 3.11, 3.12.

## What to Work On

- **New analyzers** — add to `kona/analyzers/`, register in `engine.py`
- **Agent improvements** — heuristic tuning in `kona/agents/`
- **CLI flags** — extend `ts/cli.ts`
- **Dashboard components** — add Vue components in `dashboard/src/`
- **Tests** — 70%+ coverage required (CI enforces this)

## Code Standards

- Python: dataclasses only, no Pydantic, no external ML deps
- All metrics must be normalized to 0–100
- New agents must implement `analyze(token: TokenProcess) -> float`
- New analyzers must implement `score(token: TokenProcess) -> float`
- Tests live in `tests/` mirroring the source structure

## Commit Style

```
feat(engine): add cross-metric correlation pass
fix(signal_agent): handle empty ticker edge case
test(memory_analyzer): add pattern coverage for rug signatures
docs: update metric weights table
chore: bump deps
```

## Adding a New Metric

1. Create `kona/analyzers/your_analyzer.py` with a `score(token) -> float` method
2. Register it in `kona/engine.py` inside `analyze()`
3. Add the weight to `OsMetrics.final_score()`
4. Write tests in `tests/test_analyzers.py`
5. Update the metric table in `README.md`

## Pull Request Checklist

- [ ] All existing tests pass
- [ ] New code has test coverage
- [ ] No external ML dependencies introduced
- [ ] Metric outputs normalized to 0–100
- [ ] Commit messages follow Conventional Commits

## Issues

Open an issue before starting large changes. Describe what you want to fix or add and why. This saves time if the direction doesn't fit the project.
