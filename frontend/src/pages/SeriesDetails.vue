<template>
  <div class="page" v-if="item">
    <div class="details-hero" :style="{ backgroundImage: `url(${item.backdrop})` }">
      <div class="details-overlay"></div>
      <div class="container details-content">
        <img class="details-poster" :src="item.poster" :alt="item.title" />
        <div class="details-info">
          <h1>{{ item.title }}</h1>
          <div class="meta">
            <span v-if="item.rating">★ {{ item.rating }}</span>
            <span v-if="item.releaseDate">{{ item.releaseDate.slice(0,4) }}</span>
            <span v-if="item.language">{{ item.language }}</span>
            <span v-if="item.seasons">{{ item.seasons }} season(s)</span>
            <span v-if="item.episodes">{{ item.episodes }} episodes</span>
          </div>
          <div class="genres">
            <span v-for="g in item.genres" :key="g" class="genre-chip">{{ g }}</span>
          </div>
          <p class="overview">{{ item.overview }}</p>
          <div class="actions">
            <AppButton variant="primary" @click="watch">Play Trailer</AppButton>
            <AppButton variant="ghost" @click="toggleList">{{ inList ? '✓ In My List' : '+ My List' }}</AppButton>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      <section class="section">
        <h2>Seasons & Episodes</h2>
        <div class="season-grid">
          <div v-for="s in (item.seasons || 1)" :key="s" class="season-card">
            <h3>Season {{ s }}</h3>
            <p>{{ Math.ceil((item.episodes||6)/(item.seasons||1)) }} episodes</p>
          </div>
        </div>
      </section>
    </div>
  </div>
  <div v-else class="page container">
    <SkeletonBox width="100%" height="400px" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import AppButton from "@/components/common/AppButton.vue";
import SkeletonBox from "@/components/common/SkeletonBox.vue";
import { seriesService } from "@/services/movieService";
import { useWatchlistStore } from "@/stores/watchlist";

const route = useRoute();
const router = useRouter();
const watchlist = useWatchlistStore();
const item = ref(null);

const inList = computed(() => (item.value ? watchlist.contains(item.value.id) : false));

onMounted(async () => {
  item.value = await seriesService.getSeriesById(route.params.id);
});

function watch() {
  if (item.value) router.push({ name: "Watch", params: { id: item.value.id } });
}
function toggleList() {
  if (item.value) watchlist.toggle(item.value);
}
</script>

<style scoped>
.page { padding-bottom: var(--space-12); }
.details-hero {
  position: relative;
  background-size: cover;
  background-position: center;
  padding: var(--space-12) 0;
  margin-bottom: var(--space-8);
}
.details-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to right, rgba(9,9,13,0.95) 0%, rgba(9,9,13,0.6) 60%, rgba(9,9,13,0.3) 100%);
}
.details-content {
  position: relative; z-index: 2;
  display: grid; grid-template-columns: 240px 1fr; gap: var(--space-8); align-items: end;
}
.details-poster {
  width: 100%; border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); border: 1px solid var(--color-border);
}
.details-info h1 { font-size: var(--text-4xl); font-weight: var(--font-weight-extrabold); margin: 0 0 var(--space-3); }
.meta { display: flex; gap: var(--space-4); color: var(--color-lavender); font-size: var(--text-sm); margin-bottom: var(--space-3); flex-wrap: wrap; }
.genres { display: flex; gap: var(--space-2); flex-wrap: wrap; margin-bottom: var(--space-4); }
.genre-chip { padding: 4px 10px; border-radius: var(--radius-full); background: rgba(139,92,246,0.15); border: 1px solid var(--color-border); font-size: var(--text-xs); color: var(--color-lavender); }
.overview { color: var(--color-secondary-text); max-width: 720px; margin: 0 0 var(--space-6); }
.actions { display: flex; gap: var(--space-3); flex-wrap: wrap; }
.section { margin: var(--space-8) 0; }
.section h2 { font-size: var(--text-2xl); margin: 0 0 var(--space-4); }
.season-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px,1fr)); gap: var(--space-4); }
.season-card { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: var(--space-4); }
.season-card h3 { margin: 0 0 var(--space-1); }
.season-card p { color: var(--color-secondary-text); font-size: var(--text-sm); margin: 0; }
@media (max-width: 700px) { .details-content { grid-template-columns: 1fr; } .details-poster { max-width: 200px; } }
</style>
