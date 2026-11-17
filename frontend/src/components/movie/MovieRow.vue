<template>
  <section class="row-section">
    <div class="row-header">
      <h2 class="row-title">{{ title }}</h2>
      <button v-if="seeAllTo" class="btn btn-ghost btn-sm" @click="$router.push(seeAllTo)">See all</button>
    </div>
    <div v-if="loading" class="row">
      <SkeletonBox v-for="n in 6" :key="n" width="160px" height="240px" />
    </div>
    <div v-else-if="error" class="row-error">
      <ErrorState title="Couldn't load" text="Please try again." :retry="true" @retry="$emit('retry')" />
    </div>
    <div v-else-if="!items.length" class="row-empty">
      <EmptyState icon="🎞️" title="No titles" text="Nothing to show yet." />
    </div>
    <div v-else class="row">
      <MovieCard v-for="item in items" :key="item.id" :item="item" />
    </div>
  </section>
</template>

<script setup>
import { useRouter } from "vue-router";
import MovieCard from "@/components/movie/MovieCard.vue";
import SkeletonBox from "@/components/common/SkeletonBox.vue";
import EmptyState from "@/components/common/EmptyState.vue";
import ErrorState from "@/components/common/ErrorState.vue";

defineProps({
  title: { type: String, required: true },
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  error: { type: Boolean, default: false },
  seeAllTo: { type: String, default: "" },
});
defineEmits(["retry"]);

const $router = useRouter();
</script>

<style scoped>
.row-section {
  margin: var(--space-8) 0;
}
.row-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-4);
}
.row-title {
  font-size: var(--text-xl);
  font-weight: var(--font-weight-bold);
  margin: 0;
}
.row-error,
.row-empty {
  padding: var(--space-4) 0;
}
.btn-sm {
  padding: 4px 10px;
  font-size: var(--text-xs);
}
</style>
