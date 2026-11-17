<template>
  <div class="empty-state">
    <div class="empty-icon">{{ icon }}</div>
    <h3 class="empty-title">{{ title }}</h3>
    <p class="empty-text">{{ text }}</p>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  icon: { type: String, default: "🎬" },
  title: { type: String, default: "Nothing here yet" },
  text: { type: String, default: "" },
});
</script>

<style scoped>
.empty-state {
  text-align: center;
  padding: var(--space-12) var(--space-6);
  color: var(--color-secondary-text);
}
.empty-icon {
  font-size: 3rem;
  margin-bottom: var(--space-4);
}
.empty-title {
  color: var(--color-white);
  font-size: var(--text-xl);
  font-weight: var(--font-weight-bold);
  margin: 0 0 var(--space-2);
}
.empty-text {
  margin: 0 auto var(--space-6);
  max-width: 420px;
}
</style>
