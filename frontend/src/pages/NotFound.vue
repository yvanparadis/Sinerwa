<template>
  <div class="page">
    <div class="container notfound">
      <h1>404</h1>
      <p>This page doesn't exist.</p>
      <router-link to="/" class="btn btn-primary">Go Home</router-link>
    </div>
  </div>
</template>

<style scoped>
.page { padding: var(--space-16) 0; }
.notfound { text-align: center; }
.notfound h1 { font-size: 6rem; margin: 0; color: var(--color-primary-purple); }
.notfound p { color: var(--color-secondary-text); margin: 0 0 var(--space-6); }
</style>
