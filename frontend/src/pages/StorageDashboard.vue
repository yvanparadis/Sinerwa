<template>
  <div class="page">
    <div class="container">
      <header class="page-header">
        <h1>Storage Dashboard</h1>
        <p class="page-sub">Cloudflare R2 storage status (developer only).</p>
      </header>

      <div v-if="loading" class="empty-wrap">
        <SkeletonBox width="100%" height="120px" />
      </div>
      <div v-else-if="error" class="empty-wrap">
        <ErrorState title="Couldn't load storage status" text="Make sure the backend is running." :retry="true" @retry="load" />
      </div>
      <div v-else>
        <div class="status-grid">
          <div class="status-card">
            <h3>Configuration</h3>
            <div class="row"><span>Configured</span><strong>{{ status.configured ? 'Yes' : 'No' }}</strong></div>
            <div class="row"><span>Endpoint</span><span>{{ status.endpoint || '—' }}</span></div>
            <div class="row"><span>Max upload</span><span>{{ formatBytes(status.max_upload_bytes) }}</span></div>
          </div>
          <div class="status-card" v-for="b in buckets" :key="b.name">
            <h3>{{ b.name }} bucket</h3>
            <div class="row"><span>Name</span><span>{{ b.bucket || '—' }}</span></div>
            <div class="row"><span>Connected</span><strong :class="b.info.ok ? 'ok' : 'fail'">{{ b.info.ok ? 'Yes' : 'No' }}</strong></div>
            <div class="row"><span>Files</span><span>{{ b.info.file_count ?? 0 }}</span></div>
            <div class="row"><span>Total size</span><span>{{ formatBytes(b.info.total_bytes) }}</span></div>
            <div v-if="b.info.error" class="err">{{ b.info.error }}</div>
            <button class="btn btn-ghost btn-sm" @click="test(b.bucket)" :disabled="!status.configured || !b.bucket">Test connection</button>
          </div>
        </div>

        <div v-if="status.warnings && status.warnings.length" class="warnings">
          <div v-for="w in status.warnings" :key="w" class="warn">⚠ {{ w }}</div>
        </div>

        <div class="not-configured" v-if="!status.configured">
          <h3>R2 not configured</h3>
          <p>Set R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_PRIVATE_BUCKET, R2_PUBLIC_BUCKET (and optionally R2_S3_ENDPOINT, R2_PUBLIC_DELIVERY_BASE_URL) in backend/.env. See docs.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import SkeletonBox from "@/components/common/SkeletonBox.vue";
import ErrorState from "@/components/common/ErrorState.vue";
const status = ref({});
const loading = ref(true);
const error = ref(false);
const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

const buckets = computed(() => ([
  { name: "Private", bucket: status.value.private_bucket, info: status.value.private || {} },
  { name: "Public", bucket: status.value.public_bucket, info: status.value.public || {} },
]));

function formatBytes(b) {
  if (!b) return "0 B";
  const units = ["B","KB","MB","GB","TB"];
  let i = 0;
  let v = b;
  while (v >= 1024 && i < units.length - 1) { v /= 1024; i++; }
  return `${v.toFixed(1)} ${units[i]}`;
}

async function load() {
  loading.value = true;
  error.value = false;
  try {
    const res = await fetch(`${API_BASE}/api/v1/storage/status`);
    if (!res.ok) throw new Error("fail");
    status.value = await res.json();
  } catch (e) {
    error.value = true;
  } finally {
    loading.value = false;
  }
}

async function test(bucket) {
  try {
    const res = await fetch(`${API_BASE}/api/v1/storage/test?bucket=${encodeURIComponent(bucket)}`, { method: "POST" });
    const data = await res.json();
    alert(JSON.stringify(data));
    await load();
  } catch (e) {
    alert("Test failed: " + e.message);
  }
}

onMounted(load);
</script>

<style scoped>
.page { padding: var(--space-8) 0; }
.page-header h1 { font-size: var(--text-3xl); font-weight: var(--font-weight-extrabold); margin: 0 0 var(--space-2); }
.page-sub { color: var(--color-secondary-text); margin: 0 0 var(--space-6); }
.status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: var(--space-4); margin-bottom: var(--space-6); }
.status-card { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: var(--space-5); }
.status-card h3 { margin: 0 0 var(--space-3); font-size: var(--text-lg); }
.row { display: flex; justify-content: space-between; gap: var(--space-3); font-size: var(--text-sm); padding: var(--space-1) 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
.row span:first-child { color: var(--color-secondary-text); }
.ok { color: #4ade80; }
.fail { color: var(--color-danger); }
.err { color: var(--color-danger); font-size: var(--text-xs); margin: var(--space-2) 0; }
.warnings { margin-bottom: var(--space-6); }
.warn { background: rgba(245,158,11,0.1); border: 1px solid #f59e0b; color: #fbbf24; padding: var(--space-2) var(--space-3); border-radius: var(--radius-md); margin-bottom: var(--space-2); font-size: var(--text-sm); }
.not-configured { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: var(--space-5); }
.not-configured h3 { margin: 0 0 var(--space-2); }
.not-configured p { color: var(--color-secondary-text); font-size: var(--text-sm); }
.empty-wrap { text-align: center; padding: var(--space-10) 0; display: flex; flex-direction: column; align-items: center; gap: var(--space-4); }
</style>
