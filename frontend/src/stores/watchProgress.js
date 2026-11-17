import { defineStore } from "pinia";
import { ref } from "vue";

const KEY = "cinerwa_watch_progress";

function load() {
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

export const useWatchProgressStore = defineStore("watchProgress", () => {
  const progress = ref(load()); // { [movieId]: { time, duration, updatedAt } }

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(progress.value)); } catch {}
  }

  function update(movieId, time, duration) {
    if (!movieId) return;
    progress.value[movieId] = { time, duration, updatedAt: Date.now() };
    save();
  }

  function get(movieId) {
    return progress.value[movieId] || null;
  }

  function remove(movieId) {
    delete progress.value[movieId];
    save();
  }

  function recent(limit = 12) {
    return Object.entries(progress.value)
      .sort((a, b) => b[1].updatedAt - a[1].updatedAt)
      .slice(0, limit)
      .map(([id, p]) => ({ id, ...p }));
  }

  return { progress, update, get, remove, recent };
});
