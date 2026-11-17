<template>
  <section class="hero-slider" v-if="slides.length">
    <div class="hero-slide" :style="{ backgroundImage: `url(${current.backdrop || current.poster})` }">
      <div class="hero-gradient"></div>
      <div class="container hero-content">
        <div class="hero-text">
          <span class="badge">Top Movie</span>
          <h1 class="hero-title">{{ current.title }}</h1>
          <p class="hero-overview">{{ current.overview }}</p>
          <div class="hero-meta">
            <span v-if="current.rating">★ {{ current.rating }}</span>
            <span v-if="current.releaseDate">{{ String(current.releaseDate).slice(0,4) }}</span>
            <span v-if="current.runtime">{{ current.runtime }} min</span>
          </div>
          <div class="hero-genres">
            <span v-for="g in (current.genres || [])" :key="g" class="genre-chip">{{ g }}</span>
          </div>
          <div class="hero-actions">
            <AppButton variant="primary" @click="watch(current)">Watch</AppButton>
            <AppButton variant="ghost" @click="details(current)">Details</AppButton>
          </div>
        </div>
      </div>
    </div>
    <button class="slider-btn prev" @click="prev" aria-label="Previous">‹</button>
    <button class="slider-btn next" @click="next" aria-label="Next">›</button>
    <div class="slider-dots">
      <button
        v-for="(s, i) in slides"
        :key="i"
        class="dot"
        :class="{ active: i === index }"
        @click="index = i"
        :aria-label="`Slide ${i + 1}`"
      ></button>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import AppButton from "@/components/common/AppButton.vue";

const props = defineProps({
  slides: { type: Array, default: () => [] },
});
const router = useRouter();
const index = ref(0);
const current = computed(() => props.slides[index.value] || props.slides[0]);
let timer = null;

function next() {
  index.value = (index.value + 1) % props.slides.length;
}
function prev() {
  index.value = (index.value - 1 + props.slides.length) % props.slides.length;
}
function watch(item) {
  if (item && item.id) router.push({ name: "Watch", params: { id: item.id } });
}
function details(item) {
  if (item && item.id) {
    const name = item.contentType === "series" ? "SeriesDetails" : "MovieDetails";
    router.push({ name, params: { id: item.id } });
  }
}

onMounted(() => {
  timer = setInterval(next, 6000);
});
onBeforeUnmount(() => {
  clearInterval(timer);
});
</script>

<style scoped>
.hero-slider { position: relative; margin-bottom: var(--space-8); }
.hero-slide {
  position: relative;
  min-height: 70vh;
  display: flex;
  align-items: center;
  overflow: hidden;
  background-size: cover;
  background-position: center;
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
  padding-top: var(--space-12);
  padding-bottom: var(--space-12);
  max-width: 640px;
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
.slider-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 5;
  background: rgba(9,9,13,0.6);
  border: 1px solid var(--color-border);
  color: var(--color-white);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.slider-btn.prev { left: var(--space-4); }
.slider-btn.next { right: var(--space-4); }
.slider-btn:hover { background: var(--color-primary-purple); }
.slider-dots {
  position: absolute;
  bottom: var(--space-4);
  left: 50%;
  transform: translateX(-50%);
  z-index: 5;
  display: flex;
  gap: var(--space-2);
}
.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255,255,255,0.3);
  border: none;
  cursor: pointer;
  padding: 0;
}
.dot.active { background: var(--color-primary-purple); }
@media (max-width: 900px) {
  .hero-title { font-size: var(--text-3xl); }
}
</style>
