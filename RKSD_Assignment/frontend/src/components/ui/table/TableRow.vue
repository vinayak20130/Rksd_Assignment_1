<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  class?: string
}>()

const rowClass = computed(() => {
  return [
    'border-b transition-colors hover:bg-[#262626] data-[state=selected]:bg-[#262626]',
    props.class,
  ]
    .filter(Boolean)
    .join(' ')
})
</script>

<template>
  <tr :class="rowClass">
    <slot />
  </tr>
</template>
