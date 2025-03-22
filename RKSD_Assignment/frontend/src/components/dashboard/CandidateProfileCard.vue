<template>
  <div class="bg-[#1E1E1E] rounded-xl p-4 flex flex-col items-center">
    <!-- Profile section -->
    <div class="flex flex-col items-center gap-2 mb-8">
      <div class="w-24 h-24 rounded-full bg-[#333] flex items-center justify-center text-3xl overflow-hidden">
        {{ candidate.avatar }}
      </div>
      <div class="text-center">
        <h3 class="text-xl font-bold text-white">
          {{ applicationDetails?.candidate_name || candidate.name }}
        </h3>
        <p class="text-[#898989]">{{ applicationDetails?.role_name || candidate.role }}</p>
      </div>
    </div>

    <!-- Stats section -->
    <div class="w-full px-2">
      <!-- Contact info section -->
      <div class="mt-6 w-full flex gap-3 justify-between">
        <!-- Email row -->
        <div class="flex items-center rounded-xl">
          <div class="w-10 h-10 rounded-full bg-[#262626] flex items-center justify-center mr-3">
            <EmailIcon color="#898989" />
          </div>
          <div>
            <p class="text-[#898989] text-xs font-medium uppercase">EMAIL</p>
            <p class="text-white text-sm font-medium">
              {{ candidate.email || 'malaika.br@gmail.com' }}
            </p>
          </div>
        </div>

        <!-- Phone row -->
        <div class="flex items-center rounded-xl">
          <div class="w-10 h-10 rounded-full bg-[#262626] flex items-center justify-center mr-3">
            <PhoneIcon color="#898989" />
          </div>
          <div>
            <p class="text-[#898989] text-xs font-medium uppercase">PHONE NUMBER</p>
            <p class="text-white text-sm font-medium">
              {{ candidate.phone || '+11 5423-6548' }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { EmailIcon, PhoneIcon } from '@/icons'
import type { ApplicationDetails } from '@/services/api'

// Define candidate type
interface Candidate {
  id: number
  name: string
  avatar: string
  rating: number
  stage: string
  role: string
  date: string
  files: number
  email?: string
  phone?: string
}

defineProps<{
  candidate: Candidate
  applicationDetails: ApplicationDetails | null
}>()
</script>
