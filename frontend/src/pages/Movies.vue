<template>
  <div class="page">
    <div class="container">
      <header class="page-header">
        <h1>Movies</h1>
        <p class="page-sub">Browse the complete CineRwa catalog.</p>
      </header>

      <div class="toolbar">
        <input v-model="query" class="input" placeholder="Search movies..." @input="apply" />
        <select v-model="genre" class="input" @change="apply">
          <option value="">All genres</option>
          <option v-for="g in genres" :key="g.name" :value="g.name">{{ g.name }}</option>
        </select>
        <select v-model="translator" class="input" @change="apply">
          <option value="">All translators</option>
          <option v-for="t in translators" :key="t" :value="t">{{ t }}</option>
        </select>
        <select v-model="language" class="input" @change="apply">
          <option value="">All languages</option>
          <option v-for="l in languages" :key="l" :value="l">{{ l }}</option>
        </select>
        <select v-model="sort" class="input" @change="apply">
          <option value="rating">Top rated</option>
          <option value="newest">Newest</option>
          <option value="title">Title A-Z</option>
        </select>
      </div>

      <div v-if="loading" class="grid">
        <SkeletonBox v-for="n in 12" :key="n" width="100%" height="260px" />
      </div>
      <div v-else-if="filtered.length === 0" class="empty-wrap">
        <EmptyState icon="🔍" title="No matches" text="Try adjusting your filters or search." />
      </div>
      <div v-else class="grid">
        <MovieCard v-for="m in filtered" :key="m.id" :item="m" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import MovieCard from "@/components/movie/MovieCard.vue";
import SkeletonBox from "@/components/common/SkeletonBox.vue";
import EmptyState from "@/components/common/EmptyState.vue";
import { movieService } from "@/services/movieService";
import { translators as allTranslators } from "@/data/movies";
const allGenres = ref([]);

const genres = computed(() => allGenres.value.map((g) => ({ name: typeof g === "string" ? g : (g.name || g) })));
const languages = ["English", "French", "Kinyarwanda", "Swahili", "Spanish"];
const translators = allTranslators;

const all = ref([]);
const loading = ref(true);
const query = ref("");
const genre = ref("");
const translator = ref("");
const language = ref("");
const sort = ref("rating");
const filtered = ref([]);

async function load() {
  loading.value = true;
  const API = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
  try {
    const gRes = await fetch(`${API}/api/v1/genres`);
    if (gRes.ok) {
      const gd = await gRes.json();
      allGenres.value = gd.genres || [];
    }
  } catch (e) {}
  all.value = await movieService.getAllMovies();
  apply();
  loading.value = false;
}
function apply() {
  let r = [...all.value];
  const q = query.value.trim().toLowerCase();
  if (q) {
    r = r.filter(
      (m) =>
        m.title.toLowerCase().includes(q) ||
        m.overview.toLowerCase().includes(q) ||
        m.genres.some((g) => g.toLowerCase().includes(q))
    );
  }
  if (genre.value) r = r.filter((m) => m.genres.includes(genre.value));
  if (translator.value) r = r.filter((m) => m.translator === translator.value);
  if (language.value) r = r.filter((m) => m.language === language.value);
  if (sort.value === "rating") r.sort((a, b) => b.rating - a.rating);
  else if (sort.value === "newest") r.sort((a, b) => new Date(b.releaseDate) - new Date(a.releaseDate));
  else if (sort.value === "title") r.sort((a, b) => a.title.localeCompare(b.title));
  filtered.value = r;
}

onMounted(load);
</script>

<style scoped>
.page {
  padding: var(--space-8) 0;
}
.page-header h1 {
  font-size: var(--text-3xl);
  font-weight: var(--font-weight-extrabold);
  margin: 0 0 var(--space-2);
}
.page-sub {
  color: var(--color-secondary-text);
  margin: 0 0 var(--space-6);
}
.toolbar {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr;
  gap: var(--space-3);
  margin-bottom: var(--space-6);
}
@media (max-width: 768px) {
  .toolbar {
    grid-template-columns: 1fr;
  }
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: var(--space-4);
}
.empty-wrap {
  padding: var(--space-10) 0;
}
</style>
