<template>
  <div class="panel">
    <h2>Analyze Token</h2>
    <div class="fields">
      <input v-model="contract" placeholder="Contract address (e.g. So111...)" />
      <input type="number" v-model.number="lp" placeholder="LP locked %" min="0" max="100" />
      <input type="number" v-model.number="age" placeholder="Token age (days)" min="0" />
      <textarea v-model="narrative" placeholder="Paste narrative / community text..." rows="3" />
      <button :disabled="loading || !contract" @click="emit('analyze', { contract, lp, age, narrative })">
        {{ loading ? "Analyzing..." : "Run Kernel Scan" }}
      </button>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
defineProps<{ loading: boolean }>();
const emit = defineEmits<{ analyze: [p: { contract: string; lp: number; age: number; narrative: string }] }>();
const contract = ref(""); const lp = ref(0); const age = ref(0); const narrative = ref("");
</script>
<style scoped>
.panel{background:#0d1117;border:1px solid #1e2533;border-radius:12px;padding:24px;margin-bottom:24px}
h2{font-size:.85rem;font-weight:600;margin-bottom:16px;color:#6b7280;text-transform:uppercase;letter-spacing:.08em}
.fields{display:flex;flex-direction:column;gap:10px}
input,textarea{background:#070c14;border:1px solid #1e2533;border-radius:8px;padding:10px 14px;color:#e2e8f0;font-size:.9rem;outline:none;font-family:inherit}
input:focus,textarea:focus{border-color:#7c3aed}
textarea{resize:vertical}
button{background:#7c3aed;color:#fff;font-weight:700;border:none;border-radius:8px;padding:12px;cursor:pointer;font-size:.9rem;transition:opacity .2s}
button:disabled{opacity:.4;cursor:not-allowed}
</style>
