<template>
  <div class="home">
    <HeroSlider :slides="slides" />
    <ContinueWatching :items="continueWatching" />
    <div class="container">
      <Top10 :items="top10" />
      <MovieRow v-if="trending.length" title="Trending Now" :items="trending" :loading="loading" :error="error" see-all-to="/movies" @retry="load" />
      <MovieRow v-if="popular.length" title="Popular Movies" :items="popular" :loading="loading" see-all-to="/movies" />
      <MovieRow v-if="recent.length" title="Recently Added" :items="recent" :loading="loading" />
      <MovieRow v-if="recommended.length" title="Recommended For You" :items="recommended" :loading="loading" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import HeroSlider from "@/components/movie/HeroSlider.vue";
import MovieRow from "@/components/movie/MovieRow.vue";
import Top10 from "@/components/movie/Top10.vue";
import ContinueWatching from "@/components/movie/ContinueWatching.vue";
import { useWatchProgressStore } from "@/stores/watchProgress";
import { movieService } from "@/services/movieService";

const all = ref([]);
const trending = ref([]);
const popular = ref([]);
const recent = ref([]);
const recommended = ref([]);
const progressStore = useWatchProgressStore();
const top10 = computed(() => [...all.value].sort((a, b) => (b.rating || 0) - (a.rating || 0)).slice(0, 10));
const continueWatching = computed(() => {
  const map = new Map(all.value.map((m) => [m.id, m]));
  return progressStore.recent(12).map((p) => {
    const m = map.get(p.id);
    if (!m) return null;
    const percent = p.duration ? Math.min(100, (p.time / p.duration) * 100) : 0;
    const remaining = p.duration ? formatTime(p.duration - p.time) : "";
    return { ...m, percent, remaining };
  }).filter(Boolean);
});

function formatTime(t) {
  if (!t || isNaN(t)) return "0:00";
  const m = Math.floor(t / 60);
  const s = Math.floor(t % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}
const loading = ref(true);
const error = ref(false);

const slides = computed(() => {
  if (!all.value.length) return [];
  const sorted = [...all.value].sort((a, b) => (b.rating || 0) - (a.rating || 0));
  const possibleLove = all.value.find((m) => (m.title || "").toLowerCase() === "possible love");
  const others = sorted.filter((m) => (m.title || "").toLowerCase() !== "possible love").slice(0, 7);
  const result = [];
  if (possibleLove) result.push(possibleLove);
  result.push(...others);
  return result.slice(0, 8);
});

async function load() {
  loading.value = true;
  error.value = false;
  try {
    const API = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
    const [a, t, p, r] = await Promise.all([
      movieService.getAllMovies(),
      movieService.getTrending(),
      movieService.getPopular(),
      movieService.getRecentlyAdded(),
    ]);
    // Extra sections from TMDB
    let topRated = [];
    let upcoming = [];
    try {
      const tr = await fetch(`${API}/api/v1/tmdb/top_rated`);
      if (tr.ok) { const d = await tr.json(); topRated = d.results || []; }
    } catch (e) {}
    try {
      const up = await fetch(`${API}/api/v1/tmdb/upcoming`);
      if (up.ok) { const d = await up.json(); upcoming = d.results || []; }
    } catch (e) {}
    // recommendations from backend
    let rec = [];
    try {
      const res = await fetch((import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000") + "/api/v1/recommendations");
      if (res.ok) {
        const d = await res.json();
        rec = d.items || [];
      }
    } catch (e) { /* ignore */ }
    if (!rec.length) rec = a.slice(2, 10);
    all.value = a;
    trending.value = t;
    popular.value = p;
    recent.value = r;
    recommended.value = rec;
  } catch (e) {
    error.value = true;
  } finally {
    loading.value = false;
  }
}

onMounted(load);
</script>
