<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  class?: string
}>()

const cellClass = computed(() => {
  return ['p-4 align-middle [&:has([role=checkbox])]:pr-0', props.class].filter(Boolean).join(' ')
})
</script>

<template>
  <td :class="cellClass">
    <slot />
  </td>
</template>
