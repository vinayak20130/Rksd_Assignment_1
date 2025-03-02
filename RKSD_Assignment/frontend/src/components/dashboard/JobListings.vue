<script setup lang="ts">
import { ref, computed } from 'vue'
import JobCard from './JobCard.vue'
import { DropDownIcon } from '@/icons'
import type { CompanyIconKey, ColorKey } from '@/types/job'

// Sort options
const sortOptions = ['Latest', 'Oldest', 'Most Applications', 'Fewest Applications']
const activeSort = ref('Latest')
const showSortDropdown = ref(false)

const setSort = (sort: string) => {
  activeSort.value = sort
  showSortDropdown.value = false
}

// Job listings data
const jobs = ref([
  {
    id: 1,
    title: 'Sr. UX Designer',
    postedDays: 3,
    applications: 45,
    steps: ['Bengaluru', '3+ years exp'],
    color: 'blue' as ColorKey,
    daysLeft: 30,
    companyIcon: 'designer' as CompanyIconKey,
  },
  {
    id: 2,
    title: 'Growth Manager',
    postedDays: 5,
    applications: 38,
    steps: ['Remote', '2+ years exp'],
    color: 'red' as ColorKey,
    daysLeft: 45,
    companyIcon: 'growth-manager' as CompanyIconKey,
  },
  {
    id: 3,
    title: 'Financial Analyst',
    postedDays: 10,
    applications: 25,
    steps: ['Verified', '5+ years exp'],
    color: 'yellow' as ColorKey,
    daysLeft: 30,
    companyIcon: 'financial-analyst' as CompanyIconKey,
  },
  {
    id: 4,
    title: 'Security Analyst',
    postedDays: 2,
    applications: 105,
    steps: ['Remote', '3+ years exp'],
    color: 'teal' as ColorKey,
    daysLeft: 15,
    companyIcon: 'security-analyst' as CompanyIconKey,
  },
])

// Sort the jobs based on the active sort option
const sortedJobs = computed(() => {
  const jobsCopy = [...jobs.value]

  switch (activeSort.value) {
    case 'Latest':
      return jobsCopy.sort((a, b) => a.postedDays - b.postedDays)
    case 'Oldest':
      return jobsCopy.sort((a, b) => b.postedDays - a.postedDays)
    case 'Most Applications':
      return jobsCopy.sort((a, b) => b.applications - a.applications)
    case 'Fewest Applications':
      return jobsCopy.sort((a, b) => a.applications - b.applications)
    default:
      return jobsCopy
  }
})
</script>

<template>
  <!-- Job Listings Section with Colored Lines -->
  <div class="px-5 mt-4 mb-6">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-bold text-white">Current Openings</h2>
      <div class="relative">
        <div
          @click="showSortDropdown = !showSortDropdown"
          class="flex items-center gap-1 text-sm font-medium text-[#898989] cursor-pointer py-1 px-2.5 rounded-2xl bg-[#262626]"
        >
          Sort By: {{ activeSort }}
          <DropDownIcon
            class="w-4 h-4 ml-1"
            :class="{ 'transform rotate-180': showSortDropdown }"
          />
        </div>
        <div
          v-if="showSortDropdown"
          v-click-outside="() => (showSortDropdown = false)"
          class="absolute right-0 top-full mt-1 bg-[#262626] rounded-lg shadow-lg z-10 w-48"
        >
          <div
            v-for="option in sortOptions"
            :key="option"
            @click="setSort(option)"
            class="px-4 py-2 text-sm hover:bg-[#333] cursor-pointer"
            :class="{
              'text-white font-medium': option === activeSort,
              'text-[#898989]': option !== activeSort,
            }"
          >
            {{ option }}
          </div>
        </div>
      </div>
    </div>

    <div class="flex gap-5 overflow-x-auto">
      <JobCard
        v-for="job in sortedJobs"
        :key="job.id"
        :title="job.title"
        :postedDays="job.postedDays"
        :applications="job.applications"
        :steps="job.steps"
        :color="job.color"
        :daysLeft="job.daysLeft"
        :companyIcon="job.companyIcon"
      />
    </div>
  </div>
</template>
