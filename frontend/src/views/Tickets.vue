<template>
  <div>
    <header class="header">
      <div class="container header-inner">
        <router-link to="/" class="logo">
          <span>Р</span><span>Ж</span><span>Д</span>
        </router-link>

        <nav class="nav">
          <router-link to="/" class="nav-link">Главная</router-link>
          <router-link to="/tickets" class="nav-link nav-link-active">Все заявки</router-link>
          <router-link to="/my-tickets" class="nav-link">Мои заявки</router-link>
        </nav>

        <div class="user-menu">
          <router-link to="/tickets/new" class="btn btn-primary">
            <i class="fas fa-plus"></i>
            Новая заявка
          </router-link>

          <div class="dropdown">
            <button class="user-avatar" @click="showMenu = !showMenu">
              {{ userInitials }}
            </button>

            <div v-if="showMenu" class="dropdown-menu">
              <div class="dropdown-header">
                <div class="dropdown-user-name">{{ authStore.user?.full_name }}</div>
                <div class="dropdown-user-role">{{ userRoles[authStore.user?.role] }}</div>
              </div>
              <router-link to="/profile" class="dropdown-item" @click="showMenu = false">
                <i class="fas fa-user"></i>
                Профиль
              </router-link>
              <router-link v-if="authStore.isAdmin" to="/admin" class="dropdown-item" @click="showMenu = false">
                <i class="fas fa-cog"></i>
                Админ-панель
              </router-link>
              <button class="dropdown-item dropdown-item-danger" @click="handleLogout">
                <i class="fas fa-sign-out-alt"></i>
                Выйти
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

<main class="main-content">
      <div class="page-layout">
        <aside class="filters-sidebar">
          <div class="filter-block">
            <h3 class="filter-title">Поиск</h3>
            <input
              v-model="searchQuery"
              type="text"
              class="input search-input"
              placeholder="Поиск по заявкам..."
              @input="handleSearch"
            />
          </div>

          <template v-if="authStore.isSpecialist">
            <div class="filter-block">
              <h3 class="filter-title">Мои заявки</h3>
              <select v-model="filters.assignee" class="select filter-select" @change="loadTickets">
                <option value="">Все заявки</option>
                <option value="me">Назначенные на меня</option>
                <option value="unassigned">Неназначенные</option>
              </select>
            </div>
          </template>

          <div class="filter-block">
            <h3 class="filter-title">Статус</h3>
            <select v-model="filters.status" class="select filter-select" @change="loadTickets">
              <option value="">Все</option>
              <option value="new">Новые</option>
              <option value="in_progress">В работе</option>
              <option value="closed">Закрытые</option>
              <option value="rejected">Отклонённые</option>
            </select>
          </div>

          <div class="filter-block">
            <h3 class="filter-title">Приоритет</h3>
            <select v-model="filters.priority" class="select filter-select" @change="loadTickets">
              <option value="">Все</option>
              <option value="low">Низкий</option>
              <option value="normal">Обычный</option>
              <option value="high">Высокий</option>
              <option value="critical">Критический</option>
            </select>
          </div>

          <div class="filter-block">
            <h3 class="filter-title">Тип</h3>
            <select v-model="filters.type" class="select filter-select" @change="loadTickets">
              <option value="">Все</option>
              <option value="equipment">Оборудование</option>
              <option value="software">ПО</option>
              <option value="access">Доступ</option>
            </select>
          </div>

          <button v-if="hasActiveFilters" class="btn btn-secondary btn-sm" @click="clearFilters">
            <i class="fas fa-times"></i>
            Сбросить
          </button>
        </aside>

        <div class="page-main">
          <div class="page-header">
            <div>
              <h1 class="page-title">Все заявки</h1>
              <p class="page-subtitle">Просмотр и фильтрация заявок в системе</p>
            </div>
            <router-link to="/tickets/new" class="btn btn-primary">
              <i class="fas fa-plus"></i>
              Создать заявку
            </router-link>
          </div>

          <div class="stats-bar">
            <div class="stat-pill">
              <span class="stat-count">{{ filteredTickets.length }}</span>
              <span class="stat-label">заявок</span>
            </div>
            <div class="stat-pill stat-pill-new">
              <span class="stat-count">{{ stats.new || 0 }}</span>
              <span class="stat-label">новых</span>
            </div>
            <div class="stat-pill stat-pill-progress">
              <span class="stat-count">{{ stats.in_progress || 0 }}</span>
              <span class="stat-label">в работе</span>
            </div>
            <div class="stat-pill stat-pill-closed">
              <span class="stat-count">{{ stats.closed || 0 }}</span>
              <span class="stat-label">закрыто</span>
            </div>
          </div>

          <div v-if="loading" class="loading-state">
            <i class="fas fa-spinner fa-spin"></i>
            <p>Загрузка заявок...</p>
          </div>

          <div v-else-if="filteredTickets.length === 0" class="empty-state">
            <div class="empty-icon">
              <i class="fas fa-inbox"></i>
            </div>
            <h3 class="empty-title">Заявки не найдены</h3>
            <p class="empty-text">
              {{ hasFilters ? 'Попробуйте изменить параметры поиска' : 'Создайте первую заявку' }}
            </p>
            <router-link v-if="!hasFilters" to="/tickets/new" class="btn btn-primary">
              <i class="fas fa-plus"></i>
              Создать заявку
            </router-link>
          </div>

          <div v-else class="tickets-grid">
            <TicketCard
              v-for="ticket in filteredTickets"
              :key="ticket.id"
              :ticket="ticket"
              show-creator
            />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import TicketCard from '../components/TicketCard.vue'
import api from '../api'

const router = useRouter()
const authStore = useAuthStore()

const showMenu = ref(false)
const loading = ref(false)
const tickets = ref([])
const stats = ref({})
const searchQuery = ref('')
const filters = ref({
  status: '',
  priority: '',
  type: '',
  assignee: ''
})

let searchTimeout = null

const handleSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadTickets()
  }, 300)
}

const userInitials = computed(() => {
  if (!authStore.user?.full_name) return '?'
  return authStore.user.full_name.split(' ').map(n => n[0]).join('').slice(0, 2)
})

const userRoles = {
  employee: 'Сотрудник',
  specialist: 'Специалист',
  admin: 'Администратор'
}

const hasFilters = computed(() => {
  return searchQuery.value ||
    filters.value.status ||
    filters.value.priority ||
    filters.value.type ||
    filters.value.assignee
})

const hasActiveFilters = computed(() => hasFilters.value)

const clearFilters = () => {
  searchQuery.value = ''
  filters.value = { status: '', priority: '', type: '', assignee: '' }
  loadTickets()
}

const filteredTickets = computed(() => {
  if (!searchQuery.value) return tickets.value

  const query = searchQuery.value.toLowerCase()
  return tickets.value.filter(
    t => t.title.toLowerCase().includes(query) ||
      t.description?.toLowerCase().includes(query)
  )
})

const loadTickets = async () => {
  loading.value = true
  try {
    const params = {}
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.priority) params.priority = filters.value.priority
    if (filters.value.type) params.type = filters.value.type
    if (filters.value.assignee === 'me') params.assigned_to_me = 'true'
    if (filters.value.assignee === 'unassigned') params.unassigned = 'true'

    const res = await api.get('/tickets', { params })
    tickets.value = res.data.tickets
  } catch (e) {
    console.error('Failed to load tickets:', e)
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    const res = await api.get('/dashboard/stats')
    stats.value = res.data
  } catch (e) {
    console.error('Failed to load stats:', e)
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(() => {
  loadTickets()
  loadStats()
})

onUnmounted(() => {
  clearTimeout(searchTimeout)
})
</script>

<style scoped>
.page-layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px 24px;
}

.filters-sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  height: fit-content;
  position: sticky;
  top: 88px;
}

.filter-block {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-title {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.search-input {
  padding: 10px 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-size: 14px;
  background: var(--bg-primary);
  width: 100%;
}

.search-input:focus {
  outline: none;
  border-color: var(--accent);
}

.filter-select {
  padding: 10px 14px;
  font-size: 13px;
  background-color: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  cursor: pointer;
  width: 100%;
}

.filter-select:focus {
  outline: none;
  border-color: var(--accent);
}

.page-main {
  min-width: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.page-title {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 4px;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 15px;
}

.stats-bar {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.stat-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  white-space: nowrap;
}

.stat-count {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
}

.stat-pill-new .stat-count { color: var(--accent); }
.stat-pill-progress .stat-count { color: var(--warning); }
.stat-pill-closed .stat-count { color: var(--success); }

.loading-state i {
  font-size: 24px;
}

.tickets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}

@media (max-width: 900px) {
  .page-layout {
    grid-template-columns: 1fr;
  }

  .filters-sidebar {
    position: static;
  }

  .page-header {
    flex-direction: column;
  }

  .tickets-grid {
    grid-template-columns: 1fr;
  }
}
</style>