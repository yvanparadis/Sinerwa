<template>
  <div class="page">
    <div class="container">
      <div class="watch-header">
        <router-link to="/" class="back-link">← Back</router-link>
        <h1 v-if="item">{{ item.title }}</h1>
      </div>

      <div v-if="!item" class="page container">
        <SkeletonBox width="100%" height="400px" />
      </div>

      <div v-else-if="isLocal" class="player-wrap">
        <VideoPlayer :src="videoSrc" :poster="item.backdrop" />
      </div>

      <div v-else-if="isExternalUrl" class="external-wrap">
        <p>This movie is available from an authorized external provider.</p>
        <a :href="item.externalWatchUrl" target="_blank" rel="noopener" class="btn btn-primary">Open External Player</a>
      </div>

      <div v-else-if="isEmbed" class="embed-wrap">
        <iframe :src="item.externalWatchUrl" title="Player" frameborder="0" allowfullscreen></iframe>
      </div>

      <div v-else class="unavailable-wrap">
        <EmptyState icon="🚫" title="Playback unavailable" text="This title does not have an authorized playable source." />
      </div>

      <div v-if="item" class="details-below">
        <p class="overview">{{ item.overview }}</p>
        <div class="meta">
          <span v-if="item.rating">★ {{ item.rating }}</span>
          <span v-if="item.releaseDate">{{ String(item.releaseDate).slice(0,4) }}</span>
          <span v-if="item.runtime">{{ item.runtime }} min</span>
          <span v-if="item.translator">Translated by {{ item.translator }}</span>
        </div>
        <div class="playback-status">
          Playback type: <strong>{{ item.playbackType || 'METADATA_ONLY' }}</strong> ·
          Availability: <strong>{{ item.availabilityStatus || 'unknown' }}</strong>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import VideoPlayer from "@/components/player/VideoPlayer.vue";
import SkeletonBox from "@/components/common/SkeletonBox.vue";
import EmptyState from "@/components/common/EmptyState.vue";
import { movieService } from "@/services/movieService";

const route = useRoute();
const item = ref(null);
const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

const isLocal = computed(() => item.value && item.value.playbackType === "LOCAL_FILE");
const isExternalUrl = computed(() => item.value && item.value.playbackType === "AUTHORIZED_EXTERNAL_URL");
const isEmbed = computed(() => item.value && item.value.playbackType === "AUTHORIZED_EMBED");

const videoSrc = computed(() => {
  if (!item.value) return "";
  if (item.value.externalWatchUrl && item.value.externalWatchUrl.startsWith("/")) {
    return `${API_BASE}${item.value.externalWatchUrl}`;
  }
  return item.value.externalWatchUrl || "";
});

onMounted(async () => {
  item.value = await movieService.getMovieById(route.params.id);
});
</script>

<style scoped>
.page { padding: var(--space-6) 0 var(--space-12); }
.watch-header { display: flex; align-items: center; gap: var(--space-4); margin-bottom: var(--space-4); }
.watch-header h1 { font-size: var(--text-2xl); margin: 0; }
.back-link { color: var(--color-secondary-text); font-size: var(--text-sm); }
.back-link:hover { color: var(--color-white); }
.player-wrap { margin-bottom: var(--space-4); }
.external-wrap, .embed-wrap, .unavailable-wrap { text-align: center; padding: var(--space-10) 0; display: flex; flex-direction: column; align-items: center; gap: var(--space-4); }
.embed-wrap iframe { width: 100%; max-width: 900px; aspect-ratio: 16/9; border-radius: var(--radius-lg); border: 1px solid var(--color-border); }
.details-below .overview { color: var(--color-secondary-text); max-width: 720px; }
.meta { display: flex; gap: var(--space-4); color: var(--color-lavender); font-size: var(--text-sm); margin-top: var(--space-2); flex-wrap: wrap; }
.playback-status { margin-top: var(--space-3); font-size: var(--text-xs); color: var(--color-secondary-text); }
</style>
