<template>
  <section class="hero" v-if="item">
    <div class="hero-bg" :style="{ backgroundImage: `url(${item.backdrop})` }"></div>
    <div class="hero-gradient"></div>
    <div class="container hero-content">
      <div class="hero-text">
        <span class="badge">Featured</span>
        <h1 class="hero-title">{{ item.title }}</h1>
        <p class="hero-overview">{{ item.overview }}</p>
        <div class="hero-meta">
          <span v-if="item.rating">★ {{ item.rating }}</span>
          <span v-if="item.releaseDate">{{ item.releaseDate.slice(0, 4) }}</span>
          <span v-if="item.runtime">{{ item.runtime }} min</span>
          <span v-if="item.language">{{ item.language }}</span>
        </div>
        <div class="hero-genres">
          <span v-for="g in item.genres" :key="g" class="genre-chip">{{ g }}</span>
        </div>
        <div class="hero-actions">
          <AppButton variant="primary" @click="goDetails">View Details</AppButton>
          <AppButton variant="ghost" @click="toggleList">
            {{ inList ? "✓ In My List" : "+ My List" }}
          </AppButton>
        </div>
      </div>
      <div class="hero-poster">
        <img :src="item.poster" :alt="item.title" />
      </div>
    </div>
  </section>
  <section v-else class="hero hero-skeleton">
    <div class="container">
      <SkeletonBox width="60%" height="48px" />
      <div style="margin-top:16px"><SkeletonBox width="80%" height="16px" /></div>
      <div style="margin-top:8px"><SkeletonBox width="70%" height="16px" /></div>
    </div>
  </section>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useWatchlistStore } from "@/stores/watchlist";
import AppButton from "@/components/common/AppButton.vue";
import SkeletonBox from "@/components/common/SkeletonBox.vue";

const props = defineProps({ item: { type: Object, default: null } });
const router = useRouter();
const watchlist = useWatchlistStore();
const inList = computed(() => (props.item ? watchlist.contains(props.item.id) : false));

function goDetails() {
  if (!props.item) return;
  const name = props.item.contentType === "series" ? "SeriesDetails" : "MovieDetails";
  router.push({ name, params: { id: props.item.id } });
}
function toggleList() {
  if (props.item) watchlist.toggle(props.item);
}
</script>

<style scoped>
.hero {
  position: relative;
  min-height: 70vh;
  display: flex;
  align-items: center;
  overflow: hidden;
  margin-bottom: var(--space-8);
}
.hero-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  filter: brightness(0.35);
}
.hero-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, var(--color-midnight) 0%, rgba(9,9,13,0.6) 50%, transparent 100%),
              linear-gradient(to top, var(--color-midnight) 0%, transparent 40%);
}
.hero-content {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: 1.4fr 0.6fr;
  gap: var(--space-8);
  align-items: center;
  padding-top: var(--space-12);
  padding-bottom: var(--space-12);
}
.hero-title {
  font-size: var(--text-5xl);
  font-weight: var(--font-weight-extrabold);
  margin: var(--space-3) 0;
  line-height: 1.05;
}
.hero-overview {
  color: var(--color-secondary-text);
  font-size: var(--text-lg);
  max-width: 620px;
  margin: 0 0 var(--space-4);
}
.hero-meta {
  display: flex;
  gap: var(--space-4);
  color: var(--color-lavender);
  font-size: var(--text-sm);
  margin-bottom: var(--space-3);
}
.hero-genres {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
  margin-bottom: var(--space-6);
}
.genre-chip {
  padding: 4px 10px;
  border-radius: var(--radius-full);
  background: rgba(139, 92, 246, 0.15);
  border: 1px solid var(--color-border);
  font-size: var(--text-xs);
  color: var(--color-lavender);
}
.hero-actions {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
}
.hero-poster {
  justify-self: end;
}
.hero-poster img {
  width: 260px;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--color-border);
}
@media (max-width: 900px) {
  .hero-content {
    grid-template-columns: 1fr;
  }
  .hero-poster {
    display: none;
  }
  .hero-title {
    font-size: var(--text-3xl);
  }
}
.hero-skeleton {
  min-height: 40vh;
}
</style>
