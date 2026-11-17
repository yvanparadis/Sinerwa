<template>
  <button :class="classes" :disabled="disabled" @click="$emit('click', $event)">
    <slot />
  </button>
</template>

<script setup>
import { computed } from "vue";
const props = defineProps({
  variant: { type: String, default: "primary" },
  size: { type: String, default: "md" },
  disabled: { type: Boolean, default: false },
  block: { type: Boolean, default: false },
});
defineEmits(["click"]);

const classes = computed(() => {
  const base = "btn";
  const v = `btn-${props.variant}`;
  const b = props.block ? "btn-block" : "";
  return [base, v, b].join(" ");
});
</script>

<style scoped>
.btn-block {
  width: 100%;
}
</style>
