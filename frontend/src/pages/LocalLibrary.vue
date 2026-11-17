<template>
  <div class="page">
    <div class="container">
      <header class="page-header">
        <h1>Local Library</h1>
        <p class="page-sub">Movies and series from your local device (read-only). {{ items.length }} files found.</p>
      </header>

      <div v-if="loading" class="grid">
        <SkeletonBox v-for="n in 8" :key="n" width="100%" height="120px" />
      </div>
      <div v-else-if="error" class="empty-wrap">
        <ErrorState title="Couldn't load local library" text="Make sure the backend is running on port 8000." :retry="true" @retry="load" />
      </div>
      <div v-else-if="items.length === 0" class="empty-wrap">
        <EmptyState icon="📁" title="No local media" text="No video files found in the configured folder." />
      </div>
      <div v-else>
        <div class="player-wrap" v-if="selected">
          <VideoPlayer :src="streamUrl(selected)" :subtitle="subtitleUrl(selected)" />
          <div class="now-playing">
            <h2>{{ selected.title }}</h2>
            <p v-if="selected.translator">Translated by {{ selected.translator }}</p>
          </div>
        </div>

        <div class="filters">
          <input v-model="query" class="input" placeholder="Search local files..." />
          <select v-model="typeFilter" class="input">
            <option value="">All types</option>
            <option value="movie">Movies</option>
            <option value="episode">Episodes/Series</option>
          </select>
          <select v-model="translatorFilter" class="input">
            <option value="">All translators</option>
            <option v-for="t in translators" :key="t" :value="t">{{ t }}</option>
          </select>
        </div>

        <div class="list">
          <div
            v-for="item in filtered"
            :key="item.id"
            class="local-card"
            :class="{ active: selected && selected.id === item.id }"
            @click="select(item)"
          >
            <div class="lc-icon">{{ item.contentType === 'episode' ? '📺' : '🎬' }}</div>
            <div class="lc-info">
              <div class="lc-title">{{ item.title }}</div>
              <div class="lc-meta">
                <span v-if="item.translator" class="lc-translator">🎬 {{ item.translator }}</span>
                <span v-if="item.season">{{ item.season }}</span>
                <span v-if="item.episode">{{ item.episode }}</span>
                <span class="lc-ext">{{ item.extension }}</span>
              </div>
            </div>
            <button class="btn btn-primary btn-sm" @click.stop="select(item)">Play</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import SkeletonBox from "@/components/common/SkeletonBox.vue";
import EmptyState from "@/components/common/EmptyState.vue";
import ErrorState from "@/components/common/ErrorState.vue";
import VideoPlayer from "@/components/player/VideoPlayer.vue";
import { localLibraryService } from "@/services/localLibrary";

const items = ref([]);
const loading = ref(true);
const error = ref(false);
const selected = ref(null);
const query = ref("");
const typeFilter = ref("");
const translatorFilter = ref("");

const translators = [
  "B da great","Cyber Bigwi","Didier","Dylan Kabaka","Eric Pro","Fey","Fred","Gaheza","Hakim","Jovi","Junior Giti","Kim Rwanda","Master P","Moses","Mr Genius","Ndabaga","Nkuba","Perfect","PK","Remmy","Rocky",
];

const filtered = computed(() => {
  let r = items.value;
  const q = query.value.trim().toLowerCase();
  if (q) r = r.filter((i) => i.title.toLowerCase().includes(q) || (i.translator || "").toLowerCase().includes(q));
  if (typeFilter.value) r = r.filter((i) => i.contentType === typeFilter.value);
  if (translatorFilter.value) r = r.filter((i) => i.translator === translatorFilter.value);
  return r;
});

function select(item) {
  selected.value = item;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function streamUrl(item) {
  return localLibraryService.streamUrl(item);
}
function subtitleUrl(item) {
  return localLibraryService.subtitleUrl(item);
}

async function load() {
  loading.value = true;
  error.value = false;
  try {
    items.value = await localLibraryService.list();
  } catch (e) {
    error.value = true;
  } finally {
    loading.value = false;
  }
}

onMounted(load);
</script>

<style scoped>
.page { padding: var(--space-8) 0; }
.page-header h1 { font-size: var(--text-3xl); font-weight: var(--font-weight-extrabold); margin: 0 0 var(--space-2); }
.page-sub { color: var(--color-secondary-text); margin: 0 0 var(--space-6); }
.player-wrap { margin-bottom: var(--space-6); }
.now-playing { margin-top: var(--space-3); }
.now-playing h2 { font-size: var(--text-xl); margin: 0 0 var(--space-1); }
.now-playing p { color: var(--color-secondary-text); font-size: var(--text-sm); margin: 0; }
.filters { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: var(--space-3); margin-bottom: var(--space-6); }
@media (max-width: 768px) { .filters { grid-template-columns: 1fr; } }
.list { display: flex; flex-direction: column; gap: var(--space-2); max-height: 60vh; overflow-y: auto; padding-right: var(--space-2); }
.local-card { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3); background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); cursor: pointer; transition: all var(--transition-fast); }
.local-card:hover { border-color: var(--color-primary-purple); }
.local-card.active { border-color: var(--color-primary-purple); background: var(--color-deep-violet); }
.lc-icon { font-size: 1.5rem; }
.lc-info { flex: 1; min-width: 0; }
.lc-title { font-weight: var(--font-weight-semibold); font-size: var(--text-sm); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.lc-meta { display: flex; gap: var(--space-2); font-size: var(--text-xs); color: var(--color-secondary-text); flex-wrap: wrap; margin-top: 2px; }
.lc-translator { color: var(--color-lavender); }
.lc-ext { opacity: 0.6; }
.empty-wrap { text-align: center; padding: var(--space-10) 0; display: flex; flex-direction: column; align-items: center; gap: var(--space-4); }
</style>
