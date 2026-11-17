<template>
  <footer class="footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <img src="/logo.png" alt="CineRwa" height="36" />
        <p class="footer-tagline">Your World of Cinema.</p>
      </div>
      <div class="footer-links">
        <router-link to="/">Home</router-link>
        <router-link to="/movies">Movies</router-link>
        <router-link to="/series">Series</router-link>
        <router-link to="/about">About</router-link>
      </div>
      <div class="footer-legal">
        <p>© 2026 CineRwa. Content is provided through authorized sources only.</p>
        <p class="attribution">Movie metadata powered by TMDB (attribution required in production). Images are placeholders.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: var(--color-deep-violet);
  border-top: 1px solid var(--color-border);
  padding: var(--space-10) 0 var(--space-6);
  margin-top: var(--space-12);
}
.footer-inner {
  display: grid;
  gap: var(--space-6);
}
.footer-tagline {
  color: var(--color-secondary-text);
  margin: var(--space-2) 0 0;
}
.footer-links {
  display: flex;
  gap: var(--space-4);
  flex-wrap: wrap;
}
.footer-links a {
  color: var(--color-secondary-text);
  font-size: var(--text-sm);
}
.footer-links a:hover {
  color: var(--color-white);
}
.footer-legal {
  color: var(--color-secondary-text);
  font-size: var(--text-xs);
}
.attribution {
  opacity: 0.7;
}
</style>
