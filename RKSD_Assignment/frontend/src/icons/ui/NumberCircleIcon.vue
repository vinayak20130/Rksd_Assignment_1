<template>
  <div class="bg-[#262626] rounded-full h-10 w-10 flex items-center justify-center">
    <span class="text-[#898989] text-base font-semibold">{{ number }}</span>
  </div>
</template>

<script setup lang="ts">
defineProps({
  number: {
    type: [Number, String],
    required: true,
  },
})
</script>
