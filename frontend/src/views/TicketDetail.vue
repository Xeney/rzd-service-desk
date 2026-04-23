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
      <div class="detail-page">
        <div v-if="loading" class="loading-state">
          <i class="fas fa-spinner fa-spin"></i>
          <p>Загрузка заявки...</p>
        </div>

        <template v-else-if="ticket">
          <div class="detail-layout">
            <div class="detail-main">
              <div class="detail-card">
                <router-link to="/tickets" class="back-link">
                  <i class="fas fa-arrow-left"></i>
                  К списку заявок
                </router-link>

                <div class="ticket-header">
                  <div class="ticket-id-badge">#{{ ticket.id }}</div>
                  <h1 class="ticket-title">{{ ticket.title }}</h1>
                  <div class="ticket-badges">
                    <span class="badge" :class="`badge-${ticket.priority}`">
                      {{ ticketPriorities[ticket.priority] }}
                    </span>
                    <span class="badge" :class="`badge-${ticket.status}`">
                      {{ ticketStatuses[ticket.status] }}
                    </span>
                  </div>
                </div>

                <div class="ticket-meta-row">
                  <div class="meta-item">
                    <i class="fas fa-tag"></i>
                    <span>{{ ticketTypes[ticket.type] }}</span>
                  </div>
                  <div class="meta-item">
                    <i class="fas fa-calendar"></i>
                    <span>{{ formatDate(ticket.created_at) }}</span>
                  </div>
                </div>

                <div v-if="editMode" class="edit-panel">
                  <h3 class="section-title">Редактирование заявки</h3>

                  <div class="edit-form">
                    <div class="form-row">
                      <div class="form-group">
                        <label class="label">Статус</label>
                        <select v-model="editForm.status" class="select">
                          <option value="new">Новая</option>
                          <option value="in_progress">В работе</option>
                          <option value="closed">Закрыта</option>
                          <option value="rejected">Отклонена</option>
                        </select>
                      </div>

                      <div class="form-group">
                        <label class="label">Приоритет</label>
                        <select v-model="editForm.priority" class="select">
                          <option value="low">Низкий</option>
                          <option value="normal">Обычный</option>
                          <option value="high">Высокий</option>
                          <option value="critical">Критический</option>
                        </select>
                      </div>
                    </div>

                    <div v-if="canAssign" class="form-group">
                      <label class="label">Исполнитель</label>
                      <select v-model="editForm.assigned_to" class="select">
                        <option :value="null">Не назначен</option>
                        <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }}</option>
                      </select>
                    </div>

                    <div class="form-actions">
                      <button class="btn btn-primary" @click="saveChanges" :disabled="saving">
                        <i v-if="saving" class="fas fa-spinner fa-spin"></i>
                        <span v-else>Сохранить</span>
                      </button>
                      <button class="btn btn-secondary" @click="cancelEdit">Отмена</button>
                    </div>
                  </div>
                </div>

                <div v-if="!editMode && canEdit" class="edit-actions">
                  <button class="btn btn-secondary" @click="startEdit">
                    <i class="fas fa-edit"></i> Редактировать
                  </button>
                </div>

                <div class="ticket-description">
                  <h3 class="section-title">Описание</h3>
                  <p>{{ ticket.description || 'Описание не указано' }}</p>
                </div>
              </div>

              <div class="detail-card">
                <h3 class="section-title">
                  <i class="fas fa-comments"></i>
                  Комментарии
                </h3>

                <div v-if="ticket.comments?.length" class="comments-list">
                  <div v-for="comment in ticket.comments" :key="comment.id" class="comment-item">
                    <div class="comment-avatar">
                      {{ comment.user?.full_name?.split(' ').map(n => n[0]).join('').slice(0, 2) }}
                    </div>
                    <div class="comment-content">
                      <div class="comment-header">
                        <strong>{{ comment.user?.full_name }}</strong>
                        <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                      </div>
                      <p>{{ comment.text }}</p>
                    </div>
                  </div>
                </div>
                <p v-else class="empty-text">Нет комментариев</p>

                <div class="comment-form">
                  <textarea v-model="newComment" class="textarea" placeholder="Добавить комментарий..."></textarea>
                  <button class="btn btn-primary" @click="addComment" :disabled="!newComment">
                    <i class="fas fa-paper-plane"></i> Отправить
                  </button>
                </div>
              </div>

              <div v-if="ticket.history?.length" class="detail-card">
                <h3 class="section-title">
                  <i class="fas fa-history"></i>
                  История изменений
                </h3>

                <div class="history-list">
                  <div v-for="h in ticket.history" :key="h.id" class="history-item">
                    <span class="history-date">{{ formatDate(h.created_at) }}</span>
                    <strong>{{ h.changed_by?.full_name }}</strong>
                    изменил(а) {{ h.field }}:
                    <span class="old-value">{{ h.old_value || 'пусто' }}</span>
                    <i class="fas fa-arrow-right"></i>
                    <span class="new-value">{{ h.new_value }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="detail-sidebar">
              <div class="detail-card">
                <h3 class="section-title">Информация</h3>

                <div class="info-list">
                  <div class="info-row">
                    <div class="info-label">Создатель</div>
                    <div class="info-value">{{ ticket.created_by?.full_name }}</div>
                  </div>
                  <div class="info-row">
                    <div class="info-label">Подразделение</div>
                    <div class="info-value">{{ ticket.created_by?.department || '—' }}</div>
                  </div>
                  <div class="info-row">
                    <div class="info-label">Исполнитель</div>
                    <div class="info-value">{{ ticket.assigned_to?.full_name || 'Не назначен' }}</div>
                  </div>
                  <div class="info-row">
                    <div class="info-label">Тип</div>
                    <div class="info-value">{{ ticketTypes[ticket.type] }}</div>
                  </div>
                  <div class="info-row">
                    <div class="info-label">Создана</div>
                    <div class="info-value">{{ formatDate(ticket.created_at) }}</div>
                  </div>
                  <div class="info-row">
                    <div class="info-label">Обновлена</div>
                    <div class="info-value">{{ formatDate(ticket.updated_at) }}</div>
                  </div>
                </div>
              </div>

              <div class="detail-card">
                <h3 class="section-title">Вложения</h3>

                <div v-if="ticket.attachments?.length" class="attachments-list">
                  <a v-for="att in ticket.attachments" :key="att.id" :href="att.filepath" target="_blank" class="attachment-item">
                    <i class="fas fa-paperclip"></i>
                    <span>{{ att.filename }}</span>
                  </a>
                </div>
                <p v-else class="empty-text">Нет вложений</p>

                <div v-if="authStore.isSpecialist" class="file-upload">
                  <label class="btn btn-secondary btn-sm">
                    <i class="fas fa-upload"></i> Загрузить файл
                    <input type="file" @change="handleFileUpload" style="display: none" accept=".pdf,.png,.jpg,.jpeg,.gif" />
                  </label>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useTicketsStore } from '../stores/tickets'
import api from '../api'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const ticketsStore = useTicketsStore()

const showMenu = ref(false)
const loading = computed(() => ticketsStore.loading)
const ticket = computed(() => ticketsStore.currentTicket)
const users = ref([])

const editMode = ref(false)
const saving = ref(false)
const newComment = ref('')

const editForm = reactive({
  status: '',
  priority: '',
  assigned_to: null
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

const ticketTypes = { equipment: 'Оборудование', software: 'ПО', access: 'Доступ' }
const ticketPriorities = { low: 'Низкий', normal: 'Обычный', high: 'Высокий', critical: 'Критический' }
const ticketStatuses = { new: 'Новая', in_progress: 'В работе', closed: 'Закрыта', rejected: 'Отклоне��а' }

const canEdit = computed(() => {
  if (!ticket.value) return false
  const isCreator = ticket.value.created_by?.id === authStore.user?.id
  const isAssignee = ticket.value.assigned_to?.id === authStore.user?.id
  return isCreator || isAssignee || authStore.isAdmin
})

const canAssign = computed(() => {
  if (!ticket.value) return false
  const isAssignee = ticket.value.assigned_to?.id === authStore.user?.id
  return isAssignee || authStore.isAdmin
})

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleString('ru-RU')
}

const startEdit = () => {
  if (ticket.value) {
    editForm.status = ticket.value.status
    editForm.priority = ticket.value.priority
    editForm.assigned_to = ticket.value.assigned_to?.id
  }
  editMode.value = true
}

const cancelEdit = () => {
  editMode.value = false
}

const saveChanges = async () => {
  saving.value = true
  try {
    await ticketsStore.updateTicket(ticket.value.id, editForm)
    editMode.value = false
  } finally {
    saving.value = false
  }
}

const addComment = async () => {
  if (!newComment.value) return
  await ticketsStore.addComment(ticket.value.id, newComment.value)
  newComment.value = ''
}

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  await ticketsStore.uploadFile(ticket.value.id, file)
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(async () => {
  await ticketsStore.fetchTicket(route.params.id)
  if (ticket.value) {
    editForm.status = ticket.value.status
    editForm.priority = ticket.value.priority
    editForm.assigned_to = ticket.value.assigned_to?.id
  }
  if (authStore.isSpecialist) {
    const res = await api.get('/users')
    users.value = res.data.users
  }
})
</script>

<style scoped>
.detail-page {
  padding: 32px 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.detail-layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
}

.detail-main {
  display: flex;
  flex-direction: column;
  gap: 24px;
  min-width: 0;
}

.detail-sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.detail-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--text-muted);
  font-size: 14px;
  margin-bottom: 20px;
  transition: var(--transition);
}

.back-link:hover {
  color: var(--accent);
}

.ticket-header {
  margin-bottom: 20px;
}

.ticket-id-badge {
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.ticket-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 16px;
  line-height: 1.3;
}

.ticket-badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.ticket-meta-row {
  display: flex;
  gap: 24px;
  padding: 16px 0;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  margin-bottom: 20px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 14px;
}

.meta-item i {
  color: var(--text-muted);
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-title i {
  color: var(--accent);
}

.edit-actions {
  margin-bottom: 20px;
}

.edit-panel {
  background: var(--bg-tertiary);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 20px;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-actions {
  display: flex;
  gap: 12px;
  padding-top: 8px;
}

.ticket-description p {
  white-space: pre-wrap;
  line-height: 1.6;
  color: var(--text-secondary);
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
}

.comment-item {
  display: flex;
  gap: 12px;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--accent-light);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
  min-width: 0;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
  flex-wrap: wrap;
  gap: 8px;
}

.comment-date {
  font-size: 12px;
  color: var(--text-muted);
}

.comment-content p {
  font-size: 14px;
  line-height: 1.5;
}

.comment-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-start;
}

.empty-text {
  color: var(--text-muted);
  font-size: 14px;
  margin-bottom: 16px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-item {
  font-size: 14px;
  line-height: 1.5;
  padding: 12px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
}

.history-date {
  color: var(--text-muted);
  margin-right: 8px;
}

.old-value {
  color: var(--error);
  text-decoration: line-through;
}

.new-value {
  color: var(--success);
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.info-label {
  font-size: 13px;
  color: var(--text-muted);
}

.info-value {
  font-size: 13px;
  font-weight: 500;
  text-align: right;
}

.attachments-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.attachment-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  font-size: 13px;
  transition: var(--transition);
}

.attachment-item:hover {
  background: var(--border);
}

.loading-state {
  text-align: center;
  padding: 64px 24px;
  color: var(--text-muted);
}

.loading-state i {
  font-size: 24px;
  margin-bottom: 12px;
}

@media (max-width: 900px) {
  .detail-layout {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>