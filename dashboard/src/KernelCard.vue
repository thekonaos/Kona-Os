<template>
  <div class="card">
    <div class="top">
      <div>
        <span class="pid">PID: {{ report.process_id }}</span>
        <span class="verdict" :class="report.verdict.toLowerCase()">{{ report.verdict }}</span>
      </div>
      <div class="score">{{ finalScore.toFixed(1) }}<span class="denom">/100</span></div>
    </div>
    <div class="addr">{{ report.contract_address }}</div>
    <div class="metrics">
      <div v-for="(val, key) in report.metrics" :key="key" class="metric">
        <span class="mname">{{ labels[key] }}</span>
        <div class="track"><div class="fill" :style="{ width: val + '%' }" /></div>
        <span class="mval">{{ val.toFixed(1) }}</span>
      </div>
    </div>
    <div class="log">
      <div v-for="(line, i) in report.log" :key="i" class="line">{{ line }}</div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";
import type { KernelReport } from "./types";
const props = defineProps<{ report: KernelReport }>();
const finalScore = computed(() => { const m = props.report.metrics; return m.signal_clarity*.25+m.process_health*.25+m.kernel_stability*.20+m.routing_efficiency*.20+m.memory_score*.10; });
const labels: Record<string,string> = { signal_clarity:"Signal Clarity", process_health:"Process Health", kernel_stability:"Kernel Stability", routing_efficiency:"Routing Efficiency", memory_score:"Memory Score" };
</script>
<style scoped>
.card{background:#0d1117;border:1px solid #1e2533;border-radius:12px;padding:24px}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.pid{font-size:.75rem;color:#4a5568;margin-right:10px}
.verdict{font-weight:800;font-size:1.2rem;letter-spacing:.06em}
.verdict.kernel{color:#22c55e}.verdict.root{color:#4ade80}.verdict.system{color:#facc15}.verdict.user{color:#fb923c}.verdict.idle{color:#6b7280}.verdict.crashed{color:#ef4444}
.score{font-size:1.6rem;font-weight:700;color:#a78bfa}
.denom{font-size:.9rem;color:#4a5568}
.addr{font-size:.75rem;color:#4a5568;margin-bottom:18px;word-break:break-all}
.metrics{display:flex;flex-direction:column;gap:8px;margin-bottom:18px}
.metric{display:grid;grid-template-columns:150px 1fr 40px;align-items:center;gap:10px}
.mname{font-size:.75rem;color:#6b7280}
.track{height:4px;background:#1e2533;border-radius:4px;overflow:hidden}
.fill{height:100%;background:#7c3aed;border-radius:4px;transition:width .4s}
.mval{font-size:.75rem;color:#9ca3af;text-align:right}
.log{border-top:1px solid #1e2533;padding-top:14px;display:flex;flex-direction:column;gap:4px}
.line{font-size:.75rem;color:#6b7280;font-family:'JetBrains Mono',monospace}
</style>
