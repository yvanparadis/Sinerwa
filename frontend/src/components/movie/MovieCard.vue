<template>
  <article class="movie-card" @click="go">
    <img :src="item.poster" :alt="item.title" loading="lazy" decoding="async" />
    <div class="overlay">
      <div class="overlay-title">{{ item.title }}</div>
      <div class="overlay-meta">
        <span>{{ item.releaseDate?.slice(0, 4) }}</span>
        <span v-if="item.rating" class="rating">★ {{ item.rating }}</span>
        <span v-if="item.language" class="lang">{{ item.language }}</span>
        <span v-if="item.translator" class="translator">🎬 {{ item.translator }}</span>
      </div>
      <div class="overlay-actions">
        <button v-if="item.playbackType && item.playbackType !== 'METADATA_ONLY'" class="btn btn-primary btn-sm" @click.stop="play">Watch</button>
        <button v-else class="btn btn-ghost btn-sm" disabled title="No authorized playback source">Unavailable</button>
        <button class="btn btn-ghost btn-sm" @click.stop="go">Details</button>
        <button class="btn btn-ghost btn-icon btn-sm" :class="{ active: inList }" @click.stop="toggleList" :aria-label="inList ? 'Remove from My List' : 'Add to My List'">
          {{ inList ? "✓" : "+" }}
        </button>
      </div>
    </div>
    <div class="title-bar">
      <span class="title-bar-text">{{ item.title }}</span>
    </div>
    <div v-if="item.translator" class="translator-badge" :title="'Translated by ' + item.translator">
      🎬 {{ item.translator }}
    </div>
    <div class="card-badge" v-if="item.contentType === 'series'">Series</div>
  </article>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useWatchlistStore } from "@/stores/watchlist";

const props = defineProps({
  item: { type: Object, required: true },
});
const router = useRouter();
const watchlist = useWatchlistStore();

const inList = computed(() => watchlist.contains(props.item.id));

function go() {
  const name = props.item.contentType === "series" ? "SeriesDetails" : "MovieDetails";
  router.push({ name, params: { id: props.item.id } });
}

function toggleList() {
  watchlist.toggle(props.item);
}
function play() {
  router.push({ name: "Watch", params: { id: props.item.id } });
}
</script>

<style scoped>
.overlay-title {
  font-weight: var(--font-weight-bold);
  font-size: var(--text-sm);
  margin-bottom: var(--space-1);
}
.overlay-meta {
  display: flex;
  gap: var(--space-2);
  font-size: var(--text-xs);
  color: var(--color-secondary-text);
  margin-bottom: var(--space-2);
}
.rating {
  color: var(--color-lavender);
}
.overlay-actions {
  display: flex;
  gap: var(--space-2);
  align-items: center;
}
.btn-sm {
  padding: 4px 10px;
  font-size: var(--text-xs);
}
.card-badge {
  position: absolute;
  top: var(--space-2);
  left: var(--space-2);
  background: rgba(139, 92, 246, 0.85);
  color: #fff;
  font-size: var(--text-xs);
  font-weight: var(--font-weight-bold);
  padding: 2px 8px;
  border-radius: var(--radius-full);
}
button.active {
  background: var(--color-primary-purple);
  border-color: var(--color-primary-purple);
}
</style>

