<template>
  <section class="top10-section" v-if="items.length">
    <div class="container">
      <div class="top10-header">
        <span class="top10-big">TOP 10</span>
        <span class="top10-sub">CONTENTS TODAY</span>
      </div>
      <div class="top10-row">
        <div v-for="(item, i) in items" :key="item.id" class="top10-card" @click="go(item)">
          <span class="rank">{{ i + 1 }}</span>
          <img :src="item.poster" :alt="item.title" loading="lazy" decoding="async" />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from "vue-router";
const props = defineProps({ items: { type: Array, default: () => [] } });
const router = useRouter();
function go(item) {
  const name = item.contentType === "series" ? "SeriesDetails" : "MovieDetails";
  router.push({ name, params: { id: item.id } });
}
</script>

<style scoped>
.top10-section { padding: var(--space-8) 0; }
.top10-header { display: flex; align-items: baseline; gap: var(--space-3); margin-bottom: var(--space-4); }
.top10-big {
  font-size: 4rem;
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 2px var(--color-primary-purple);
  letter-spacing: 2px;
  line-height: 1;
}
.top10-sub {
  font-size: var(--text-sm);
  letter-spacing: 4px;
  color: var(--color-secondary-text);
  font-weight: var(--font-weight-bold);
}
.top10-row {
  display: flex;
  gap: var(--space-4);
  overflow-x: auto;
  padding-bottom: var(--space-2);
  scroll-snap-type: x mandatory;
}
.top10-card {
  position: relative;
  flex: 0 0 150px;
  cursor: pointer;
  scroll-snap-align: start;
  transition: transform var(--transition-base);
}
.top10-card:hover { transform: scale(1.05); }
.top10-card img {
  width: 100%;
  aspect-ratio: 2 / 3;
  object-fit: cover;
  border-radius: var(--radius-md);
}
.rank {
  position: absolute;
  left: -12px;
  bottom: 0;
  font-size: 5rem;
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 2px var(--color-primary-purple);
  line-height: 0.8;
  z-index: 2;
  pointer-events: none;
}
</style>

