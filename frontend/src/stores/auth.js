import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: state => !!state.user,
    isAdmin: state => state.user?.role === 'admin',
    isSpecialist: state => state.user?.role === 'specialist' || state.user?.role === 'admin'
  },

  actions: {
    async login(login, password) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post('/login', { login, password })
        this.user = response.data.user
        return true
      } catch (error) {
        this.error = error.response?.data?.error || 'Ошибка входа'
        return false
      } finally {
        this.loading = false
      }
    },

    async checkAuth() {
      try {
        const response = await api.get('/me')
        this.user = response.data.user
      } catch (error) {
        this.user = null
      }
    },

    async logout() {
      try {
        await api.post('/logout')
      } finally {
        this.user = null
      }
    },

    async updateProfile(data) {
      try {
        const response = await api.put('/profile', data)
        this.user = response.data.user
        return response.data.user
      } catch (error) {
        throw error.response?.data?.error || 'Ошибка обновления профиля'
      }
    }
  }
})