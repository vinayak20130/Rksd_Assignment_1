<template>
  <div class="fixed inset-0 z-50 flex justify-end" v-if="isOpen && candidate">
    <!-- Blurred overlay -->
    <div class="absolute inset-0 bg-black/10 backdrop-blur-sm" @click="close"></div>

    <!-- Sidebar -->
    <div
      class="relative w-[500px] h-full bg-[#151515] border-l border-[#272727] shadow-xl overflow-y-auto"
    >
      <!-- Notification -->
      <NotificationComponent
        v-if="notification.show"
        :show="notification.show"
        :type="notification.type"
        :message="notification.message"
        @close="closeNotification"
      />

      <!-- Header with close button -->
      <div
        class="sticky top-0 bg-[#151515] p-6 border-b border-[#272727] flex justify-between items-center"
      >
        <h2 class="text-2xl font-bold text-white">Candidate Details</h2>
        <button
          @click="close"
          class="text-[#898989] hover:text-white p-1 rounded-full hover:bg-[#262626]"
        >
          <CloseIcon />
        </button>
      </div>

      <!-- Loading state -->
      <div v-if="isLoading" class="p-6 flex flex-col items-center justify-center">
        <div
          class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-[#6E38E0]"
        ></div>
        <p class="mt-2 text-[#898989]">Loading candidate details...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="p-6 text-center">
        <p class="text-red-500">{{ error }}</p>
        <button
          @click="() => candidate && fetchApplicationDetails(candidate.id)"
          class="mt-4 px-4 py-2 bg-[#262626] text-white rounded-lg hover:bg-[#333]"
        >
          Try Again
        </button>
      </div>

      <!-- Content container with padding -->
      <div v-else-if="candidate" class="p-6 space-y-6">
        <!-- Candidate Profile Card -->
        <CandidateProfileCard :candidate="candidate" :application-details="applicationDetails" />

        <!-- Application Details Card -->
        <div class="bg-[#1E1E1E] rounded-xl p-4">
          <h4 class="text-xl font-semibold text-white mb-6">Application Details</h4>

          <!-- Application details content -->
          <div class="space-y-6">
            <!-- Application Stages Timeline -->
            <ApplicationStagesTimeline :application-details="applicationDetails" />
          </div>
        </div>

        <!-- Experience Card -->
        <ExperienceCard v-if="applicationDetails" :experiences="applicationDetails.experiences" />
      </div>

      <!-- Fixed action buttons at bottom -->
      <div
        class="fixed bottom-0 w-[500px] bg-[#151515] p-6 border-t border-[#272727] shadow-[0_-16px_48px_rgba(21,21,21,1)]"
      >
        <ActionButtons
          :application-id="applicationDetails?.application_id || null"
          :is-updating="isUpdating"
          :update-action="updateAction"
          @next-stage="handleNextStage"
          @reject="handleReject"
          @open-pdf="openPdf"
        />
      </div>

      <!-- Extra padding at bottom to account for fixed buttons -->
      <div class="h-24"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from 'vue'
import { CloseIcon } from '@/icons'
import {
  getApplicationDetails,
  updateApplicationStage,
  type ApplicationDetails,
  type StageInfo,
} from '@/services/api'

// Import sub-components
import NotificationComponent from './NotificationComponent.vue'
import CandidateProfileCard from './CandidateProfileCard.vue'
import ApplicationStagesTimeline from './ApplicationStagesTimeline.vue'
import ExperienceCard from './ExperienceCard.vue'
import ActionButtons from './ActionButtons.vue'

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

const props = defineProps<{
  isOpen: boolean
  candidate: Candidate | null
}>()

const emit = defineEmits<{
  close: []
  stageUpdated: [applicationId: number, newStatus: string, newStage: StageInfo | null]
}>()

const close = () => {
  emit('close')
}

// State for application details
const applicationDetails = ref<ApplicationDetails | null>(null)
const isLoading = ref(false)
const error = ref<string | null>(null)
const isUpdating = ref(false)
const updateAction = ref<'next' | 'reject' | null>(null)
const updateError = ref<string | null>(null)
const notification = ref({
  show: false,
  type: 'success' as 'success' | 'error',
  message: '',
  timeout: null as number | null,
})

// Fetch application details when candidate changes
watch(
  () => props.candidate,
  async (newCandidate) => {
    if (newCandidate && props.isOpen) {
      await fetchApplicationDetails(newCandidate.id)
    }
  },
  { immediate: true },
)

// Also watch isOpen to fetch data when sidebar opens
watch(
  () => props.isOpen,
  async (isOpen) => {
    if (isOpen && props.candidate) {
      await fetchApplicationDetails(props.candidate.id)
    }
  },
)

// Function to fetch application details
const fetchApplicationDetails = async (applicationId: number) => {
  if (!applicationId) return

  isLoading.value = true
  error.value = null

  try {
    applicationDetails.value = await getApplicationDetails(applicationId)
  } catch (err) {
    console.error('Error fetching application details:', err)
    error.value = 'Failed to load application details. Please try again.'
  } finally {
    isLoading.value = false
  }
}

// Function to show notification
const showNotification = (type: 'success' | 'error', message: string) => {
  // Clear any existing timeout
  if (notification.value.timeout) {
    clearTimeout(notification.value.timeout)
  }

  // Set notification
  notification.value = {
    show: true,
    type,
    message,
    timeout: setTimeout(() => {
      notification.value.show = false
    }, 5000) as unknown as number, // Auto-hide after 5 seconds
  }
}

// Function to close notification
const closeNotification = () => {
  if (notification.value.timeout) {
    clearTimeout(notification.value.timeout)
  }
  notification.value.show = false
}

// Function to handle moving to the next stage
const handleNextStage = async () => {
  if (!applicationDetails.value || isUpdating.value) return

  isUpdating.value = true
  updateAction.value = 'next'
  updateError.value = null

  try {
    const result = await updateApplicationStage(applicationDetails.value.application_id, 'next')
    // Refresh application details after successful update
    await fetchApplicationDetails(applicationDetails.value.application_id)

    // Emit event to update the table
    if (applicationDetails.value) {
      const newStage = applicationDetails.value.current_stage_sequence
        ? {
            current_stage: applicationDetails.value.current_stage_id,
            stage_name: applicationDetails.value.current_stage_name,
            stage_sequence: applicationDetails.value.current_stage_sequence,
          }
        : null

      emit(
        'stageUpdated',
        applicationDetails.value.application_id,
        applicationDetails.value.status,
        newStage,
      )
    }

    // Show success message
    showNotification('success', 'Application moved to the next stage successfully')
  } catch (err) {
    console.error('Error moving to next stage:', err)
    updateError.value = 'Failed to move to next stage. Please try again.'
    showNotification('error', 'Failed to move to next stage. Please try again.')
  } finally {
    isUpdating.value = false
    updateAction.value = null
  }
}

// Function to handle rejecting the application
const handleReject = async () => {
  if (!applicationDetails.value || isUpdating.value) return

  isUpdating.value = true
  updateAction.value = 'reject'
  updateError.value = null

  try {
    await updateApplicationStage(applicationDetails.value.application_id, 'reject')
    // Refresh application details after successful update
    await fetchApplicationDetails(applicationDetails.value.application_id)

    // Emit event to update the table
    if (applicationDetails.value) {
      const newStage = applicationDetails.value.current_stage_sequence
        ? {
            current_stage: applicationDetails.value.current_stage_id,
            stage_name: applicationDetails.value.current_stage_name,
            stage_sequence: applicationDetails.value.current_stage_sequence,
          }
        : null

      emit(
        'stageUpdated',
        applicationDetails.value.application_id,
        applicationDetails.value.status,
        newStage,
      )
    }

    // Show success message
    showNotification('success', 'Application has been rejected')
  } catch (err) {
    console.error('Error rejecting application:', err)
    updateError.value = 'Failed to reject application. Please try again.'
    showNotification('error', 'Failed to reject application. Please try again.')
  } finally {
    isUpdating.value = false
    updateAction.value = null
  }
}

// Function to open PDF in a new tab
const openPdf = () => {
  if (!applicationDetails.value) return

  const pdfUrl = `http://localhost:8000/applications/${applicationDetails.value.application_id}/pdf`
  window.open(pdfUrl, '_blank')
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
