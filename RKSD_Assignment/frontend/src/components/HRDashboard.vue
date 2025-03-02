<script setup lang="ts">
import Sidebar from './ui/Sidebar.vue'
import TopBar from './dashboard/TopBar.vue'
import JobListings from './dashboard/JobListings.vue'
import CandidatesTable from './dashboard/CandidatesTable.vue'
</script>

<template>
  <div class="flex w-full h-screen bg-[#151515] text-white font-['Urbanist'] overflow-hidden">
    <!-- Sidebar Component -->
    <Sidebar activePage="Candidates" />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-auto">
      <!-- Top Bar Component -->
      <TopBar />

      <!-- Horizontal line below top bar -->
      <hr class="w-full border-t border-[#272727] border-solid m-0 p-0" />

      <!-- Job Listings Component -->
      <JobListings />

      <!-- Candidates Table Component -->
      <CandidatesTable />
    </div>
  </div>
</template>
