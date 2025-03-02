<template>
  <div
    v-if="show"
    class="fixed top-20 right-6 p-4 rounded-lg shadow-lg z-50 flex items-center gap-3 animate-fade-in"
    :class="{
      'bg-[#38E0AE]/10 text-[#38E0AE] border border-[#38E0AE]/20': type === 'success',
      'bg-[#E03838]/10 text-[#E03838] border border-[#E03838]/20': type === 'error',
    }"
  >
    <div v-if="type === 'success'" class="w-5 h-5 flex-shrink-0">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M12 22C17.5 22 22 17.5 22 12C22 6.5 17.5 2 12 2C6.5 2 2 6.5 2 12C2 17.5 6.5 22 12 22Z"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
        <path
          d="M7.75 12L10.58 14.83L16.25 9.17"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </div>
    <div v-else class="w-5 h-5 flex-shrink-0">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M12 22C17.5 22 22 17.5 22 12C22 6.5 17.5 2 12 2C6.5 2 2 6.5 2 12C2 17.5 6.5 22 12 22Z"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
        <path
          d="M12 8V13"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
        <path
          d="M11.995 16H12.005"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </div>
    <p class="font-medium">{{ message }}</p>
    <button @click="onClose" class="ml-2 text-current hover:opacity-70 p-1">
      <svg
        width="14"
        height="14"
        viewBox="0 0 14 14"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M13 1L1 13"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
        <path
          d="M1 1L13 13"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  show: boolean
  type: 'success' | 'error'
  message: string
}>()

const emit = defineEmits<{
  close: []
}>()

const onClose = () => {
  emit('close')
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
