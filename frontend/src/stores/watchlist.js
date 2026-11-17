import { defineStore } from "pinia";
import { ref, computed } from "vue";

const STORAGE_KEY = "cinerwa_watchlist";

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export const useWatchlistStore = defineStore("watchlist", () => {
  const items = ref(load());

  const count = computed(() => items.value.length);

  function persist() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(items.value));
    } catch {
      /* ignore */
    }
  }

  function add(item) {
    if (!items.value.find((i) => i.id === item.id)) {
      items.value.unshift({ ...item, savedAt: new Date().toISOString() });
      persist();
    }
  }

  function remove(id) {
    items.value = items.value.filter((i) => i.id !== id);
    persist();
  }

  function toggle(item) {
    if (items.value.find((i) => i.id === item.id)) {
      remove(item.id);
      return false;
    }
    add(item);
    return true;
  }

  function contains(id) {
    return items.value.some((i) => i.id === id);
  }

  function clear() {
    items.value = [];
    persist();
  }

  return { items, count, add, remove, toggle, contains, clear };
});
