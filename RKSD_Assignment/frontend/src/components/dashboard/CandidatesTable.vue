<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { StarIcon, AttachmentIcon, SortIcon, DropDownIcon } from '@/icons'
import CandidateDetails from './CandidateDetails.vue'
import { Table, TableHeader, TableBody, TableHead, TableRow, TableCell } from '../ui/table'
import { searchQuery } from '@/stores/searchStore'
import { getDetailedApplicationsByMonth, type Candidate as ApiCandidate } from '@/services/api'

// Define candidate type for the UI
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
  status: string
}

// Loading state
const isLoading = ref(true)
const error = ref<string | null>(null)

// Candidate data
const candidates = ref<Candidate[]>([])

// Function to fetch candidates from the API
const fetchCandidates = async () => {
  isLoading.value = true
  error.value = null

  try {
    // Get current date for default month/year
    const currentDate = new Date()
    const currentYear = currentDate.getFullYear()
    const currentMonth = currentDate.getMonth() + 1 // JavaScript months are 0-indexed

    // Prepare parameters based on selected month
    let yearParam: number | undefined = undefined
    let monthParam: number | undefined = undefined

    if (activeMonth.value !== 'All Months') {
      const selectedMonthNumber = getMonthNumber(activeMonth.value)
      const selectedYear = parseInt(activeMonth.value.split(' ')[1])

      yearParam = selectedYear
      monthParam = selectedMonthNumber
    }

    // Map filter to status
    let status: string | undefined = undefined
    if (activeFilter.value === 'Accepted') {
      status = 'ACCEPTED'
    } else if (activeFilter.value === 'Rejected') {
      status = 'REJECTED'
    }

    // Get candidates from API
    const apiCandidates = await getDetailedApplicationsByMonth(yearParam, monthParam, status)

    // Map API candidates to UI candidates
    candidates.value = apiCandidates.map((candidate: ApiCandidate) => {
      // Format date from ISO string to DD/MM/YY
      const appDate = new Date(candidate.application_date)
      const formattedDate = `${appDate.getDate().toString().padStart(2, '0')}/${(appDate.getMonth() + 1).toString().padStart(2, '0')}/${appDate.getFullYear().toString().slice(2)}`

      // Generate avatar from first letter of name
      const avatarEmoji = getAvatarEmoji(candidate.candidate_name)

      return {
        id: candidate.application_id,
        name: candidate.candidate_name,
        avatar: avatarEmoji,
        rating: candidate.rating,
        stage: candidate.stage?.stage_name || 'Not Started',
        role: candidate.role_name,
        date: formattedDate,
        files: candidate.attachments || 0,
        // You can add mock email and phone for now
        email: `${candidate.candidate_name.toLowerCase().replace(/\s+/g, '.')}@example.com`,
        phone: '+1 555-123-4567',
        status: candidate.status || 'pending', // Get status from API or default to pending
      }
    })

    // Extract available months from the API response
    if (activeMonth.value === 'All Months' || !months.value.length) {
      extractAvailableMonths()
    }
  } catch (err) {
    console.error('Error fetching candidates:', err)
    error.value = 'Failed to load candidates. Please try again later.'
    candidates.value = [] // Clear candidates on error
  } finally {
    isLoading.value = false
  }
}

// Helper function to generate avatar emoji based on name
const getAvatarEmoji = (name: string): string => {
  const emojiOptions = ['👨‍💼', '👩‍💼', '👨‍💻', '👩‍💻', '👨‍🎨', '👩‍🎨']
  // Use the first character of the name to deterministically select an emoji
  const charCode = name.charCodeAt(0)
  return emojiOptions[charCode % emojiOptions.length]
}

// Fetch candidates on component mount
onMounted(() => {
  fetchCandidates()
})

// Selected candidate for details sidebar
const selectedCandidate = ref<Candidate | null>(null)
const isSidebarOpen = ref(false)

const openCandidateDetails = (candidate: Candidate) => {
  selectedCandidate.value = candidate
  isSidebarOpen.value = true
}

const closeSidebar = () => {
  isSidebarOpen.value = false
}

// Filter state
const activeFilter = ref('All')
const filters = ['All', 'Accepted', 'Rejected']

const setFilter = (filter: string) => {
  activeFilter.value = filter
  fetchCandidates() // Refetch candidates when filter changes
}

// Month filter state
const months = ref<string[]>(['All Months'])
const activeMonth = ref('All Months')
const showMonthDropdown = ref(false)

// Function to extract available months from candidate data
const extractAvailableMonths = () => {
  if (candidates.value.length === 0) return

  const uniqueMonths = new Set<string>()

  candidates.value.forEach((candidate) => {
    // Parse date in format DD/MM/YY
    const [day, month, year] = candidate.date.split('/').map(Number)
    // Convert YY to YYYY
    const fullYear = 2000 + year

    const monthNames = [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December',
    ]

    const formattedMonth = `${monthNames[month - 1]} ${fullYear}`
    uniqueMonths.add(formattedMonth)
  })

  // Convert Set to Array and sort (newest first)
  const sortedMonths = Array.from(uniqueMonths).sort((a, b) => {
    const [monthA, yearA] = a.split(' ')
    const [monthB, yearB] = b.split(' ')

    if (yearA !== yearB) return parseInt(yearB) - parseInt(yearA)

    const monthNames = [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December',
    ]

    return monthNames.indexOf(monthB) - monthNames.indexOf(monthA)
  })

  months.value = ['All Months', ...sortedMonths]

  // Set default active month if not already set
  if (sortedMonths.length > 0 && activeMonth.value === 'All Months') {
    activeMonth.value = sortedMonths[0]
    // Don't call fetchCandidates here to avoid infinite loop
  }
}

const setMonth = (month: string) => {
  activeMonth.value = month
  showMonthDropdown.value = false
  fetchCandidates() // Refetch candidates when month changes
}

// Helper function to get month number from month name
const getMonthNumber = (monthName: string): number => {
  // Handle "All Months" case
  if (monthName === 'All Months') {
    return 0 // Return 0 or any default value that won't match any month
  }

  const monthMap: Record<string, number> = {
    January: 1,
    February: 2,
    March: 3,
    April: 4,
    May: 5,
    June: 6,
    July: 7,
    August: 8,
    September: 9,
    October: 10,
    November: 11,
    December: 12,
  }

  // Extract month name from format "Month YYYY"
  const monthOnly = monthName.split(' ')[0]
  return monthMap[monthOnly] || 0
}

// Filter candidates by month, rating, and search query
const filteredCandidates = computed(() => {
  // First filter by search query
  let filtered = candidates.value

  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    filtered = filtered.filter((candidate) => candidate.name.toLowerCase().includes(query))
  }

  // Then filter by month and year if needed
  // Note: We're already filtering by month/year in the API call,
  // but we still need this for when "All Months" is selected and we get all data
  if (activeMonth.value !== 'All Months') {
    const selectedMonthNumber = getMonthNumber(activeMonth.value)
    const selectedYear = parseInt(activeMonth.value.split(' ')[1])

    filtered = filtered.filter((candidate) => {
      // Parse date in format DD/MM/YY
      const [day, month, year] = candidate.date.split('/').map(Number)
      // Convert YY to YYYY for comparison
      const fullYear = 2000 + year

      return month === selectedMonthNumber && fullYear === selectedYear
    })
  }

  // Then filter by rating
  if (activeFilter.value === 'All') {
    return filtered
  } else if (activeFilter.value === 'Accepted') {
    // Use status instead of rating for filtering
    return filtered.filter((c) => c.status === 'accepted' || c.status === 'pending')
  } else {
    // Use status instead of rating for filtering
    return filtered.filter((c) => c.status === 'rejected')
  }
})

// Sorting state
const sortColumn = ref('')
const sortDirection = ref<'asc' | 'desc' | ''>('')

// Toggle sorting
const toggleSort = (column: string) => {
  if (column === 'name' || column === 'files') return // These columns are not sortable

  if (sortColumn.value === column) {
    // Cycle through: asc -> desc -> none
    if (sortDirection.value === 'asc') {
      sortDirection.value = 'desc'
    } else if (sortDirection.value === 'desc') {
      sortDirection.value = ''
      sortColumn.value = ''
    }
  } else {
    sortColumn.value = column
    sortDirection.value = 'asc'
  }
}

// Sort the candidates
const sortedCandidates = computed(() => {
  if (!sortColumn.value || !sortDirection.value) {
    return filteredCandidates.value
  }

  return [...filteredCandidates.value].sort((a, b) => {
    const aValue = a[sortColumn.value as keyof typeof a]
    const bValue = b[sortColumn.value as keyof typeof b]

    // Handle different data types
    if (typeof aValue === 'number' && typeof bValue === 'number') {
      return sortDirection.value === 'asc' ? aValue - bValue : bValue - aValue
    }

    // Handle date strings (convert to Date objects for comparison)
    if (sortColumn.value === 'date') {
      const [aDay, aMonth, aYear] = (aValue as string).split('/').map(Number)
      const [bDay, bMonth, bYear] = (bValue as string).split('/').map(Number)

      const aDate = new Date(2000 + aYear, aMonth - 1, aDay)
      const bDate = new Date(2000 + bYear, bMonth - 1, bDay)

      return sortDirection.value === 'asc'
        ? aDate.getTime() - bDate.getTime()
        : bDate.getTime() - aDate.getTime()
    }

    // Default string comparison
    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return sortDirection.value === 'asc'
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue)
    }

    return 0
  })
})

// Column definitions
const columns = [
  { id: 'name', header: 'CANDIDATE NAME', sortable: false },
  { id: 'rating', header: 'RATING', sortable: true },
  { id: 'stage', header: 'STAGES', sortable: true },
  { id: 'role', header: 'APPLIED ROLE', sortable: false },
  { id: 'date', header: 'APPLICATION DATE', sortable: true },
  { id: 'files', header: 'ATTACHMENTS', sortable: false },
]

// Computed property for empty state
const noResults = computed(() => sortedCandidates.value.length === 0)

// Computed properties for filter counts
const acceptedCount = computed(() => {
  // Filter by search query first
  let filtered = candidates.value

  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    filtered = filtered.filter((candidate) => candidate.name.toLowerCase().includes(query))
  }

  // Filter by month and year if needed
  if (activeMonth.value !== 'All Months') {
    const selectedMonthNumber = getMonthNumber(activeMonth.value)
    const selectedYear = parseInt(activeMonth.value.split(' ')[1])

    filtered = filtered.filter((candidate) => {
      const [day, month, year] = candidate.date.split('/').map(Number)
      const fullYear = 2000 + year
      return month === selectedMonthNumber && fullYear === selectedYear
    })
  }

  // Then count accepted candidates based on status
  return filtered.filter((c) => c.status === 'accepted' || c.status === 'pending').length
})

const rejectedCount = computed(() => {
  // Filter by search query first
  let filtered = candidates.value

  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    filtered = filtered.filter((candidate) => candidate.name.toLowerCase().includes(query))
  }

  // Filter by month and year if needed
  if (activeMonth.value !== 'All Months') {
    const selectedMonthNumber = getMonthNumber(activeMonth.value)
    const selectedYear = parseInt(activeMonth.value.split(' ')[1])

    filtered = filtered.filter((candidate) => {
      const [day, month, year] = candidate.date.split('/').map(Number)
      const fullYear = 2000 + year
      return month === selectedMonthNumber && fullYear === selectedYear
    })
  }

  // Then count rejected candidates based on status
  return filtered.filter((c) => c.status === 'rejected').length
})

const allCount = computed(() => {
  // Filter by search query first
  let filtered = candidates.value

  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    filtered = filtered.filter((candidate) => candidate.name.toLowerCase().includes(query))
  }

  // Filter by month and year if needed
  if (activeMonth.value !== 'All Months') {
    const selectedMonthNumber = getMonthNumber(activeMonth.value)
    const selectedYear = parseInt(activeMonth.value.split(' ')[1])

    filtered = filtered.filter((candidate) => {
      const [day, month, year] = candidate.date.split('/').map(Number)
      const fullYear = 2000 + year
      return month === selectedMonthNumber && fullYear === selectedYear
    })
  }

  return filtered.length
})

// Function to generate class string for table headers
const getHeaderClass = (column: { id: string; sortable: boolean }) => {
  let classes = 'text-sm font-medium tracking-wider text-[#898989]'

  if (column.sortable) {
    classes += ' cursor-pointer select-none'
  }

  if (column.id === 'name') {
    classes += ' rounded-tl-lg rounded-bl-lg'
  }

  if (column.id === 'files') {
    classes += ' rounded-tr-lg rounded-br-lg'
  }

  return classes
}

// Function to handle stage updates from the CandidateDetails component
const handleStageUpdated = (applicationId: number, newStatus: string, newStage: any) => {
  // Find the candidate in the list and update its stage
  const candidateIndex = candidates.value.findIndex((c) => c.id === applicationId)
  if (candidateIndex !== -1) {
    // Update the candidate's stage
    candidates.value[candidateIndex].stage = newStage?.stage_name || 'Not Started'

    // Update the candidate's status based on the new status from the API
    candidates.value[candidateIndex].status = newStatus

    // If the status is 'rejected', update the rating to reflect that
    if (newStatus.toLowerCase() === 'rejected') {
      candidates.value[candidateIndex].rating = 1 // Set a low rating for rejected candidates
    } else if (newStatus.toLowerCase() === 'accepted') {
      candidates.value[candidateIndex].rating = 5 // Set a high rating for accepted candidates
    }
  }
}
</script>

<template>
  <!-- Candidates Section -->
  <div class="px-5 pb-5">
    <div class="flex justify-between items-center mb-4">
      <div class="flex items-center gap-3">
        <h2 class="text-xl font-bold text-white">Candidates</h2>
        <div class="bg-[#262626] text-[#898989] text-xs px-2 py-1 rounded-full">
          {{ sortedCandidates.length }} results
        </div>
      </div>
      <div class="relative">
        <div
          @click="showMonthDropdown = !showMonthDropdown"
          class="flex items-center gap-1 text-sm font-medium text-[#898989] cursor-pointer py-1 px-2.5 bg-[#262626] rounded-2xl"
          :class="{
            'border border-[#151515]': activeMonth !== 'All Months',
          }"
        >
          {{ activeMonth }}
          <DropDownIcon
            class="w-4 h-4 ml-1"
            :class="{ 'transform rotate-180': showMonthDropdown }"
          />
        </div>
        <div
          v-if="showMonthDropdown"
          v-click-outside="() => (showMonthDropdown = false)"
          class="absolute right-0 top-full mt-1 bg-[#262626] rounded-lg shadow-lg z-10 w-40"
        >
          <div
            v-for="month in months"
            :key="month"
            @click="setMonth(month)"
            class="px-4 py-2 text-sm hover:bg-[#333] cursor-pointer flex items-center"
            :class="{
              'text-white font-medium': month === activeMonth,
              'text-[#898989]': month !== activeMonth,
            }"
          >
            {{ month }}
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-[#1E1E1E] rounded-t-2xl px-5 pt-5 pb-2">
      <div class="flex gap-10 relative">
        <div
          v-for="filter in filters"
          :key="filter"
          class="text-sm font-medium text-[#898989] cursor-pointer py-1 px-2.5 relative"
          :class="{ 'font-bold text-white': activeFilter === filter }"
          @click="setFilter(filter)"
        >
          <div class="flex items-center gap-2">
            {{ filter }}
            <span class="text-xs bg-[#262626] px-1.5 py-0.5 rounded-full">
              {{
                filter === 'All' ? allCount : filter === 'Accepted' ? acceptedCount : rejectedCount
              }}
            </span>
          </div>
          <div
            v-if="activeFilter === filter"
            class="absolute bottom-[-10px] left-0 w-full h-0.5 bg-gradient-to-r from-[#6E38E0] to-[#FF5F36] rounded-[23px]"
          ></div>
        </div>
      </div>
    </div>
    <div class="flex w-full">
      <hr class="w-[95%] border-t border-[#272727] border-solid" />
      <hr class="w-[5%] border-t border-[#1E1E1E] border-solid" />
    </div>
    <!-- Candidates Table -->
    <div class="bg-[#1E1E1E] rounded-b-2xl overflow-hidden px-5">
      <div class="mt-4">
        <!-- Loading state -->
        <div v-if="isLoading" class="py-10 text-center">
          <div
            class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-[#6E38E0]"
          ></div>
          <p class="mt-2 text-[#898989]">Loading candidates...</p>
        </div>

        <!-- Error state -->
        <div v-else-if="error" class="py-10 text-center">
          <p class="text-red-500">{{ error }}</p>
          <button
            @click="fetchCandidates"
            class="mt-4 px-4 py-2 bg-[#262626] text-white rounded-lg hover:bg-[#333]"
          >
            Try Again
          </button>
        </div>

        <!-- Data table -->
        <Table v-else>
          <TableHeader class="bg-[#262626]">
            <TableRow class="border-none">
              <TableHead
                v-for="column in columns"
                :key="column.id"
                :class="getHeaderClass(column)"
                @click="column.sortable && toggleSort(column.id)"
              >
                <div class="flex items-center">
                  {{ column.header }}
                  <SortIcon v-if="column.sortable" class="ml-2" />
                </div>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow
              v-for="candidate in sortedCandidates"
              :key="candidate.id"
              class="border-b border-[#272727] hover:bg-[#262626] cursor-pointer transition-colors"
              @click="openCandidateDetails(candidate)"
            >
              <TableCell>
                <div class="flex items-center gap-1.5 text-sm font-medium">
                  <div
                    class="w-10 h-10 rounded-full bg-[#333] flex items-center justify-center text-xl"
                  >
                    {{ candidate.avatar }}
                  </div>
                  <div>{{ candidate.name }}</div>
                </div>
              </TableCell>
              <TableCell>
                <div class="flex items-center gap-1 text-sm font-medium tracking-wider">
                  <StarIcon :filled="true" class="w-4 h-4" />
                  <span>{{ candidate.rating }}</span>
                </div>
              </TableCell>
              <TableCell class="text-sm font-medium tracking-wider">
                {{ candidate.stage }}
              </TableCell>
              <TableCell class="text-sm font-medium tracking-wider">
                {{ candidate.role }}
              </TableCell>
              <TableCell class="text-sm font-medium tracking-wider">
                {{ candidate.date }}
              </TableCell>
              <TableCell>
                <div class="flex items-center gap-1 text-sm font-medium tracking-wider">
                  <AttachmentIcon class="w-4 h-4" />
                  <span>{{ candidate.files }} {{ candidate.files === 1 ? 'file' : 'files' }}</span>
                </div>
              </TableCell>
            </TableRow>
            <!-- Empty state when no results -->
            <TableRow v-if="noResults">
              <TableCell colspan="6" class="text-center py-8">
                <div class="text-[#898989] text-sm">
                  No candidates found for the selected filters
                </div>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </div>

    <!-- Candidate Details Sidebar -->
    <CandidateDetails
      :is-open="isSidebarOpen"
      :candidate="selectedCandidate"
      @close="closeSidebar"
      @stage-updated="handleStageUpdated"
    />
  </div>
</template>
