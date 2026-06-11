import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const isAuthenticated = ref(false)
  const loading = ref(false)

  async function fetchUser() {
    loading.value = true
    try {
      const response = await axios.get('/api/auth/user/', { withCredentials: true })
      if (response.data.id) {
        user.value = response.data
        isAuthenticated.value = true
      } else {
        user.value = null
        isAuthenticated.value = false
      }
    } catch (error) {
      user.value = null
      isAuthenticated.value = false
    } finally {
      loading.value = false
    }
  }

  async function login(username, password) {
    try {
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)
      
      const response = await axios.post('/api/auth/login/', formData, {
        withCredentials: true,
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      
      if (response.data.success) {
        await fetchUser()
        return true
      }
      return false
    } catch (error) {
      console.error('Login error:', error)
      return false
    }
  }

  async function logout() {
    try {
      await axios.post('/api/auth/logout/', {}, { withCredentials: true })
      user.value = null
      isAuthenticated.value = false
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  return { user, isAuthenticated, loading, fetchUser, login, logout }
})