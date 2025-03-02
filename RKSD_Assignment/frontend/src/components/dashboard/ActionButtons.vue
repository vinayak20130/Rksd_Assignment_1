<template>
  <div class="flex gap-4">
    <button
      class="flex-1 bg-gradient-to-r from-[#6E38E0] to-[#FF5F36] text-white py-3.5 rounded-xl font-medium flex items-center justify-center gap-2"
      @click="onNextStage"
      :disabled="isUpdating || !applicationId"
    >
      <span v-if="isUpdating && updateAction === 'next'">
        <div
          class="inline-block animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white mr-2"
        ></div>
        Processing...
      </span>
      <span v-else>Move to Next Stage</span>
      <ArrowRightIcon v-if="!isUpdating || updateAction !== 'next'" />
    </button>
    <button
      class="bg-gradient-to-r from-[#38E0AE] to-[#AF36FF] text-white py-3.5 px-4 rounded-xl font-medium w-[67px]"
      @click="onReject"
      :disabled="isUpdating || !applicationId"
    >
      <span v-if="isUpdating && updateAction === 'reject'">
        <div
          class="inline-block animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white"
        ></div>
      </span>
      <span v-else>Reject</span>
    </button>
    <button
      class="bg-gradient-to-r from-[#E03838] to-[#FFA836] text-white py-3.5 px-4 rounded-xl font-medium w-[72px]"
      @click="onOpenPdf"
    >
      PDF
    </button>
  </div>
</template>

<script setup lang="ts">
import { ArrowRightIcon } from '@/icons'

defineProps<{
  applicationId: number | null
  isUpdating: boolean
  updateAction: 'next' | 'reject' | null
}>()

const emit = defineEmits<{
  nextStage: []
  reject: []
  openPdf: []
}>()

const onNextStage = () => {
  emit('nextStage')
}

const onReject = () => {
  emit('reject')
}

const onOpenPdf = () => {
  emit('openPdf')
}
</script>
