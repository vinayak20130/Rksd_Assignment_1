<template>
  <div class="bg-[#1E1E1E] rounded-xl p-4" v-if="experiences && experiences.length > 0">
    <h4 class="text-xl font-semibold text-white mb-6">Experience</h4>

    <!-- Experience content -->
    <div class="space-y-4">
      <div v-for="exp in experiences" :key="exp.experience_id" class="bg-[#262626] p-3 rounded-lg">
        <div class="flex justify-between items-center mb-2">
          <p class="text-white font-medium">{{ exp.position }}</p>
          <p class="text-[#898989] text-sm">
            {{ new Date(exp.start_date).getFullYear() }} -
            {{ exp.end_date ? new Date(exp.end_date).getFullYear() : 'Present' }}
          </p>
        </div>
        <p class="text-[#898989] text-sm">{{ exp.company_name }}</p>
        <p v-if="exp.description" class="text-[#898989] text-sm mt-2">
          {{ exp.description }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Define experience type
interface Experience {
  experience_id: number
  position: string
  company_name: string
  start_date: string
  end_date?: string
  description?: string
}

defineProps<{
  experiences: Experience[] | null
}>()
</script>
