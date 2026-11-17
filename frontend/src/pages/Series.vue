<template>
  <div class="page">
    <div class="container">
      <header class="page-header">
        <h1>Series</h1>
        <p class="page-sub">Discover television series from Rwanda and beyond.</p>
      </header>
      <div v-if="loading" class="grid">
        <SkeletonBox v-for="n in 8" :key="n" width="100%" height="260px" />
      </div>
      <div v-else-if="items.length === 0" class="empty-wrap">
        <EmptyState icon="📺" title="No series yet" text="Check back soon." />
      </div>
      <div v-else class="grid">
        <MovieCard v-for="s in items" :key="s.id" :item="s" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import MovieCard from "@/components/movie/MovieCard.vue";
import SkeletonBox from "@/components/common/SkeletonBox.vue";
import EmptyState from "@/components/common/EmptyState.vue";
import { seriesService } from "@/services/movieService";

const items = ref([]);
const loading = ref(true);

onMounted(async () => {
  items.value = await seriesService.getAllSeries();
  loading.value = false;
});
</script>

<style scoped>
.page { padding: var(--space-8) 0; }
.page-header h1 { font-size: var(--text-3xl); font-weight: var(--font-weight-extrabold); margin: 0 0 var(--space-2); }
.page-sub { color: var(--color-secondary-text); margin: 0 0 var(--space-6); }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: var(--space-4); }
.empty-wrap { padding: var(--space-10) 0; }
</style>
