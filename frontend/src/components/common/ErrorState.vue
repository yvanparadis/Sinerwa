<template>
  <div class="error-state">
    <div class="error-icon">⚠️</div>
    <h3 class="error-title">{{ title }}</h3>
    <p class="error-text">{{ text }}</p>
    <button v-if="retry" class="btn btn-primary" @click="$emit('retry')">Try again</button>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: "Something went wrong" },
  text: { type: String, default: "We couldn't load this content. Please try again." },
  retry: { type: Boolean, default: false },
});
defineEmits(["retry"]);
</script>

<style scoped>
.error-state {
  text-align: center;
  padding: var(--space-12) var(--space-6);
  color: var(--color-secondary-text);
}
.error-icon {
  font-size: 2.5rem;
  margin-bottom: var(--space-4);
  color: var(--color-danger);
}
.error-title {
  color: var(--color-white);
  font-size: var(--text-xl);
  font-weight: var(--font-weight-bold);
  margin: 0 0 var(--space-2);
}
.error-text {
  margin: 0 auto var(--space-6);
  max-width: 420px;
}
</style>
