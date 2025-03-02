<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  class?: string
}>()

const headClass = computed(() => {
  return [
    'h-12 px-4 text-left align-middle font-medium text-[#898989] [&:has([role=checkbox])]:pr-0',
    props.class,
  ]
    .filter(Boolean)
    .join(' ')
})
</script>

<template>
  <th :class="headClass">
    <slot />
  </th>
</template>
