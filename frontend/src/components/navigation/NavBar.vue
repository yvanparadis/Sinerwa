<template>
  <header class="navbar">
    <div class="container nav-inner">
      <router-link to="/" class="brand">
        <img src="/logo-compact.svg" alt="CineRwa" class="brand-logo" />
      </router-link>

      <nav class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/movies" class="nav-link">Movies</router-link>
        <router-link to="/series" class="nav-link">Series</router-link>
        <router-link to="/search" class="nav-link">Search</router-link>
        <router-link to="/my-list" class="nav-link">My List</router-link>
        <router-link to="/about" class="nav-link">About</router-link>
        <router-link to="/providers" class="nav-link">Providers</router-link>
        <router-link to="/storage" class="nav-link">Storage</router-link>
      </nav>

      <div class="nav-actions">
        <router-link to="/search" class="btn btn-ghost btn-icon" aria-label="Search">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        </router-link>
        <router-link to="/my-list" class="btn btn-ghost btn-icon" aria-label="My List">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
          <span v-if="watchlist.count" class="badge-count">{{ watchlist.count }}</span>
        </router-link>
        <template v-if="auth.isAuthenticated">
          <span class="user-name">{{ auth.user?.username }}</span>
          <button class="btn btn-ghost btn-sm" @click="auth.logout()">Sign out</button>
        </template>
        <template v-else>
          <router-link to="/login" class="btn btn-ghost btn-sm">Sign in</router-link>
          <router-link to="/register" class="btn btn-primary btn-sm">Register</router-link>
        </template>
        <button class="btn btn-ghost btn-icon mobile-toggle" @click="ui.toggleMobileMenu" aria-label="Menu">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useWatchlistStore } from "@/stores/watchlist";
import { useUIStore } from "@/stores/ui";
import { useAuthStore } from "@/stores/auth";
const watchlist = useWatchlistStore();
const ui = useUIStore();
const auth = useAuthStore();
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(9, 9, 13, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border);
  height: var(--nav-height);
}
.nav-inner {
  height: 100%;
  display: flex;
  align-items: center;
  gap: var(--space-6);
}
.brand-logo {
  height: 32px;
}
.nav-links {
  display: flex;
  gap: var(--space-1);
  flex: 1;
}
.nav-link {
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-secondary-text);
  transition: all var(--transition-fast);
}
.nav-link:hover,
.nav-link.router-link-active {
  color: var(--color-white);
  background: var(--color-deep-violet);
}
.nav-actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  position: relative;
}
.badge-count {
  position: absolute;
  top: -4px;
  right: -4px;
  background: var(--color-primary-purple);
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  min-width: 16px;
  height: 16px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
}
.mobile-toggle {
  display: none;
}
@media (max-width: 768px) {
  .nav-links {
    display: none;
  }
  .mobile-toggle {
    display: inline-flex;
  }
}
</style>
