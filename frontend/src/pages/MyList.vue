<template>
  <div class="page">
    <div class="container">
      <header class="page-header">
        <h1>My List</h1>
        <p class="page-sub">Your saved movies and series.</p>
      </header>

      <div v-if="watchlist.items.length === 0" class="empty-wrap">
        <EmptyState icon="📌" title="Your list is empty" text="Save movies and series to watch later." />
        <router-link to="/movies" class="btn btn-primary">Browse movies</router-link>
      </div>
      <div v-else>
        <div class="list-header">
          <span>{{ watchlist.count }} saved</span>
          <button class="btn btn-ghost" @click="watchlist.clear()">Clear all</button>
        </div>
        <div class="grid">
          <MovieCard v-for="item in watchlist.items" :key="item.id" :item="item" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useWatchlistStore } from "@/stores/watchlist";
import MovieCard from "@/components/movie/MovieCard.vue";
import EmptyState from "@/components/common/EmptyState.vue";

const watchlist = useWatchlistStore();
</script>

<style scoped>
.page { padding: var(--space-8) 0; }
.page-header h1 { font-size: var(--text-3xl); font-weight: var(--font-weight-extrabold); margin: 0 0 var(--space-2); }
.page-sub { color: var(--color-secondary-text); margin: 0 0 var(--space-6); }
.empty-wrap { text-align: center; padding: var(--space-10) 0; display: flex; flex-direction: column; align-items: center; gap: var(--space-4); }
.list-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--space-4); color: var(--color-secondary-text); font-size: var(--text-sm); }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: var(--space-4); }
</style>
