<template>
  <div>
    <header class="header">
      <div class="container header-inner">
        <router-link to="/" class="logo">
          <span>Р</span><span>Ж</span><span>Д</span>
        </router-link>

        <nav class="nav">
          <router-link to="/" class="nav-link">Главная</router-link>
          <router-link to="/tickets" class="nav-link">Все заявки</router-link>
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
              <router-link to="/profile" class="dropdown-item dropdown-item-active" @click="showMenu = false">
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
      <div class="profile-page">
        <div class="profile-hero">
          <div class="hero-bg-shapes">
            <div class="shape shape-1"></div>
            <div class="shape shape-2"></div>
            <div class="shape shape-3"></div>
          </div>
          
          <div class="hero-main">
            <div class="hero-left">
              <div class="avatar-wrap">
                <div class="avatar">{{ userInitials }}</div>
                <div class="avatar-ring"></div>
              </div>
            </div>
            
            <div class="hero-center">
              <div class="name-wrap">
                <h1>{{ authStore.user?.full_name }}</h1>
                <span class="role-badge" :class="authStore.user?.role">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                  {{ userRoles[authStore.user?.role] }}
                </span>
              </div>
              
              <div class="hero-meta-row">
                <div class="meta-tag">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                  {{ formatDate(authStore.user?.created_at) }}
                </div>
                <div class="meta-tag">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                  {{ authStore.user?.login }}
                </div>
                <div class="meta-tag" v-if="authStore.user?.department">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="9" y1="22" x2="15" y2="22"></line><line x1="12" y1="2" x2="12" y2="22"></line></svg>
                  {{ authStore.user?.department }}
                </div>
              </div>
            </div>
            
            <div class="hero-right">
              <button v-if="!editMode" class="btn-edit" @click="startEdit">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                Редактировать
              </button>
              <button v-else class="btn-cancel" @click="cancelEdit">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                Отмена
              </button>
            </div>
          </div>
        </div>

        <div v-if="editMode" class="edit-section">
          <div class="edit-card">
            <div class="edit-header">
              <h2><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>Редактирование профиля</h2>
            </div>
            <form @submit.prevent="saveProfile" class="edit-form">
              <div class="form-fields">
                <div class="field">
                  <label>ФИО</label>
                  <input v-model="editForm.full_name" type="text" />
                </div>
                <div class="field">
                  <label>Подразделение</label>
                  <select v-model="editForm.department_id">
                    <option :value="null">Не выбрано</option>
                    <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
                  </select>
                </div>
                <div class="field">
                  <label>Email</label>
                  <input v-model="editForm.email" type="email" />
                </div>
                <div class="field">
                  <label>Телефон</label>
                  <input v-model="editForm.phone" type="text" placeholder="+7 (XXX) XXX-XX-XX" />
                </div>
                <div class="field full">
                  <label>Новый пароль</label>
                  <input v-model="editForm.password" type="password" placeholder="Оставьте пустым, чтобы не менять" />
                </div>
              </div>
              <div class="form-btns">
                <button type="button" class="btn-sec" @click="cancelEdit">Отмена</button>
                <button type="submit" class="btn-pri">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>
                  Сохранить
                </button>
              </div>
            </form>
          </div>
        </div>

        <div class="profile-content">
          <div class="content-main">
            <div class="stats-row">
              <div class="stat-box">
                <div class="stat-icon red">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                </div>
                <div class="stat-info">
                  <span class="stat-num">{{ myTickets.length }}</span>
                  <span class="stat-lbl">Всего</span>
                </div>
              </div>
              <div class="stat-box">
                <div class="stat-icon blue">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                </div>
                <div class="stat-info">
                  <span class="stat-num">{{ getStatusCount('new') }}</span>
                  <span class="stat-lbl">Новых</span>
                </div>
              </div>
              <div class="stat-box">
                <div class="stat-icon yellow">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="2" x2="12" y2="22"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
                </div>
                <div class="stat-info">
                  <span class="stat-num">{{ getStatusCount('in_progress') }}</span>
                  <span class="stat-lbl">В работе</span>
                </div>
              </div>
              <div class="stat-box">
                <div class="stat-icon green">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                </div>
                <div class="stat-info">
                  <span class="stat-num">{{ getStatusCount('closed') }}</span>
                  <span class="stat-lbl">Закрыто</span>
                </div>
              </div>
            </div>

            <div class="info-grid-section">
              <div class="info-card-big">
                <div class="card-head">
                  <h3>Личная информация</h3>
                </div>
                <div class="info-list">
                  <div class="info-row">
                    <div class="info-icon-box">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                    </div>
                    <div class="info-text">
                      <span class="lbl">Полное имя</span>
                      <span class="val">{{ authStore.user?.full_name }}</span>
                    </div>
                  </div>
                  <div class="info-row">
                    <div class="info-icon-box">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
                    </div>
                    <div class="info-text">
                      <span class="lbl">Логин</span>
                      <span class="val code">{{ authStore.user?.login }}</span>
                    </div>
                  </div>
                  <div class="info-row">
                    <div class="info-icon-box">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                    </div>
                    <div class="info-text">
                      <span class="lbl">Роль</span>
                      <span class="val"><span class="role-tag" :class="authStore.user?.role">{{ userRoles[authStore.user?.role] }}</span></span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="info-card-big">
                <div class="card-head">
                  <h3>Контакты</h3>
                </div>
                <div class="contacts-list">
                  <a v-if="authStore.user?.email" :href="`mailto:${authStore.user?.email}`" class="contact-item">
                    <div class="contact-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                    </div>
                    <div class="contact-val">{{ authStore.user?.email }}</div>
                    <div class="contact-arrow">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                    </div>
                  </a>
                  <div v-else class="contact-item empty">
                    <div class="contact-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                    </div>
                    <div class="contact-val">Email не указан</div>
                  </div>
                  
                  <a v-if="authStore.user?.phone" :href="`tel:${authStore.user?.phone}`" class="contact-item">
                    <div class="contact-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
                    </div>
                    <div class="contact-val">{{ authStore.user?.phone }}</div>
                    <div class="contact-arrow">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                    </div>
                  </a>
                  <div v-else class="contact-item empty">
                    <div class="contact-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
                    </div>
                    <div class="contact-val">Телефон не указан</div>
                  </div>
                  
                  <div class="contact-item">
                    <div class="contact-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="9" y1="22" x2="15" y2="22"></line><line x1="12" y1="2" x2="12" y2="22"></line></svg>
                    </div>
                    <div class="contact-val">{{ authStore.user?.department || 'Не указано' }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="myTickets.length > 0" class="tickets-section">
              <div class="section-header">
                <h3>Мои заявки</h3>
                <router-link to="/my-tickets" class="view-all">Все <span class="count">{{ myTickets.length }}</span></router-link>
              </div>
              <div class="tickets-grid">
                <router-link v-for="ticket in myTickets.slice(0, 4)" :key="ticket.id" :to="`/tickets/${ticket.id}`" class="ticket-card-mini">
                  <div class="ticket-top">
                    <span class="ticket-id">#{{ ticket.id }}</span>
                    <span class="status-dot" :class="ticket.status"></span>
                  </div>
                  <div class="ticket-title">{{ ticket.title }}</div>
                  <div class="ticket-bottom">
                    <span class="status-lbl" :class="ticket.status">{{ ticketStatuses[ticket.status] }}</span>
                    <span class="ticket-date">{{ formatShortDate(ticket.created_at) }}</span>
                  </div>
                </router-link>
              </div>
            </div>
          </div>

          <div class="content-sidebar">
            <div class="actions-card">
              <div class="card-head">
                <h3>Действия</h3>
              </div>
              <div class="actions-list">
                <router-link to="/tickets/new" class="action-btn-main">
                  <div class="action-icon-main">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
                  </div>
                  <div class="action-text">
                    <span class="action-title">Создать заявку</span>
                    <span class="action-desc">Новое обращение</span>
                  </div>
                </router-link>
                <router-link to="/my-tickets" class="action-btn-main">
                  <div class="action-icon-main">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
                  </div>
                  <div class="action-text">
                    <span class="action-title">Мои заявки</span>
                    <span class="action-desc">{{ myTickets.length }} обращений</span>
                  </div>
                </router-link>
                <router-link to="/" class="action-btn-main">
                  <div class="action-icon-main">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
                  </div>
                  <div class="action-text">
                    <span class="action-title">На главную</span>
                    <span class="action-desc">Обзор системы</span>
                  </div>
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <transition name="fade">
          <div v-if="success" class="toast success">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
            {{ success }}
          </div>
        </transition>
        <transition name="fade">
          <div v-if="error" class="toast error">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
            {{ error }}
          </div>
        </transition>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const router = useRouter()
const authStore = useAuthStore()

const showMenu = ref(false)
const editMode = ref(false)
const departments = ref([])
const myTickets = ref([])
const error = ref('')
const success = ref('')

const editForm = reactive({
  full_name: '',
  email: '',
  phone: '',
  department_id: null,
  password: ''
})

const userInitials = computed(() => {
  if (!authStore.user?.full_name) return '?'
  return authStore.user.full_name.split(' ').map(n => n[0]).join('').slice(0, 2)
})

const userRoles = {
  employee: 'Сотрудник',
  specialist: 'Специалист',
  admin: 'Администратор'
}

const ticketStatuses = {
  new: 'Новая',
  in_progress: 'В работе',
  closed: 'Закрыта',
  rejected: 'Отклонена'
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}

const formatShortDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
}

const getStatusCount = (status) => {
  return myTickets.value.filter(t => t.status === status).length
}

const startEdit = () => {
  editForm.full_name = authStore.user?.full_name || ''
  editForm.email = authStore.user?.email || ''
  editForm.phone = authStore.user?.phone || ''
  editForm.department_id = authStore.user?.department_id
  editForm.password = ''
  editMode.value = true
}

const cancelEdit = () => {
  editMode.value = false
}

const loadDepartments = async () => {
  try {
    const res = await api.get('/departments')
    departments.value = res.data.departments
  } catch (e) {
    console.error('Failed to load departments:', e)
  }
}

const saveProfile = async () => {
  error.value = ''
  success.value = ''

  try {
    const data = {}
    if (editForm.full_name) data.full_name = editForm.full_name
    if (editForm.email !== undefined) data.email = editForm.email
    if (editForm.phone !== undefined) data.phone = editForm.phone
    if (editForm.department_id !== undefined) data.department_id = editForm.department_id
    if (editForm.password) data.password = editForm.password

    const updatedUser = await authStore.updateProfile(data)
    authStore.user = updatedUser
    editMode.value = false
    success.value = 'Профиль обновлён!'
    setTimeout(() => { success.value = '' }, 3000)
  } catch (e) {
    error.value = e.response?.data?.error || 'Ошибка сохранения'
    setTimeout(() => { error.value = '' }, 3000)
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

const loadMyTickets = async () => {
  try {
    const res = await api.get('/me/tickets')
    myTickets.value = res.data.tickets
  } catch (e) {
    console.error('Failed to load tickets:', e)
  }
}

onMounted(() => {
  loadDepartments()
  loadMyTickets()
})
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  padding-bottom: 48px;
}

.profile-hero {
  position: relative;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 48px 24px;
  overflow: hidden;
}

.hero-bg-shapes {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}

.shape-1 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(231, 76, 60, 0.2) 0%, transparent 70%);
  top: -150px;
  right: -50px;
}

.shape-2 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(52, 152, 219, 0.15) 0%, transparent 70%);
  bottom: -100px;
  left: -50px;
}

.shape-3 {
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(231, 76, 60, 0.1) 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.hero-main {
  position: relative;
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 32px;
}

.hero-left {
  flex-shrink: 0;
}

.avatar-wrap {
  position: relative;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 700;
  color: var(--accent);
  position: relative;
  z-index: 1;
}

.avatar-ring {
  position: absolute;
  inset: -6px;
  border-radius: 50%;
  border: 3px solid rgba(231, 76, 60, 0.5);
  animation: ringPulse 2s ease-in-out infinite;
}

@keyframes ringPulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 1; }
}

.hero-center {
  flex: 1;
}

.name-wrap {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.name-wrap h1 {
  font-size: 28px;
  font-weight: 700;
  color: #fff;
}

.role-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

.role-badge.employee {
  background: rgba(52, 152, 219, 0.2);
  color: #3498db;
}

.role-badge.specialist {
  background: rgba(241, 196, 15, 0.2);
  color: #f1c40f;
}

.role-badge.admin {
  background: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
}

.hero-meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.meta-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
}

.hero-right {
  flex-shrink: 0;
}

.btn-edit, .btn-cancel {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-edit {
  background: #fff;
  color: var(--accent);
  border: none;
}

.btn-edit:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.edit-section {
  max-width: 1100px;
  margin: -30px auto 24px;
  padding: 0 24px;
  position: relative;
  z-index: 1;
}

.edit-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid var(--border);
}

.edit-header h2 {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  margin-bottom: 20px;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field.full {
  grid-column: 1 / -1;
}

.field label {
  font-size: 13px;
  color: var(--text-secondary);
}

.field input, .field select {
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 14px;
  background: var(--bg-primary);
  color: var(--text-primary);
}

.field input:focus, .field select:focus {
  outline: none;
  border-color: var(--accent);
}

.form-btns {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 16px;
  border-top: 1px solid var(--border);
}

.btn-sec, .btn-pri {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.btn-sec {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border);
}

.btn-pri {
  background: var(--accent);
  color: #fff;
  border: none;
}

.profile-content {
  max-width: 1100px;
  margin: 24px auto 0;
  padding: 0 24px;
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
}

.content-main {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-box {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--border);
}

.stat-icon {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon.red {
  background: rgba(231, 76, 60, 0.15);
  color: var(--accent);
}

.stat-icon.blue {
  background: rgba(52, 152, 219, 0.15);
  color: var(--secondary);
}

.stat-icon.yellow {
  background: rgba(241, 196, 15, 0.15);
  color: var(--warning);
}

.stat-icon.green {
  background: rgba(46, 204, 113, 0.15);
  color: var(--success);
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-num {
  font-size: 26px;
  font-weight: 700;
}

.stat-lbl {
  font-size: 13px;
  color: var(--text-secondary);
}

.info-grid-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.info-card-big {
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--border);
  padding: 20px;
}

.card-head h3 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 16px;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px;
  background: var(--bg-primary);
  border-radius: 10px;
}

.info-icon-box {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--accent-light);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
}

.info-text {
  display: flex;
  flex-direction: column;
}

.info-text .lbl {
  font-size: 12px;
  color: var(--text-muted);
}

.info-text .val {
  font-weight: 500;
}

.info-text .val.code {
  font-family: monospace;
  padding: 2px 8px;
  background: var(--bg-tertiary);
  border-radius: 4px;
  font-size: 13px;
}

.role-tag {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
}

.role-tag.employee {
  background: rgba(52, 152, 219, 0.15);
  color: var(--secondary);
}

.role-tag.specialist {
  background: rgba(241, 196, 15, 0.15);
  color: var(--warning);
}

.role-tag.admin {
  background: rgba(231, 76, 60, 0.15);
  color: var(--accent);
}

.contacts-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px;
  background: var(--bg-primary);
  border-radius: 10px;
  transition: all 0.2s;
}

.contact-item:hover {
  background: var(--bg-tertiary);
  transform: translateX(4px);
}

.contact-item.empty {
  opacity: 0.5;
  cursor: default;
}

.contact-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(52, 152, 219, 0.15);
  color: var(--secondary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.contact-val {
  flex: 1;
  font-weight: 500;
}

.contact-arrow {
  color: var(--text-muted);
}

.tickets-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--border);
  padding: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  font-size: 15px;
  font-weight: 600;
}

.view-all {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--accent);
}

.view-all .count {
  background: var(--accent-light);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
}

.tickets-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.ticket-card-mini {
  padding: 14px;
  background: var(--bg-primary);
  border-radius: 10px;
  transition: all 0.2s;
}

.ticket-card-mini:hover {
  background: var(--bg-tertiary);
}

.ticket-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.ticket-id {
  font-family: monospace;
  font-size: 12px;
  color: var(--text-muted);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.new {
  background: var(--accent);
}

.status-dot.in_progress {
  background: var(--warning);
}

.status-dot.closed {
  background: var(--success);
}

.status-dot.rejected {
  background: var(--error);
}

.ticket-title {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 10px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ticket-bottom {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.status-lbl {
  font-weight: 500;
}

.status-lbl.new { color: var(--accent); }
.status-lbl.in_progress { color: var(--warning); }
.status-lbl.closed { color: var(--success); }
.status-lbl.rejected { color: var(--error); }

.ticket-date {
  color: var(--text-muted);
}

.content-sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.actions-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--border);
  padding: 20px;
}

.actions-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.action-btn-main {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-secondary) 100%);
  border-radius: 12px;
  transition: all 0.2s;
}

.action-btn-main:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(231, 76, 60, 0.3);
}

.action-icon-main {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.action-text {
  display: flex;
  flex-direction: column;
}

.action-title {
  font-size: 15px;
  font-weight: 600;
  color: #fff;
}

.action-desc {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
}

.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  background: var(--bg-secondary);
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}

.toast.success {
  border-left: 4px solid var(--success);
}

.toast.success svg {
  color: var(--success);
}

.toast.error {
  border-left: 4px solid var(--error);
}

.toast.error svg {
  color: var(--error);
}

.fade-enter-active, .fade-leave-active {
  transition: all 0.3s;
}

.fade-enter-from, .fade-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

@media (max-width: 900px) {
  .profile-content {
    grid-template-columns: 1fr;
  }
  
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .info-grid-section {
    grid-template-columns: 1fr;
  }
  
  .hero-main {
    flex-direction: column;
    text-align: center;
  }
  
  .name-wrap {
    justify-content: center;
  }
  
  .hero-meta-row {
    justify-content: center;
  }
  
  .hero-right {
    width: 100%;
  }
  
  .btn-edit, .btn-cancel {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 600px) {
  .stats-row {
    grid-template-columns: 1fr;
  }
  
  .tickets-grid {
    grid-template-columns: 1fr;
  }
  
  .form-fields {
    grid-template-columns: 1fr;
  }
}
</style>