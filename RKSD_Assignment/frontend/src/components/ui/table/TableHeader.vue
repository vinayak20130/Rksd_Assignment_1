<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  class?: string
}>()

const headerClass = computed(() => {
  return ['[&_tr]:border-b', props.class].filter(Boolean).join(' ')
})
</script>

<template>
  <thead :class="headerClass">
    <slot />
  </thead>
</template>
