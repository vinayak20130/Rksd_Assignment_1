<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  class?: string
}>()

const bodyClass = computed(() => {
  return ['[&_tr:last-child]:border-0', props.class].filter(Boolean).join(' ')
})
</script>

<template>
  <tbody :class="bodyClass">
    <slot />
  </tbody>
</template>
