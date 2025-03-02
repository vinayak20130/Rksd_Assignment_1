<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  class?: string
}>()

const tableClass = computed(() => {
  return ['w-full caption-bottom text-sm', props.class].filter(Boolean).join(' ')
})
</script>

<template>
  <div class="relative w-full overflow-auto">
    <table :class="tableClass">
      <slot />
    </table>
  </div>
</template>
