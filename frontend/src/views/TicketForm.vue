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
      <div class="create-page">
        <div class="page-decoration">
          <div class="deco-circle deco-1"></div>
          <div class="deco-circle deco-2"></div>
          <div class="deco-circle deco-3"></div>
        </div>

        <div class="create-card">
          <div class="card-sidebar">
            <div class="step-indicator">
              <div class="step" :class="{ stepActive: step === 1, stepDone: step > 1 }">
                <div class="step-num">1</div>
                <div class="step-text">Тип</div>
              </div>
              <div class="step-line" :class="{ stepLineActive: step > 1 }"></div>
              <div class="step" :class="{ stepActive: step === 2, stepDone: step > 2 }">
                <div class="step-num">2</div>
                <div class="step-text">Детали</div>
              </div>
              <div class="step-line" :class="{ stepLineActive: step > 2 }"></div>
              <div class="step" :class="{ stepActive: step === 3 }">
                <div class="step-num">3</div>
                <div class="step-text">Подтверждение</div>
              </div>
            </div>

            <div class="sidebar-info">
              <div class="info-box">
                <i class="fas fa-lightbulb"></i>
                <p>Выберите тип заявки, который лучше всего описывает вашу проблему</p>
              </div>
            </div>
          </div>

          <div class="card-body">
            <div v-if="error" class="error-banner">
              <i class="fas fa-circle-exclamation"></i>
              {{ error }}
            </div>

            <div v-if="step === 1" class="step-content">
              <div class="step-header">
                <h1 class="step-title">Выберите тип заявки</h1>
                <p class="step-description">Какой тип проблемы описывает вашу ситуацию?</p>
              </div>

              <div class="type-grid">
                <div
                  v-for="type in ticketTypes"
                  :key="type.value"
                  class="type-card"
                  :class="{ typeCardActive: form.type === type.value }"
                  @click="selectType(type.value)"
                >
                  <div class="type-icon-wrap">
                    <i :class="type.icon"></i>
                  </div>
                  <div class="type-content">
                    <h3>{{ type.label }}</h3>
                    <p>{{ type.description }}</p>
                  </div>
                  <div class="type-check">
                    <i class="fas fa-check"></i>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="step === 2" class="step-content">
              <div class="step-header">
                <h1 class="step-title">Заполните детали</h1>
                <p class="step-description">Опишите вашу проблему подробнее</p>
              </div>

              <form @submit.prevent="nextStep" class="detail-form">
                <div class="form-group">
                  <label class="label">Заголовок</label>
                  <input
                    v-model="form.title"
                    type="text"
                    class="input input-large"
                    placeholder="Кратко опишите проблему"
                    required
                  />
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label class="label">Приоритет</label>
                    <div class="priority-options">
                      <div
                        v-for="p in priorities"
                        :key="p.value"
                        class="priority-option"
                        :class="{ priorityOptionActive: form.priority === p.value }"
                        @click="form.priority = p.value"
                      >
                        <span class="badge" :class="p.badge">{{ p.label }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="form-group">
                  <label class="label">Описание проблемы</label>
                  <textarea
                    v-model="form.description"
                    class="textarea"
                    placeholder="Подробно опишите, что произошло, какие ошибки появились, какие действия вы предпринимали..."
                    rows="6"
                  ></textarea>
                  <div class="textarea-hint">
                    <i class="fas fa-info-circle"></i>
                    Чем подробнее описание, тем быстрее помогут
                  </div>
                </div>
              </form>
            </div>

            <div v-if="step === 3" class="step-content">
              <div class="step-header">
                <h1 class="step-title">Подтвердите заявку</h1>
                <p class="step-description">Проверьте информацию перед отправкой</p>
              </div>

              <div class="preview-card">
                <div class="preview-header">
                  <span class="badge" :class="getPriorityBadge(form.priority)">{{ getPriorityLabel(form.priority) }}</span>
                  <span class="type-label">{{ getTypeLabel(form.type) }}</span>
                </div>
                <h2 class="preview-title">{{ form.title || 'Без заголовка' }}</h2>
                <p class="preview-description">{{ form.description || 'Описание не указано' }}</p>
                <div class="preview-meta">
                  <div class="meta-item">
                    <i class="fas fa-user"></i>
                    <span>{{ authStore.user?.full_name }}</span>
                  </div>
                  <div class="meta-item">
                    <i class="fas fa-calendar"></i>
                    <span>{{ currentDate }}</span>
                  </div>
                </div>
              </div>

              <div v-if="error" class="error-message">
                <i class="fas fa-circle-exclamation"></i>
                {{ error }}
              </div>
            </div>

            <div class="form-navigation">
              <button
                v-if="step > 1"
                type="button"
                class="btn btn-ghost"
                @click="prevStep"
              >
                <i class="fas fa-arrow-left"></i>
                Назад
              </button>
              <div class="nav-spacer"></div>
              <button
                v-if="step < 3"
                type="button"
                class="btn btn-primary btn-lg"
                :disabled="!canProceed"
                @click="nextStep"
              >
                Далее
                <i class="fas fa-arrow-right"></i>
              </button>
              <button
                v-if="step === 3"
                type="button"
                class="btn btn-success btn-lg"
                :disabled="loading"
                @click="handleSubmit"
              >
                <i v-if="loading" class="fas fa-spinner fa-spin"></i>
                <span v-else>
                  <i class="fas fa-check"></i>
                  Создать заявку
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useTicketsStore } from '../stores/tickets'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const ticketsStore = useTicketsStore()

const showMenu = ref(false)
const step = ref(1)
const loading = ref(false)
const error = ref('')

const form = ref({
  title: '',
  type: '',
  priority: 'normal',
  description: ''
})

const ticketTypes = [
  {
    value: 'equipment',
    label: 'Оборудование',
    description: 'Ноутбук, мышь, клавиатура, монитор',
    icon: 'fas fa-laptop'
  },
  {
    value: 'software',
    label: 'Программное обеспечение',
    description: 'Установка, настройка, ошибки в программах',
    icon: 'fas fa-desktop'
  },
  {
    value: 'access',
    label: 'Доступы',
    description: 'Доступ к системам, папкам, ресурсам',
    icon: 'fas fa-key'
  }
]

const priorities = [
  { value: 'low', label: 'Низкий', badge: 'badge-low' },
  { value: 'normal', label: 'Обычный', badge: 'badge-normal' },
  { value: 'high', label: 'Высокий', badge: 'badge-high' },
  { value: 'critical', label: 'Критический', badge: 'badge-critical' }
]

const currentDate = computed(() => {
  return new Date().toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
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

const canProceed = computed(() => {
  if (step.value === 1) return !!form.value.type
  if (step.value === 2) return !!form.value.title
  return true
})

const selectType = (type) => {
  form.value.type = type
  if (route.query.type) {
    form.value.type = route.query.type
  }
}

const nextStep = () => {
  if (step.value < 3 && canProceed.value) {
    step.value++
  }
}

const prevStep = () => {
  if (step.value > 1) {
    step.value--
  }
}

const getPriorityBadge = (priority) => {
  const badges = {
    low: 'badge-low',
    normal: 'badge-normal',
    high: 'badge-high',
    critical: 'badge-critical'
  }
  return badges[priority] || 'badge-normal'
}

const getPriorityLabel = (priority) => {
  const labels = {
    low: 'Низкий',
    normal: 'Обычный',
    high: 'Высокий',
    critical: 'Критический'
  }
  return labels[priority] || 'Обычный'
}

const getTypeLabel = (type) => {
  const labels = {
    equipment: 'Оборудование',
    software: 'Программное обеспечение',
    access: 'Доступы'
  }
  return labels[type] || type
}

const handleSubmit = async () => {
  loading.value = true
  error.value = ''

  try {
    const ticket = await ticketsStore.createTicket(form.value)
    router.push(`/tickets/${ticket.id}`)
  } catch (e) {
    error.value = e
  } finally {
    loading.value = false
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(() => {
  if (route.query.type) {
    form.value.type = route.query.type
  }
})
</script>

<style scoped>
.create-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 24px;
  min-height: calc(100vh - 64px);
  position: relative;
}

.page-decoration {
  position: fixed;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
  z-index: 0;
}

.deco-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}

.deco-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(231, 76, 60, 0.08) 0%, transparent 70%);
  top: -200px;
  right: -100px;
}

.deco-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(52, 152, 219, 0.06) 0%, transparent 70%);
  bottom: -100px;
  left: -100px;
}

.deco-3 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(231, 76, 60, 0.05) 0%, transparent 70%);
  top: 40%;
  left: 30%;
}

.create-card {
  display: flex;
  gap: 0;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  width: 100%;
  max-width: 900px;
  position: relative;
  z-index: 1;
  box-shadow: var(--shadow-xl);
}

.card-sidebar {
  width: 240px;
  background: var(--bg-tertiary);
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.step-num {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  color: var(--text-muted);
  transition: var(--transition);
}

.stepActive .step-num {
  background: var(--accent);
  color: #fff;
}

.stepDone .step-num {
  background: var(--success);
  color: #fff;
}

.step-text {
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 500;
}

.stepActive .step-text {
  color: var(--text-primary);
}

.stepDone .step-text {
  color: var(--success);
}

.step-line {
  width: 2px;
  height: 24px;
  background: var(--border);
  margin: 4px 0;
}

.stepLineActive {
  background: var(--success);
}

.sidebar-info {
  margin-top: auto;
  padding-top: 24px;
}

.info-box {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.info-box i {
  color: var(--accent);
  font-size: 18px;
  flex-shrink: 0;
}

.info-box p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.card-body {
  flex: 1;
  padding: 32px;
}

.step-content {
  min-height: 360px;
}

.step-header {
  margin-bottom: 28px;
}

.step-title {
  font-family: var(--font-display);
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 8px;
}

.step-description {
  color: var(--text-secondary);
  font-size: 15px;
}

.type-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.type-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--bg-tertiary);
  border: 2px solid var(--border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: var(--transition);
}

.type-card:hover {
  border-color: var(--accent);
  transform: translateX(8px);
}

.typeCardActive {
  border-color: var(--accent);
  background: var(--accent-light);
}

.type-icon-wrap {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-md);
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: var(--accent);
  flex-shrink: 0;
}

.typeCardActive .type-icon-wrap {
  background: var(--accent);
  color: #fff;
}

.type-content {
  flex: 1;
}

.type-content h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.type-content p {
  font-size: 13px;
  color: var(--text-secondary);
}

.type-check {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  opacity: 0;
  transition: var(--transition);
}

.typeCardActive .type-check {
  opacity: 1;
  background: var(--accent);
}

.detail-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-large {
  padding: 16px;
  font-size: 16px;
}

.priority-options {
  display: flex;
  gap: 8px;
}

.priority-option {
  flex: 1;
}

.priority-option span {
  display: block;
  text-align: center;
  padding: 10px 8px;
  background: var(--bg-tertiary);
  border: 2px solid var(--border);
  border-radius: var(--radius-md);
  font-size: 13px;
  cursor: pointer;
  transition: var(--transition);
}

.priority-option:hover span {
  border-color: var(--accent);
}

.priorityOptionActive span {
  border-color: var(--accent);
  background: var(--accent-light);
}

.textarea-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  font-size: 13px;
  color: var(--text-muted);
}

.textarea-hint i {
  color: var(--accent);
}

.preview-card {
  padding: 24px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  margin-bottom: 24px;
}

.preview-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.type-label {
  font-size: 13px;
  color: var(--text-secondary);
}

.preview-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
}

.preview-description {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 20px;
  white-space: pre-wrap;
}

.preview-meta {
  display: flex;
  gap: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--border);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-muted);
}

.meta-item i {
  color: var(--accent);
}

.error-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  background: rgba(231, 76, 60, 0.1);
  border: 1px solid rgba(231, 76, 60, 0.3);
  border-radius: var(--radius-md);
  color: var(--accent);
  margin-bottom: 20px;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  background: rgba(231, 76, 60, 0.1);
  border: 1px solid rgba(231, 76, 60, 0.3);
  border-radius: var(--radius-md);
  color: var(--accent);
}

.form-navigation {
  display: flex;
  align-items: center;
  padding-top: 24px;
  border-top: 1px solid var(--border);
}

.nav-spacer {
  flex: 1;
}

.btn-success {
  background: var(--success);
  color: #fff;
  border-color: var(--success);
}

.btn-success:hover {
  background: #27ae60;
}

@media (max-width: 768px) {
  .create-card {
    flex-direction: column;
  }

  .card-sidebar {
    width: 100%;
    padding: 20px;
  }

  .step-indicator {
    flex-direction: row;
    justify-content: center;
    gap: 12px;
  }

  .step-line {
    width: 24px;
    height: 2px;
  }

  .sidebar-info {
    display: none;
  }

  .priority-options {
    flex-wrap: wrap;
  }

  .priority-option {
    flex: 1 1 45%;
  }
}
</style>