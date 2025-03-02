<script setup lang="ts">
import { SearchIcon, SettingsIcon, NotificationIcon, ClearSearchIcon } from '@/icons'
import { searchQuery, clearSearch } from '@/stores/searchStore'
</script>

<template>
  <!-- Top header with search and user controls -->
  <div class="p-10 flex justify-between items-center h-[80px]">
    <!-- Search Bar -->
    <div
      class="bg-[#1E1E1E] rounded-[31px] p-2.5 flex items-center gap-2.5 w-full max-w-[400px] h-[40px] relative"
    >
      <SearchIcon />
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search for candidates by name..."
        class="bg-transparent border-none text-white text-xs w-full outline-none"
      />
      <button
        v-if="searchQuery"
        @click="clearSearch"
        class="absolute right-3 text-[#898989] hover:text-white"
      >
        <ClearSearchIcon />
      </button>
    </div>

    <!-- User Controls -->
    <div class="flex items-center gap-4">
      <div
        class="w-10 h-10 rounded-full bg-[#1E1E1E] flex items-center justify-center cursor-pointer"
      >
        <SettingsIcon class="w-5 h-5 text-[#898989]" />
      </div>
      <div
        class="w-10 h-10 rounded-full bg-[#1E1E1E] flex items-center justify-center cursor-pointer"
      >
        <NotificationIcon class="w-5 h-5 text-[#898989]" />
      </div>
      <div
        class="w-10 h-10 rounded-full bg-[#333] flex items-center justify-center text-xl cursor-pointer"
      >
        👤
      </div>
    </div>
  </div>
</template>
