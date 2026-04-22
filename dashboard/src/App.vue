<template>
  <div class="app">
    <header>
      <h1>Kona Os</h1>
      <p class="sub">Solana Token Kernel Analyzer — Signal Routing Engine</p>
    </header>
    <main>
      <ProcessInput @analyze="onAnalyze" :loading="loading" />
      <KernelCard v-if="report" :report="report" />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import ProcessInput from "./ProcessInput.vue";
import KernelCard from "./KernelCard.vue";
import type { KernelReport } from "./types";

const loading = ref(false);
const report = ref<KernelReport | null>(null);

async function onAnalyze(payload: { contract: string; lp: number; age: number; narrative: string }) {
  loading.value = true;
  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    report.value = await res.json();
  } finally {
    loading.value = false;
  }
}
</script>

<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#07090f;color:#e2e8f0;font-family:'JetBrains Mono',monospace}
.app{max-width:860px;margin:0 auto;padding:40px 20px}
header{text-align:center;margin-bottom:40px}
h1{font-size:2rem;font-weight:700;color:#a78bfa;letter-spacing:-0.02em}
.sub{color:#4a5568;margin-top:6px;font-size:.9rem}
</style>
