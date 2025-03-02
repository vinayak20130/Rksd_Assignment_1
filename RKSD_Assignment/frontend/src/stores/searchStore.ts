import { ref } from 'vue'

// Create a reactive search query that can be shared between components
export const searchQuery = ref('')

// Function to clear the search
export const clearSearch = () => {
  searchQuery.value = ''
}
