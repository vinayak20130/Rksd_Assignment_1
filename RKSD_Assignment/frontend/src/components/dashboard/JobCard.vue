<script setup lang="ts">
import { LocationIcon, ExperienceIcon, ArrowIcon } from '@/icons'
import {
  designerIcon,
  growthManagerIcon,
  financialAnalystIcon,
  securityAnalystIcon,
} from '@/icons/images'
import type { CompanyIconKey, ColorKey } from '@/types/job'

// Map of company icons
const companyIconMap: Record<CompanyIconKey, string> = {
  designer: designerIcon,
  'growth-manager': growthManagerIcon,
  'financial-analyst': financialAnalystIcon,
  'security-analyst': securityAnalystIcon,
}

defineProps<{
  title: string
  postedDays: number
  applications: number
  steps: string[]
  color: ColorKey
  daysLeft: number
  weeklyApplications?: number
  companyIcon?: CompanyIconKey
}>()

// Map of color names to their gradient values
const colorMap: Record<ColorKey, string> = {
  teal: 'from-[#00B7C2] to-[#4ECDC4]',
  red: 'from-[#FF5F36] to-[#FF8F6B]',
  yellow: 'from-[#FFB302] to-[#FFD25F]',
  blue: 'from-[#29C5EE] to-[#29C5EE]',
}

// Map step text to appropriate icon
const getStepIcon = (step: string) => {
  if (step.includes('years') || step.includes('exp')) {
    return ExperienceIcon
  }
  return LocationIcon
}

// Get company icon based on the companyIcon prop
const getCompanyIcon = (iconKey: CompanyIconKey) => {
  return companyIconMap[iconKey] || designerIcon // Default to designer icon if not found
}
</script>

<template>
  <div class="relative bg-[#1E1E1E] rounded-2xl p-5 w-96 overflow-hidden">
    <!-- Colored vertical line -->
    <div
      class="absolute left-0 top-0 w-2 h-full rounded-l-2xl bg-gradient-to-b"
      :class="colorMap[color]"
    ></div>

    <!-- Arrow icon in the top right -->
    <div
      class="absolute top-3 right-3 w-10 h-10 rounded-full bg-[#262626] flex items-center justify-center cursor-pointer"
    >
      <ArrowIcon class="w-5 h-5 text-[#898989]" />
    </div>

    <!-- Content with left padding to account for the line -->
    <div class="relative pl-3">
      <!-- Job title and days posted -->
      <div class="flex justify-between items-start mb-5">
        <div class="flex items-center gap-3">
          <div>
            <img
              :src="companyIcon ? getCompanyIcon(companyIcon) : getCompanyIcon('designer')"
              :alt="`${title} company logo`"
              class="w-11 h-11 object-contain"
            />
          </div>
          <div>
            <h3 class="text-white text-sm font-medium">{{ title }}</h3>
            <p class="text-[#898989] text-xs">Posted {{ postedDays }} days ago</p>
          </div>
        </div>
      </div>

      <!-- Job steps -->
      <div class="flex gap-2 mb-5 flex-wrap">
        <div
          v-for="(step, index) in steps"
          :key="index"
          class="bg-[#282828] rounded-full px-2 py-1.5 flex items-center gap-1.5"
        >
          <component :is="getStepIcon(step)" />
          <span class="text-[#898989] text-xs font-medium">{{ step }}</span>
        </div>
      </div>

      <!-- Application count and days left -->
      <div class="flex justify-between items-center">
        <div class="flex flex-row items-baseline gap-2">
          <div class="text-white text-4xl font-bold">{{ applications }}</div>
          <div class="text-[#898989] text-xs">applications</div>
        </div>
        <div v-if="weeklyApplications" class="text-[#00B85E] text-xs">
          {{ weeklyApplications }} in last week
        </div>
        <div v-else class="text-[#898989] text-xs">{{ daysLeft }} days left</div>
      </div>
    </div>
  </div>
</template>
