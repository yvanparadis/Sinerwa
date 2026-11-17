<template>
  <div class="mobile-menu-overlay" @click="ui.closeMobileMenu">
    <nav class="mobile-menu" @click.stop>
      <div class="mobile-menu-header">
        <img src="/logo-compact.svg" alt="CineRwa" height="28" />
        <button class="btn btn-ghost btn-icon" @click="ui.closeMobileMenu" aria-label="Close">✕</button>
      </div>
      <router-link v-for="l in links" :key="l.to" :to="l.to" class="mobile-link" @click="ui.closeMobileMenu">
        {{ l.label }}
      </router-link>
    </nav>
  </div>
</template>

<script setup>
import { useUIStore } from "@/stores/ui";
const ui = useUIStore();
const links = [
  { to: "/", label: "Home" },
  { to: "/movies", label: "Movies" },
  { to: "/series", label: "Series" },
  { to: "/search", label: "Search" },
  { to: "/my-list", label: "My List" },
  { to: "/about", label: "About" },
];
</script>

<style scoped>
.mobile-menu-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  z-index: 100;
  display: flex;
  justify-content: flex-end;
}
.mobile-menu {
  width: 280px;
  max-width: 85vw;
  background: var(--color-deep-violet);
  height: 100%;
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  border-left: 1px solid var(--color-border);
}
.mobile-menu-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-4);
}
.mobile-link {
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  color: var(--color-white);
  font-weight: var(--font-weight-medium);
}
.mobile-link:hover,
.mobile-link.router-link-active {
  background: var(--color-primary-purple);
}
</style>
