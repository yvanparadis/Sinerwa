<template>
  <div class="page">
    <div class="container">
      <header class="page-header">
        <h1>Content Providers</h1>
        <p class="page-sub">Provider management and synchronization status.</p>
      </header>

      <div v-if="syncResult" class="sync-result" :class="syncResult.status">
        <div class="sr-title">{{ syncResult.message }}</div>
        <div class="sr-grid">
          <div><span>Status</span><strong>{{ syncResult.status }}</strong></div>
          <div><span>Processed</span><strong>{{ syncResult.records_processed }}</strong></div>
          <div><span>Added</span><strong>{{ syncResult.records_added }}</strong></div>
          <div><span>Updated</span><strong>{{ syncResult.records_updated }}</strong></div>
          <div><span>Skipped</span><strong>{{ syncResult.records_skipped }}</strong></div>
          <div><span>Failed</span><strong>{{ syncResult.records_failed }}</strong></div>
        </div>
        <div v-if="syncResult.last_sync_at" class="sr-time">Last sync: {{ syncResult.last_sync_at }}</div>
      </div>

      <div v-if="loading" class="grid">
        <SkeletonBox v-for="n in 3" :key="n" width="100%" height="160px" />
      </div>
      <div v-else-if="error" class="empty-wrap">
        <ErrorState title="Couldn't load providers" text="Make sure the backend is running." :retry="true" @retry="load" />
      </div>
      <div v-else class="provider-grid">
        <div v-for="p in providers" :key="p.id" class="provider-card">
          <div class="pc-header">
            <h3>{{ p.name }}</h3>
            <span class="badge" :class="p.authorization_status">{{ p.authorization_status }}</span>
          </div>
          <div class="pc-row"><span>Website</span><a :href="p.website" target="_blank" rel="noopener">{{ p.website }}</a></div>
          <div class="pc-row"><span>Type</span><span>{{ p.provider_type }}</span></div>
          <div class="pc-row"><span>Integration</span><span>{{ p.integration_method }}</span></div>
          <div class="pc-row"><span>Connection</span><span class="status" :class="p.connection_status">{{ p.connection_status }}</span></div>
          <div class="pc-row"><span>API available</span><span>{{ p.api_available ? 'Yes' : 'No' }}</span></div>
          <div class="pc-row"><span>Imported records</span><span>{{ p.imported_count }}</span></div>
          <div class="pc-row"><span>Last sync</span><span>{{ p.last_sync_at || 'Never' }}</span></div>
          <div v-if="p.error_message" class="pc-error">{{ p.error_message }}</div>
          <div class="pc-actions">
            <button
              class="btn btn-primary btn-sm"
              :disabled="p.authorization_status !== 'authorized' || syncing === p.id"
              @click="sync(p.id)"
            >
              {{ syncing === p.id ? 'Syncing…' : 'Synchronize' }}
            </button>
            <span v-if="p.authorization_status !== 'authorized'" class="pc-note">Authorization required before sync.</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import SkeletonBox from "@/components/common/SkeletonBox.vue";
import EmptyState from "@/components/common/EmptyState.vue";
import ErrorState from "@/components/common/ErrorState.vue";

const providers = ref([]);
const loading = ref(true);
const error = ref(false);
const syncing = ref(null);
const syncResult = ref(null);
const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

async function load() {
  loading.value = true;
  error.value = false;
  try {
    const res = await fetch(`${API_BASE}/api/v1/providers`);
    if (!res.ok) throw new Error("fail");
    const data = await res.json();
    providers.value = data.providers || [];
  } catch (e) {
    error.value = true;
  } finally {
    loading.value = false;
  }
}

async function sync(id) {
  syncing.value = id;
  syncResult.value = null;
  try {
    const res = await fetch(`${API_BASE}/api/v1/providers/${id}/sync`, { method: "POST" });
    const data = await res.json();
    syncResult.value = data;
    await load();
  } catch (e) {
    syncResult.value = { status: "failed", message: "Synchronization request failed." };
  } finally {
    syncing.value = null;
  }
}

onMounted(load);
</script>

<style scoped>
.page { padding: var(--space-8) 0; }
.page-header h1 { font-size: var(--text-3xl); font-weight: var(--font-weight-extrabold); margin: 0 0 var(--space-2); }
.page-sub { color: var(--color-secondary-text); margin: 0 0 var(--space-6); }
.provider-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: var(--space-4); }
.provider-card { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: var(--space-5); }
.pc-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--space-4); }
.pc-header h3 { margin: 0; font-size: var(--text-xl); }
.pc-row { display: flex; justify-content: space-between; gap: var(--space-3); font-size: var(--text-sm); padding: var(--space-1) 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
.pc-row span:first-child { color: var(--color-secondary-text); }
.pc-row a { color: var(--color-lavender); }
.status.connected { color: var(--color-success); }
.status.pending_authorization { color: var(--color-lavender); }
.status.error { color: var(--color-danger); }
.badge.authorized { background: rgba(34,197,94,0.18); color: #4ade80; }
.badge.pending { background: rgba(139,92,246,0.18); color: var(--color-lavender); }
.pc-error { color: var(--color-danger); font-size: var(--text-xs); margin: var(--space-3) 0; }
.pc-actions { display: flex; align-items: center; gap: var(--space-3); margin-top: var(--space-4); flex-wrap: wrap; }
.pc-note { color: var(--color-secondary-text); font-size: var(--text-xs); }
.empty-wrap { text-align: center; padding: var(--space-10) 0; display: flex; flex-direction: column; align-items: center; gap: var(--space-4); }
.sync-result { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: var(--space-5); margin-bottom: var(--space-6); }
.sync-result.skipped { border-color: var(--color-lavender); }
.sync-result.failed { border-color: var(--color-danger); }
.sync-result.partial { border-color: #f59e0b; }
.sr-title { font-weight: var(--font-weight-bold); margin-bottom: var(--space-3); }
.sr-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: var(--space-2); }
.sr-grid div { display: flex; flex-direction: column; background: var(--color-deep-violet); padding: var(--space-2); border-radius: var(--radius-md); }
.sr-grid span { font-size: var(--text-xs); color: var(--color-secondary-text); }
.sr-grid strong { font-size: var(--text-lg); }
.sr-time { margin-top: var(--space-3); font-size: var(--text-xs); color: var(--color-secondary-text); }
</style>
