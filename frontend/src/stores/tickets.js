import { defineStore } from 'pinia'
import api from '../api'

export const useTicketsStore = defineStore('tickets', {
  state: () => ({
    tickets: [],
    currentTicket: null,
    stats: null,
    loading: false,
    error: null
  }),

  actions: {
    async fetchTickets(filters = {}) {
      this.loading = true
      try {
        const params = new URLSearchParams(filters).toString()
        const response = await api.get(`/tickets?${params}`)
        this.tickets = response.data.tickets
      } catch (error) {
        this.error = error.response?.data?.error || 'Ошибка загрузки'
      } finally {
        this.loading = false
      }
    },

    async fetchTicket(id) {
      this.loading = true
      try {
        const response = await api.get(`/tickets/${id}`)
        this.currentTicket = response.data.ticket
      } catch (error) {
        this.error = error.response?.data?.error || 'Ошибка загрузки'
      } finally {
        this.loading = false
      }
    },

    async createTicket(data) {
      try {
        const response = await api.post('/tickets', data)
        this.tickets.unshift(response.data.ticket)
        return response.data.ticket
      } catch (error) {
        throw error.response?.data?.error || 'Ошибка создания'
      }
    },

    async updateTicket(id, data) {
      try {
        const response = await api.put(`/tickets/${id}`, data)
        const index = this.tickets.findIndex(t => t.id === id)
        if (index !== -1) {
          this.tickets[index] = response.data.ticket
        }
        this.currentTicket = response.data.ticket
        return response.data.ticket
      } catch (error) {
        throw error.response?.data?.error || 'Ошибка обновления'
      }
    },

    async addComment(ticketId, text) {
      try {
        const response = await api.post(`/tickets/${ticketId}/comments`, { text })
        if (this.currentTicket?.id === ticketId) {
          this.currentTicket.comments.push(response.data.comment)
        }
        return response.data.comment
      } catch (error) {
        throw error.response?.data?.error || 'Ошибка добавления комментария'
      }
    },

    async uploadFile(ticketId, file) {
      try {
        const formData = new FormData()
        formData.append('file', file)
        const response = await api.post(`/tickets/${ticketId}/attachments`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        if (this.currentTicket?.id === ticketId) {
          this.currentTicket.attachments.push(response.data.attachment)
        }
        return response.data.attachment
      } catch (error) {
        throw error.response?.data?.error || 'Ошибка загрузки файла'
      }
    },

    async fetchStats() {
      try {
        const response = await api.get('/dashboard/stats')
        this.stats = response.data
      } catch (error) {
        this.error = error.response?.data?.error || 'Ошибка загрузки'
      }
    }
  }
})