<template>
  <svg
    width="1"
    :height="height"
    :viewBox="`0 0 1 ${height}`"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <line
      x1="0.5"
      y1="2.18557e-08"
      x2="0.499987"
      :y2="height"
      stroke="#898989"
      stroke-dasharray="6 6"
    />
  </svg>
</template>

<script setup lang="ts">
// ProgressLineIcon component for application stages timeline
const props = defineProps<{
  height?: number
}>()

// Default height if not provided
const height = props.height || 296
</script>
