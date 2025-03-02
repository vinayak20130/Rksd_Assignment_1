<template>
  <div class="mt-8">
    <p class="text-sm text-[#898989] mb-4">APPLICATION STAGES</p>
    <div class="relative mb-8" v-if="applicationDetails">
      <!-- Vertical dashed line -->
      <div
        class="absolute left-[19.5px] top-3 bottom-3 w-[1px]"
        style="
          background: repeating-linear-gradient(
            to bottom,
            #898989 0,
            #898989 6px,
            transparent 6px,
            transparent 12px
          );
        "
      ></div>

      <!-- Dynamic stages based on API data -->
      <div
        v-for="(stage, index) in applicationDetails.role_stages"
        :key="stage.stage_id"
        class="flex items-center mb-6 relative z-1"
        :class="{ 'mb-0': index === applicationDetails.role_stages.length - 1 }"
      >
        <div class="z-1">
          <!-- Completed stage (check icon) -->
          <CheckIcon
            v-if="
              (applicationDetails.status !== 'rejected' &&
                getStageStatus(stage.stage_sequence, applicationDetails.current_stage_sequence) ===
                  'completed') ||
              applicationDetails.status === 'accepted'
            "
          />

          <!-- Rejected stage (cross icon) -->
          <CrossIcon v-else-if="applicationDetails.status === 'rejected'" />

          <!-- Current stage (review icon) -->
          <ReviewIcon
            v-else-if="
              getStageStatus(stage.stage_sequence, applicationDetails.current_stage_sequence) ===
              'current'
            "
          />

          <!-- Upcoming stage (number icon) -->
          <NumberCircleIcon v-else :number="stage.stage_sequence.toString()" />
        </div>

        <div
          class="ml-3 flex justify-between w-full pr-4"
          :class="{
            'flex-col':
              getStageStatus(stage.stage_sequence, applicationDetails.current_stage_sequence) !==
              'current',
          }"
        >
          <div>
            <h5
              class="text-base font-medium"
              :class="{
                'text-white':
                  getStageStatus(
                    stage.stage_sequence,
                    applicationDetails.current_stage_sequence,
                  ) !== 'upcoming',
                'text-[#898989]':
                  getStageStatus(
                    stage.stage_sequence,
                    applicationDetails.current_stage_sequence,
                  ) === 'upcoming',
              }"
            >
              {{ stage.stage_name }}
            </h5>
            <p
              v-if="
                getStageStatus(stage.stage_sequence, applicationDetails.current_stage_sequence) !==
                'upcoming'
              "
              class="text-[#898989] text-xs"
            >
              {{ formatDate(applicationDetails.application_date) }}
            </p>
          </div>

          <!-- Status badge for current stage -->
          <div
            v-if="
              getStageStatus(stage.stage_sequence, applicationDetails.current_stage_sequence) ===
              'current'
            "
            class="px-3 py-1 rounded-full text-xs font-medium h-6 flex items-center"
            :class="{
              'bg-[#EAB04D]/10 text-[#EAB04D]': applicationDetails.status === 'pending',
              'bg-[#38E0AE]/10 text-[#38E0AE]': applicationDetails.status === 'accepted',
              'bg-[#E03838]/10 text-[#E03838]': applicationDetails.status === 'rejected',
            }"
          >
            {{
              applicationDetails.status === 'pending'
                ? 'Under Review'
                : applicationDetails.status.charAt(0).toUpperCase() +
                  applicationDetails.status.slice(1)
            }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { CheckIcon, ReviewIcon, NumberCircleIcon, CrossIcon } from '@/icons'
import type { ApplicationDetails } from '@/services/api'

defineProps<{
  applicationDetails: ApplicationDetails | null
}>()

// Format date function
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

// Function to determine stage status
const getStageStatus = (stageSequence: number, currentStageSequence: number) => {
  if (stageSequence < currentStageSequence) {
    return 'completed' // Previous stages are completed
  } else if (stageSequence === currentStageSequence) {
    return 'current' // Current stage is in progress
  } else {
    return 'upcoming' // Future stages are upcoming
  }
}
</script>
