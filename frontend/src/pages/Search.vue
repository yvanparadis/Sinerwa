<template>
  <div class="page">
    <div class="container">
      <header class="page-header">
        <h1>Search</h1>
      </header>
      <div class="search-box">
        <input
          v-model="query"
          class="input"
          placeholder="Search movies, series, genres..."
          @input="onInput"
          ref="inputRef"
          autofocus
        />
      </div>

      <div v-if="loading" class="grid">
        <SkeletonBox v-for="n in 6" :key="n" width="100%" height="260px" />
      </div>
      <div v-else-if="query.trim() && results.length === 0" class="empty-wrap">
        <EmptyState icon="🔍" title="No results" text="Try a different keyword." />
      </div>
      <div v-else-if="results.length" class="grid">
        <MovieCard v-for="r in results" :key="r.id" :item="r" />
      </div>
      <div v-else class="suggestions-block">
        <h3>Suggestions</h3>
        <div class="chips">
          <button v-for="s in suggestions" :key="s" class="chip" @click="pick(s)">{{ s }}</button>
        </div>
        <p class="hint">Start typing to search the CineRwa catalog.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import MovieCard from "@/components/movie/MovieCard.vue";
import SkeletonBox from "@/components/common/SkeletonBox.vue";
import EmptyState from "@/components/common/EmptyState.vue";
import { searchService } from "@/services/movieService";

const route = useRoute();
const router = useRouter();
const query = ref(route.query.q || "");
const results = ref([]);
const suggestions = ref([]);
const loading = ref(false);
let timer = null;

async function onInput() {
  clearTimeout(timer);
  const q = query.value.trim();
  if (!q) {
    results.value = [];
    suggestions.value = await searchService.suggestions(q);
    return;
  }
  loading.value = true;
  timer = setTimeout(async () => {
    results.value = await searchService.search(q);
    suggestions.value = await searchService.suggestions(q);
    loading.value = false;
  }, 250);
}

function pick(s) {
  query.value = s;
  onInput();
}

onMounted(() => {
  if (query.value) onInput();
  else searchService.suggestions("").then((s) => (suggestions.value = s));
});
</script>

<style scoped>
.page { padding: var(--space-8) 0; }
.page-header h1 { font-size: var(--text-3xl); font-weight: var(--font-weight-extrabold); margin: 0 0 var(--space-6); }
.search-box { margin-bottom: var(--space-6); max-width: 600px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: var(--space-4); }
.empty-wrap { padding: var(--space-10) 0; }
.suggestions-block h3 { font-size: var(--text-lg); margin: 0 0 var(--space-3); }
.chips { display: flex; gap: var(--space-2); flex-wrap: wrap; margin-bottom: var(--space-4); }
.chip { padding: 6px 12px; border-radius: var(--radius-full); background: var(--color-deep-violet); border: 1px solid var(--color-border); color: var(--color-lavender); cursor: pointer; font-size: var(--text-sm); }
.chip:hover { border-color: var(--color-primary-purple); }
.hint { color: var(--color-secondary-text); font-size: var(--text-sm); }
</style>
