# Kona Os — Project Context

## What is this

Solana token kernel analyzer. Treats each token like a process in an operating system — assigns a kernel-level classification (KERNEL/ROOT/SYSTEM/USER/IDLE/CRASHED) based on 5 weighted metrics derived from on-chain data.

## Stack

- **Python 3.10+** — Core engine, agents, analyzers, 74 tests
- **TypeScript 5** — CLI tool (`ts/cli.ts`)
- **Vue 3** — Real-time dashboard (`dashboard/`)
- **FastAPI** — REST oracle (`kona/server.py`)
- **Docker** — Compose setup for oracle + dashboard

## Architecture

```
TokenProcess (input dataclass)
    ↓
KonaEngine
  ├── SignalAgent        → signal_clarity    (weight 0.25)
  ├── KernelAgent        → process_health    (weight 0.25)
  ├── StabilityAnalyzer  → kernel_stability  (weight 0.20)
  ├── RoutingAnalyzer    → routing_efficiency (weight 0.20)
  └── MemoryAnalyzer     → memory_score      (weight 0.10)
    ↓
KernelReport (verdict, metrics, final_score, log, process_id)
```

## Core Files

| Path | Role |
|------|------|
| `kona/models.py` | `TokenProcess`, `OsMetrics`, `KernelReport`, `OsVerdict` |
| `kona/engine.py` | `KonaEngine.analyze()` — orchestrates all agents/analyzers |
| `kona/agents/signal_agent.py` | Heuristic + Claude Haiku signal clarity scoring |
| `kona/agents/kernel_agent.py` | LP ratio, top-10 concentration, token age scoring |
| `kona/analyzers/memory_analyzer.py` | Pattern matching against success signatures |
| `kona/analyzers/routing_analyzer.py` | Volume-to-holder routing, buy/sell pressure |
| `kona/analyzers/stability_analyzer.py` | Volatility resistance scoring |
| `kona/server.py` | FastAPI endpoint `POST /analyze` |
| `ts/cli.ts` | TypeScript CLI |
| `dashboard/src/` | Vue 3 dashboard components |

## Key Rules

- All metrics are normalized to 0–100
- `OsMetrics.final_score()` weights: signal×0.25, health×0.25, stability×0.20, routing×0.20, memory×0.10
- `OsVerdict` thresholds: KERNEL≥90, ROOT≥75, SYSTEM≥60, USER≥40, IDLE≥20, else CRASHED
- `process_id` = first 8 chars of sha256(contract_address).upper()
- Claude Haiku (`claude-haiku-4-5-20251001`) used in signal agent; falls back to heuristic if no API key
- No Pydantic — dataclasses only
- 70% test coverage enforced by CI

## Testing

```bash
pytest tests/ -v                              # all 74 tests
pytest tests/ --cov=kona --cov-fail-under=70  # coverage check
```

## Commit Style

```
feat(module): description
fix(module): fix description
test(module): add test description
chore: maintenance

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```
