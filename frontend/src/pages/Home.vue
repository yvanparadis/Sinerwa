<template>
  <div class="home">
    <HeroSlider :slides="slides" />
    <div class="container">
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
import { movieService } from "@/services/movieService";

const all = ref([]);
const trending = ref([]);
const popular = ref([]);
const recent = ref([]);
const recommended = ref([]);
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
    const [a, t, p, r, rec] = await Promise.all([
      movieService.getAllMovies(),
      movieService.getTrending(),
      movieService.getPopular(),
      movieService.getRecentlyAdded(),
      movieService.getRecommended(),
    ]);
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
