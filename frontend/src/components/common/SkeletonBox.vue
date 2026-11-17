<template>
  <div class="skeleton" :style="{ width, height, borderRadius }"></div>
</template>

<script setup>
defineProps({
  width: { type: String, default: "100%" },
  height: { type: String, default: "16px" },
  borderRadius: { type: String, default: "var(--radius-md)" },
});
</script>
