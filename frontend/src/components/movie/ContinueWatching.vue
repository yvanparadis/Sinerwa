<template>
  <section class="cw-section" v-if="items.length">
    <div class="container">
      <h2 class="section-title">Continue Watching</h2>
      <div class="cw-row">
        <div v-for="item in items" :key="item.id" class="cw-card" @click="go(item)">
          <div class="cw-thumb">
            <img :src="item.poster || '/placeholder-movie.svg'" :alt="item.title" loading="lazy" />
            <div class="cw-progress">
              <div class="cw-bar" :style="{ width: item.percent + '%' }"></div>
            </div>
            <span class="cw-remaining">{{ item.remaining }}</span>
          </div>
          <div class="cw-title">{{ item.title }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
const props = defineProps({ items: { type: Array, default: () => [] } });
const router = useRouter();
function go(item) {
  router.push({ name: "Watch", params: { id: item.id } });
}
</script>

<style scoped>
.cw-section { padding: var(--space-6) 0; }
.section-title { font-size: var(--text-xl); font-weight: var(--font-weight-bold); margin: 0 0 var(--space-3); }
.cw-row { display: flex; gap: var(--space-3); overflow-x: auto; padding-bottom: var(--space-2); scroll-snap-type: x mandatory; }
.cw-card { flex: 0 0 220px; scroll-snap-align: start; cursor: pointer; }
.cw-thumb { position: relative; border-radius: var(--radius-md); overflow: hidden; }
.cw-thumb img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
.cw-progress { position: absolute; left: 0; right: 0; bottom: 0; height: 4px; background: rgba(255,255,255,0.2); }
.cw-bar { height: 100%; background: var(--color-primary-purple); }
.cw-remaining { position: absolute; right: var(--space-2); bottom: var(--space-2); background: rgba(0,0,0,0.7); color: #fff; font-size: 10px; padding: 2px 6px; border-radius: var(--radius-sm); }
.cw-title { margin-top: var(--space-2); font-size: var(--text-sm); font-weight: var(--font-weight-semibold); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
</style>
