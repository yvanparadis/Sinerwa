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
            <span v-if="item.runtime">{{ item.runtime }} min</span>
            <span v-if="item.language">{{ item.language }}</span>
          </div>
          <div class="genres">
            <span v-for="g in item.genres" :key="g" class="genre-chip">{{ g }}</span>
          </div>
          <div v-if="item.translator" class="translator-info">
            <span class="label">Translated by:</span>
            <span class="value">{{ item.translator }}</span>
            <span class="note">(Agasobanuye — explained in Kinyarwanda)</span>
          </div>
          <div class="playback-info">
            <span class="label">Playback:</span>
            <span class="value">{{ item.playbackType || 'METADATA_ONLY' }}</span>
            <span class="note">· {{ item.availabilityStatus || 'unknown' }}</span>
          </div>
          <p class="overview">{{ item.overview }}</p>

          <div class="cast">
            <h3>Cast</h3>
            <div class="cast-list">
              <span v-for="c in cast" :key="c" class="cast-chip">{{ c }}</span>
            </div>
          </div>

          <div class="viewing-options">
            <h3>Authorized Viewing Options</h3>
            <p class="vo-note">CineRwa only links to or embeds content through authorized providers.</p>
            <div class="vo-list">
              <div class="vo-item">
                <span class="vo-name">CineRwa Source</span>
                <span class="badge">Pending</span>
                <span class="vo-status">No authorized stream available.</span>
              </div>
            </div>
          </div>

          <div class="actions">
            <AppButton variant="primary" @click="watch">Watch</AppButton>
            <AppButton variant="ghost" @click="watchTrailer">Play Trailer</AppButton>
            <AppButton variant="ghost" @click="toggleList">{{ inList ? '✓ In My List' : '+ My List' }}</AppButton>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      <section class="section" v-if="trailer">
        <h2>Trailer</h2>
        <div class="trailer-wrap">
          <iframe :src="trailer" title="Trailer" frameborder="0" allowfullscreen></iframe>
        </div>
      </section>
      <section class="section" v-else>
        <h2>Trailer</h2>
        <p class="no-trailer">No verified trailer available for this title.</p>
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
import { movieService } from "@/services/movieService";
import { useWatchlistStore } from "@/stores/watchlist";

const route = useRoute();
const router = useRouter();
const watchlist = useWatchlistStore();
const item = ref(null);

const cast = ["Amina Uwase", "Jean Bosco", "Grace Mutoni", "Eric Habimana"];
const trailer = ref(null);
const trailerStatus = ref("not_found");

const inList = computed(() => (item.value ? watchlist.contains(item.value.id) : false));

onMounted(async () => {
  item.value = await movieService.getMovieById(route.params.id);
  const API = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
  try {
    const res = await fetch(`${API}/api/v1/trailers/${encodeURIComponent(route.params.id)}`);
    if (res.ok) {
      const data = await res.json();
      if (data.trailer && data.trailer.embed_url) {
        trailer.value = data.trailer.embed_url;
        trailerStatus.value = data.status || "verified";
      } else {
        trailerStatus.value = "not_found";
      }
    }
  } catch (e) {}
});

function watch() {
  if (item.value) router.push({ name: "Watch", params: { id: item.value.id } });
}
function watchTrailer() {
  const el = document.querySelector(".trailer-wrap");
  if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
}
function toggleList() {
  if (item.value) watchlist.toggle(item.value);
}
</script>

<style scoped>
.page { padding-bottom: var(--space-12); }
.details-hero { position: relative; background-size: cover; background-position: center; padding: var(--space-12) 0; margin-bottom: var(--space-8); }
.details-overlay { position: absolute; inset: 0; background: linear-gradient(to right, rgba(9,9,13,0.95) 0%, rgba(9,9,13,0.6) 60%, rgba(9,9,13,0.3) 100%); }
.details-content { position: relative; z-index: 2; display: grid; grid-template-columns: 240px 1fr; gap: var(--space-8); align-items: end; }
.details-poster { width: 100%; border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); border: 1px solid var(--color-border); }
.details-info h1 { font-size: var(--text-4xl); font-weight: var(--font-weight-extrabold); margin: 0 0 var(--space-3); }
.meta { display: flex; gap: var(--space-4); color: var(--color-lavender); font-size: var(--text-sm); margin-bottom: var(--space-3); flex-wrap: wrap; }
.genres { display: flex; gap: var(--space-2); flex-wrap: wrap; margin-bottom: var(--space-4); }
.genre-chip { padding: 4px 10px; border-radius: var(--radius-full); background: rgba(139,92,246,0.15); border: 1px solid var(--color-border); font-size: var(--text-xs); color: var(--color-lavender); }
.translator-info { display: flex; align-items: center; gap: var(--space-2); flex-wrap: wrap; margin-bottom: var(--space-4); padding: var(--space-2) var(--space-3); background: rgba(139,92,246,0.1); border: 1px solid var(--color-border); border-radius: var(--radius-md); font-size: var(--text-sm); }
.translator-info .label { color: var(--color-lavender); font-weight: var(--font-weight-semibold); }
.translator-info .value { color: var(--color-white); font-weight: var(--font-weight-bold); }
.translator-info .note { color: var(--color-secondary-text); font-size: var(--text-xs); }
.playback-info { display: flex; align-items: center; gap: var(--space-2); flex-wrap: wrap; margin-bottom: var(--space-4); font-size: var(--text-sm); color: var(--color-secondary-text); }
.playback-info .label { color: var(--color-lavender); font-weight: var(--font-weight-semibold); }
.playback-info .value { color: var(--color-white); font-weight: var(--font-weight-bold); }
.overview { color: var(--color-secondary-text); max-width: 720px; margin: 0 0 var(--space-6); }
.cast { margin-bottom: var(--space-6); }
.cast h3, .viewing-options h3 { font-size: var(--text-lg); margin: 0 0 var(--space-2); }
.cast-list { display: flex; gap: var(--space-2); flex-wrap: wrap; }
.cast-chip { padding: 4px 10px; background: var(--color-deep-violet); border-radius: var(--radius-full); font-size: var(--text-xs); }
.viewing-options { margin-bottom: var(--space-6); background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: var(--space-4); }
.vo-note { color: var(--color-secondary-text); font-size: var(--text-xs); margin: 0 0 var(--space-3); }
.vo-list { display: flex; flex-direction: column; gap: var(--space-2); }
.vo-item { display: flex; align-items: center; gap: var(--space-3); font-size: var(--text-sm); }
.vo-name { font-weight: var(--font-weight-semibold); }
.vo-status { color: var(--color-secondary-text); font-size: var(--text-xs); }
.actions { display: flex; gap: var(--space-3); flex-wrap: wrap; }
.section { margin: var(--space-8) 0; }
.section h2 { font-size: var(--text-2xl); margin: 0 0 var(--space-4); }
.trailer-wrap { position: relative; padding-bottom: 56.25%; height: 0; border-radius: var(--radius-lg); overflow: hidden; border: 1px solid var(--color-border); }
.trailer-wrap iframe { position: absolute; inset: 0; width: 100%; height: 100%; }
@media (max-width: 700px) { .details-content { grid-template-columns: 1fr; } .details-poster { max-width: 200px; } }
</style>
