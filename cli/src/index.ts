import { execSync } from "child_process";
import type { KernelReport, OsVerdict } from "./types";

const VERDICT_COLORS: Record<OsVerdict, string> = {
  KERNEL:  "\x1b[92m",
  ROOT:    "\x1b[32m",
  SYSTEM:  "\x1b[33m",
  USER:    "\x1b[93m",
  IDLE:    "\x1b[90m",
  CRASHED: "\x1b[91m",
};
const RESET = "\x1b[0m";

function bar(value: number, width = 20): string {
  const filled = Math.round((value / 100) * width);
  return "█".repeat(filled) + "░".repeat(width - filled);
}

function runPython(contract: string, lp: number, age: number, narratives: string[]): KernelReport {
  const cmd = `python3 -c "
import json
from kona.engine import KonaEngine
from kona.models import TokenProcess
engine = KonaEngine()
token = TokenProcess(
    contract_address='${contract}',
    lp_locked_pct=${lp},
    token_age_days=${age},
    narratives=${JSON.stringify(narratives)},
)
r = engine.analyze(token)
print(json.dumps({
    'contract_address': r.contract_address,
    'verdict': r.verdict.value,
    'process_id': r.process_id,
    'log': r.log,
    'uptime_score': r.uptime_score,
    'final_score': round(r.metrics.final_score(), 2),
    'metrics': {
        'signal_clarity': r.metrics.signal_clarity,
        'process_health': r.metrics.process_health,
        'kernel_stability': r.metrics.kernel_stability,
        'routing_efficiency': r.metrics.routing_efficiency,
        'memory_score': r.metrics.memory_score,
    }
}))
"`;
  return JSON.parse(execSync(cmd, { encoding: "utf-8" }).trim());
}

function render(report: KernelReport): void {
  const color = VERDICT_COLORS[report.verdict] ?? "";
  const m = report.metrics;
  const addr = report.contract_address;
  console.log(`\n${"─".repeat(54)}`);
  console.log(`  Kona Os — Process Report`);
  console.log(`  PID: ${report.process_id} · ${addr.slice(0, 16)}...`);
  console.log(`${"─".repeat(54)}`);
  console.log(`  Verdict  : ${color}${report.verdict}${RESET}`);
  console.log(`  Score    : ${report.final_score.toFixed(1)}/100  Uptime: ${report.uptime_score.toFixed(0)}%`);
  console.log();
  console.log(`  ${"Signal Clarity".padEnd(22)} ${bar(m.signal_clarity)} ${m.signal_clarity.toFixed(1)}`);
  console.log(`  ${"Process Health".padEnd(22)} ${bar(m.process_health)} ${m.process_health.toFixed(1)}`);
  console.log(`  ${"Kernel Stability".padEnd(22)} ${bar(m.kernel_stability)} ${m.kernel_stability.toFixed(1)}`);
  console.log(`  ${"Routing Efficiency".padEnd(22)} ${bar(m.routing_efficiency)} ${m.routing_efficiency.toFixed(1)}`);
  console.log(`  ${"Memory Score".padEnd(22)} ${bar(m.memory_score)} ${m.memory_score.toFixed(1)}`);
  console.log();
  for (const line of report.log) console.log(`  ${line}`);
  console.log(`${"─".repeat(54)}\n`);
}

const args = process.argv.slice(2);
const contract = args[0] ?? "unknown";
const lp = parseFloat(args.find(a => a.startsWith("--lp="))?.split("=")[1] ?? "0");
const age = parseInt(args.find(a => a.startsWith("--age="))?.split("=")[1] ?? "0");
const narratives = args.filter(a => !a.startsWith("--") && a !== contract);

render(runPython(contract, lp, age, narratives));
