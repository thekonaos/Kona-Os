<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=7c3aed&height=200&section=header&text=Kona%20Os&fontSize=72&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Solana%20Token%20Kernel%20Analyzer&descAlignY=60&descColor=a78bfa" />

[![Python](https://img.shields.io/badge/Python-3.10%2B-7c3aed?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-4ade80?style=flat-square&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Vue](https://img.shields.io/badge/Vue-3.x-22c55e?style=flat-square&logo=vuedotjs&logoColor=white)](https://vuejs.org)
[![Tests](https://img.shields.io/badge/tests-74%20passing-7c3aed?style=flat-square)](tests/)
[![License](https://img.shields.io/badge/license-MIT-a78bfa?style=flat-square)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-6d28d9?style=flat-square&logo=docker&logoColor=white)](Dockerfile)

</div>

---

Every Solana token runs a process. Some are kernel-level operations — clean execution, deep liquidity, tightly scoped. Others are user-space noise, idle signals waiting to dump. Most traders can't tell the difference until it's too late.

**Kona Os** treats each token like a process in an operating system. It reads the underlying signals — holder distribution, LP lock ratios, price volatility, wallet entropy — and assigns a kernel classification that describes what the token actually is, not what the narrative says it is.

Six process states. Five core metrics. One verdict.

---

## How It Works

Kona Os builds a `TokenProcess` from on-chain data and runs it through a five-layer kernel analysis engine:

```
TokenProcess (contract_address, holder_count, lp_ratio, ...)
    ↓
KonaEngine
  ├── SignalAgent       → signal_clarity   (0–100)
  ├── KernelAgent       → process_health   (0–100)
  ├── MemoryAnalyzer    → memory_score     (0–100)
  ├── RoutingAnalyzer   → routing_efficiency (0–100)
  └── StabilityAnalyzer → kernel_stability  (0–100)
    ↓
KernelReport
  { verdict, metrics, final_score, log, process_id }
```

The final score is a weighted composite:

| Metric | Weight | What It Measures |
|---|---|---|
| Signal Clarity | 25% | Token name/ticker noise vs. real signal tokens |
| Process Health | 25% | LP lock ratio, top-10 concentration, token age |
| Kernel Stability | 20% | Volatility resistance, price consistency |
| Routing Efficiency | 20% | Volume-to-holder routing, buy/sell pressure |
| Memory Score | 10% | Pattern matching against known success signatures |

---

## Kernel Verdicts

The engine classifies every token into one of six process states:

| Verdict | Score | Meaning |
|---|---|---|
| `KERNEL` | 90–100 | Deep system-level integrity. Rare. |
| `ROOT` | 75–89 | High privilege. Strong fundamentals. |
| `SYSTEM` | 60–74 | Stable process. Worth watching. |
| `USER` | 40–59 | Unprivileged. Mixed signals. |
| `IDLE` | 20–39 | Low activity. Losing momentum. |
| `CRASHED` | 0–19 | Process terminated. Exit. |

---

## Install

```bash
pip install konaos
```

Or from source:

```bash
git clone https://github.com/konaosdev/kona-os
cd kona-os
pip install -e ".[dev]"
```

---

## Python API

```python
from kona.models import TokenProcess
from kona.engine import KonaEngine

token = TokenProcess(
    contract_address="7xKX...",
    holder_count=4200,
    top10_concentration=0.22,
    lp_ratio=0.68,
    lp_locked=True,
    age_days=31,
    volume_24h=840000.0,
    price_change_24h=3.1,
    buy_sell_ratio=1.4,
    volatility_7d=0.18,
)

engine = KonaEngine()
report = engine.analyze(token)

print(report.verdict)       # ROOT
print(report.final_score)   # 81.4
print(report.process_id)    # A3F9C21B
for line in report.log:
    print(line)
```

---

## CLI

```bash
# TypeScript CLI (fast, no API key required)
cd ts && npm install
npx ts-node cli.ts \
  --address 7xKX... \
  --holders 4200 \
  --lp 0.68 \
  --locked \
  --age 31 \
  --volume 840000 \
  --change 3.1 \
  --buysell 1.4 \
  --volatility 0.18 \
  --top10 0.22
```

Output:

```
┌─────────────────────────────────────────┐
│  PID: A3F9C21B          verdict: ROOT   │
│  Score: 81.4 / 100                      │
├─────────────────────────────────────────┤
│  signal_clarity      ████████░░  79.0   │
│  process_health      █████████░  85.0   │
│  kernel_stability    ████████░░  80.0   │
│  routing_efficiency  ████████░░  82.0   │
│  memory_score        ██████░░░░  60.0   │
├─────────────────────────────────────────┤
│  [KERNEL] LP lock confirmed             │
│  [KERNEL] Age > 30d — stable process    │
│  [OK] buy/sell ratio elevated           │
│  [OK] top10 concentration within range  │
└─────────────────────────────────────────┘
```

---

## Dashboard

```bash
docker compose up
```

- Oracle API: `http://localhost:8000`
- Vue dashboard: `http://localhost:5173`

POST to `/analyze`:

```json
{
  "contract_address": "7xKX...",
  "holder_count": 4200,
  "top10_concentration": 0.22,
  "lp_ratio": 0.68,
  "lp_locked": true,
  "age_days": 31,
  "volume_24h": 840000,
  "price_change_24h": 3.1,
  "buy_sell_ratio": 1.4,
  "volatility_7d": 0.18
}
```

---

## Tests

```bash
pytest tests/ -v
```

74 tests across models, agents, analyzers, engine, and helpers. All passing.

---

## Stack

- **Python 3.10+** — Core engine, agents, analyzers
- **TypeScript 5** — CLI tool
- **Vue 3** — Real-time dashboard
- **FastAPI** — REST oracle
- **Docker** — One-command deployment
- **GitHub Actions** — CI on Python 3.10, 3.11, 3.12

---

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=7c3aed&height=100&section=footer" />
</div>
