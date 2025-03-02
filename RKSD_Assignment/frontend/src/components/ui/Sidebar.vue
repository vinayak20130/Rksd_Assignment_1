<script setup lang="ts">
import { ProfileUsersIcon, RskdLogo } from '@/icons'

defineProps<{
  activePage?: string
}>()
</script>

<template>
  <div class="w-[250px] bg-[#151515] h-screen flex flex-col border-r border-[#262626]">
    <!-- Logo -->
    <div class="p-5 h-[80px] flex items-center">
      <RskdLogo />
    </div>

    <!-- Horizontal Line -->
    <hr class="w-full border-t border-[#272727] border-solid m-0 p-0" />

    <div class="mt-5">
      <h2 class="text-xs font-medium uppercase tracking-wider text-[#898989] mb-4 px-5">
        RECRUITMENT
      </h2>

      <div
        class="flex items-center py-2 pr-4 pl-5 mr-3 rounded-r-full rounded-l-none cursor-pointer mb-2 bg-gradient-to-r from-[#6E38E0] to-[#FF5F36]"
      >
        <div class="flex items-center gap-3">
          <ProfileUsersIcon class="w-5 h-5" />
          <span class="text-base font-thin text-white">Candidates</span>
        </div>
      </div>
    </div>
  </div>
</template>
