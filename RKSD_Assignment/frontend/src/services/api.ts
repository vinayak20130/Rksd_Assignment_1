import axios from 'axios'

// Create an axios instance with the base URL of your FastAPI backend
const api = axios.create({
  baseURL: 'http://localhost:8000', // Adjust this to match your FastAPI server URL
  headers: {
    'Content-Type': 'application/json',
  },
})

// Types for API responses
export interface StageInfo {
  current_stage: number
  stage_name: string
  stage_sequence: number
}

export interface Candidate {
  application_id: number
  candidate_name: string
  role_name: string
  rating: number
  application_date: string
  attachments: number
  status: string
  stage: StageInfo | null
}

// Interface for detailed application information
export interface Experience {
  experience_id: number
  company_name: string
  position: string
  start_date: string
  end_date: string
  description: string
}

export interface RoleStage {
  stage_id: number
  stage_name: string
  stage_sequence: number
}

export interface ApplicationDetails {
  application_id: number
  candidate_id: number
  candidate_name: string
  role_id: number
  role_name: string
  current_stage_id: number
  current_stage_name: string
  current_stage_sequence: number
  status: string
  application_date: string
  experiences: Experience[]
  role_stages: RoleStage[]
}

// Function to get detailed applications with optional year and month filters
export const getDetailedApplicationsByMonth = async (
  year?: number,
  month?: number,
  status?: string,
) => {
  try {
    const response = await api.post('/applications/by-month/detailed', {
      year: year || undefined,
      month: month || undefined,
      status_filter: status || 'All',
    })
    return response.data as Candidate[]
  } catch (error) {
    console.error('Error fetching applications:', error)
    throw error
  }
}

// Function to get detailed information for a specific application
export const getApplicationDetails = async (applicationId: number) => {
  try {
    const response = await api.get(`/applications/${applicationId}/details`)
    return response.data as ApplicationDetails
  } catch (error) {
    console.error(`Error fetching application details for ID ${applicationId}:`, error)
    throw error
  }
}

// Function to update application stage (next stage or reject)
export const updateApplicationStage = async (applicationId: number, action: 'next' | 'reject') => {
  try {
    const response = await api.post(`/applications/${applicationId}/update-stage`, { action })
    return response.data
  } catch (error) {
    console.error(`Error updating application stage for ID ${applicationId}:`, error)
    throw error
  }
}

// Function to get all available application months
export const getAvailableApplicationMonths = async () => {
  try {
    // First try to get from dedicated endpoint
    const response = await api.get('/applications/available-months')
    return response.data as { year: number; month: number }[]
  } catch (error) {
    console.error(
      'Error fetching available months from endpoint, trying alternative method:',
      error,
    )

    try {
      // If dedicated endpoint fails, get all applications and extract months
      const allApplicationsResponse = await api.get('/applications/all')
      const allApplications = allApplicationsResponse.data as Candidate[]

      // Extract unique year/month combinations
      const uniqueMonths = new Set<string>()
      const result: { year: number; month: number }[] = []

      allApplications.forEach((app) => {
        const date = new Date(app.application_date)
        const year = date.getFullYear()
        const month = date.getMonth() + 1
        const key = `${year}-${month}`

        if (!uniqueMonths.has(key)) {
          uniqueMonths.add(key)
          result.push({ year, month })
        }
      })

      return result
    } catch (secondError) {
      console.error('Error fetching all applications:', secondError)
      // Return current month and previous 3 months as fallback
      const now = new Date()
      const result = []
      for (let i = 0; i < 4; i++) {
        const date = new Date(now.getFullYear(), now.getMonth() - i, 1)
        result.push({ year: date.getFullYear(), month: date.getMonth() + 1 })
      }
      return result
    }
  }
}

export default api
