<template>
  <div>
    <header class="header">
      <div class="container header-inner">
        <router-link to="/" class="logo">
          <span>Р</span><span>Ж</span><span>Д</span>
        </router-link>

        <nav class="nav">
          <router-link to="/" class="nav-link nav-link-active">Главная</router-link>
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
      <div class="page-container">
        <div class="hero-section">
          <div class="hero-bg">
            <div class="particles" ref="particlesRef">
              <div v-for="i in 50" :key="i" class="particle" :style="getParticleStyle(i)"></div>
            </div>
            
            <div class="tracks">
              <div class="track track-left">
                <div class="rail"></div>
                <div class="ties">
                  <div v-for="i in 20" :key="i" class="tie" :style="{ animationDelay: `${i * 0.1}s` }"></div>
                </div>
              </div>
              <div class="track track-right">
                <div class="rail"></div>
                <div class="ties">
                  <div v-for="i in 20" :key="i" class="tie" :style="{ animationDelay: `${i * 0.1}s` }"></div>
                </div>
              </div>
            </div>

            <div class="train-container">
              <div class="train">
                <div class="train-body">
                  <div class="train-window"></div>
                  <div class="train-window"></div>
                  <div class="train-window"></div>
                  <div class="train-lights">
                    <div class="light-front"></div>
                    <div class="light-front"></div>
                  </div>
                </div>
                <div class="train-wheels">
                  <div class="wheel"></div>
                  <div class="wheel"></div>
                  <div class="wheel"></div>
                </div>
                <div class="smoke">
                  <div class="smoke-puff"></div>
                  <div class="smoke-puff"></div>
                  <div class="smoke-puff"></div>
                </div>
              </div>
            </div>

            <div class="glow glow-1"></div>
            <div class="glow glow-2"></div>
            <div class="glow glow-3"></div>
            
            <div class="floating-elements">
              <div class="floating-icon icon-1"><i class="fas fa-wrench"></i></div>
              <div class="floating-icon icon-2"><i class="fas fa-laptop"></i></div>
              <div class="floating-icon icon-3"><i class="fas fa-key"></i></div>
              <div class="floating-icon icon-4"><i class="fas fa-cog"></i></div>
              <div class="floating-icon icon-5"><i class="fas fa-tools"></i></div>
            </div>
          </div>

          <div class="hero-content">
            <div class="hero-badge" :class="{ visible: badgeVisible }">
              <span class="badge-icon">🚂</span>
              <span>Сервис для сотрудников РЖД</span>
            </div>
            <h1 class="hero-title">
              <span class="title-service" :class="{ visible: titleVisible }">Service</span>
              <span class="title-desk" :class="{ visible: titleVisible }">Desk</span>
            </h1>
            <p class="hero-description" :class="{ visible: descVisible }">
              Единая система обработки заявок. Создавайте заявки на оборудование,<br/>
              программное обеспечение и доступы — всё в одном месте.
            </p>
            <div class="hero-actions" :class="{ visible: actionsVisible }">
              <router-link to="/tickets/new" class="btn btn-lg btn-hero-primary">
                <i class="fas fa-plus-circle"></i>
                Создать заявку
              </router-link>
              <router-link to="/my-tickets" class="btn btn-lg btn-hero-secondary">
                <i class="fas fa-list-ul"></i>
                Мои заявки
              </router-link>
            </div>
          </div>

          <div class="hero-stats-row">
            <div class="stat-card-hero stat-card-main" :class="{ visible: statsVisible }">
              <div class="stat-icon-hero">
                <i class="fas fa-ticket-alt"></i>
              </div>
              <div class="stat-content-hero">
                <span class="stat-number-hero">{{ stats.total || 0 }}</span>
                <span class="stat-label-hero">Всего заявок</span>
              </div>
            </div>
            <div class="stat-card-hero stat-card-new" :class="{ visible: statsVisible }">
              <div class="stat-icon-hero">
                <i class="fas fa-plus-circle"></i>
              </div>
              <div class="stat-content-hero">
                <span class="stat-number-hero">{{ stats.new || 0 }}</span>
                <span class="stat-label-hero">Новых</span>
              </div>
            </div>
            <div class="stat-card-hero stat-card-progress" :class="{ visible: statsVisible }">
              <div class="stat-icon-hero">
                <i class="fas fa-spinner"></i>
              </div>
              <div class="stat-content-hero">
                <span class="stat-number-hero">{{ stats.in_progress || 0 }}</span>
                <span class="stat-label-hero">В работе</span>
              </div>
            </div>
            <div class="stat-card-hero stat-card-closed" :class="{ visible: statsVisible }">
              <div class="stat-icon-hero">
                <i class="fas fa-check-circle"></i>
              </div>
              <div class="stat-content-hero">
                <span class="stat-number-hero">{{ stats.closed || 0 }}</span>
                <span class="stat-label-hero">Закрыто</span>
              </div>
            </div>
          </div>
        </div>

        <div class="dashboard-grid">
          <div class="dashboard-main">
            <section class="quick-actions-section">
              <h2 class="section-title">
                <i class="fas fa-bolt"></i>
                Быстрые действия
              </h2>
              <div class="quick-actions-grid">
                <router-link to="/tickets/new?type=equipment" class="quick-action-card">
                  <div class="quick-action-icon">
                    <i class="fas fa-laptop"></i>
                  </div>
                  <div class="quick-action-info">
                    <h3>Оборудование</h3>
                    <p>Ноутбук, мышь, клавиатура</p>
                  </div>
                  <div class="quick-action-arrow">
                    <i class="fas fa-arrow-right"></i>
                  </div>
                </router-link>
                <router-link to="/tickets/new?type=software" class="quick-action-card">
                  <div class="quick-action-icon">
                    <i class="fas fa-desktop"></i>
                  </div>
                  <div class="quick-action-info">
                    <h3>Программное обеспечение</h3>
                    <p>Установка и настройка ПО</p>
                  </div>
                  <div class="quick-action-arrow">
                    <i class="fas fa-arrow-right"></i>
                  </div>
                </router-link>
                <router-link to="/tickets/new?type=access" class="quick-action-card">
                  <div class="quick-action-icon">
                    <i class="fas fa-key"></i>
                  </div>
                  <div class="quick-action-info">
                    <h3>Доступы</h3>
                    <p>Системы, папки, ресурсы</p>
                  </div>
                  <div class="quick-action-arrow">
                    <i class="fas fa-arrow-right"></i>
                  </div>
                </router-link>
              </div>
            </section>

            <section class="dashboard-section">
              <h2 class="section-title">
                <i class="fas fa-chart-pie"></i>
                Статистика заявок
              </h2>
              <div class="stats-detailed-grid">
                <div class="status-chart">
                  <h3>По статусу</h3>
                  <div class="chart-bars">
                    <div
                      v-for="status in statusStats"
                      :key="status.key"
                      class="status-bar"
                    >
                      <div class="status-bar-header">
                        <span class="status-dot" :style="{ background: status.color }"></span>
                        <span class="status-label">{{ status.label }}</span>
                        <span class="status-count">{{ status.count }}</span>
                      </div>
                      <div class="status-bar-track">
                        <div
                          class="status-bar-fill"
                          :style="{ width: status.percent + '%', background: status.color }"
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="priority-breakdown">
                  <h3>По приоритету</h3>
                  <div class="priority-items">
                    <div class="priority-row">
                      <div class="priority-left">
                        <span class="badge badge-critical">Критический</span>
                      </div>
                      <div class="priority-right">
                        <span class="priority-num">{{ stats.priority_stats?.critical || 0 }}</span>
                      </div>
                    </div>
                    <div class="priority-row">
                      <div class="priority-left">
                        <span class="badge badge-high">Высокий</span>
                      </div>
                      <div class="priority-right">
                        <span class="priority-num">{{ stats.priority_stats?.high || 0 }}</span>
                      </div>
                    </div>
                    <div class="priority-row">
                      <div class="priority-left">
                        <span class="badge badge-normal">Обычный</span>
                      </div>
                      <div class="priority-right">
                        <span class="priority-num">{{ stats.priority_stats?.normal || 0 }}</span>
                      </div>
                    </div>
                    <div class="priority-row">
                      <div class="priority-left">
                        <span class="badge badge-low">Низкий</span>
                      </div>
                      <div class="priority-right">
                        <span class="priority-num">{{ stats.priority_stats?.low || 0 }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="type-breakdown">
                  <h3>По типу</h3>
                  <div class="type-cards">
                    <div class="type-item">
                      <div class="type-icon-wrap">
                        <i class="fas fa-laptop"></i>
                      </div>
                      <div class="type-details">
                        <span class="type-num">{{ stats.type_stats?.equipment || 0 }}</span>
                        <span class="type-label">Оборудование</span>
                      </div>
                    </div>
                    <div class="type-item">
                      <div class="type-icon-wrap">
                        <i class="fas fa-desktop"></i>
                      </div>
                      <div class="type-details">
                        <span class="type-num">{{ stats.type_stats?.software || 0 }}</span>
                        <span class="type-label">ПО</span>
                      </div>
                    </div>
                    <div class="type-item">
                      <div class="type-icon-wrap">
                        <i class="fas fa-key"></i>
                      </div>
                      <div class="type-details">
                        <span class="type-num">{{ stats.type_stats?.access || 0 }}</span>
                        <span class="type-label">Доступы</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <section v-if="authStore.isSpecialist && stats.my_assigned" class="dashboard-section specialist-section">
              <div class="specialist-card">
                <div class="specialist-icon-wrap">
                  <i class="fas fa-user-check"></i>
                </div>
                <div class="specialist-content">
                  <h3>Ваши задачи</h3>
                  <p>{{ stats.my_assigned }} заявок назначено на вас</p>
                </div>
                <router-link to="/tickets?assigned=me" class="btn btn-white">
                  Посмотреть
                  <i class="fas fa-arrow-right"></i>
                </router-link>
              </div>
            </section>
          </div>

          <div class="dashboard-sidebar">
            <section class="dashboard-section about-section">
              <div class="about-hero">
                <div class="about-emblem">
                  <i class="fas fa-train"></i>
                </div>
                <h3>Service Desk</h3>
                <p class="about-tagline">Единая система заявок РЖД</p>
                <span class="about-version">Версия 1.0.0</span>
              </div>
              <div class="about-features-list">
                <div class="feature-row">
                  <i class="fas fa-check"></i>
                  <span>Три типа заявок</span>
                </div>
                <div class="feature-row">
                  <i class="fas fa-check"></i>
                  <span>Четыре уровня приоритета</span>
                </div>
                <div class="feature-row">
                  <i class="fas fa-check"></i>
                  <span>Отслеживание статусов</span>
                </div>
                <div class="feature-row">
                  <i class="fas fa-check"></i>
                  <span>Комментарии и файлы</span>
                </div>
                <div class="feature-row">
                  <i class="fas fa-check"></i>
                  <span>История изменений</span>
                </div>
              </div>
            </section>

            <section class="dashboard-section help-section">
              <h2 class="section-title">
                <i class="fas fa-question-circle"></i>
                Как создать заявку
              </h2>
              <div class="help-steps">
                <div class="help-step">
                  <div class="help-num">1</div>
                  <div class="help-text">
                    <h4>Нажмите "Создать заявку"</h4>
                    <p>Кнопка в верхнем меню</p>
                  </div>
                </div>
                <div class="help-step">
                  <div class="help-num">2</div>
                  <div class="help-text">
                    <h4>Заполните форму</h4>
                    <p>Выберите тип и приоритет</p>
                  </div>
                </div>
                <div class="help-step">
                  <div class="help-num">3</div>
                  <div class="help-text">
                    <h4>Отправьте заявку</h4>
                    <p>Ожидайте обработки</p>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const router = useRouter()
const authStore = useAuthStore()
const particlesRef = ref(null)

const showMenu = ref(false)
const stats = ref({})

const badgeVisible = ref(false)
const titleVisible = ref(false)
const descVisible = ref(false)
const actionsVisible = ref(false)
const statsVisible = ref(false)

const userInitials = computed(() => {
  if (!authStore.user?.full_name) return '?'
  return authStore.user.full_name.split(' ').map(n => n[0]).join('').slice(0, 2)
})

const userRoles = {
  employee: 'Сотрудник',
  specialist: 'Специалист',
  admin: 'Администратор'
}

const getParticleStyle = (i) => {
  const x = Math.random() * 100
  const y = Math.random() * 100
  const size = 4 + Math.random() * 8
  const duration = 15 + Math.random() * 20
  const delay = Math.random() * 10
  return {
    left: `${x}%`,
    top: `${y}%`,
    width: `${size}px`,
    height: `${size}px`,
    animationDuration: `${duration}s`,
    animationDelay: `${delay}s`
  }
}

const statusStats = computed(() => {
  const total = stats.value.total || 1
  return [
    { key: 'new', label: 'Новые', count: stats.value.new || 0, percent: Math.round((stats.value.new || 0) / total * 100), color: 'var(--accent)' },
    { key: 'in_progress', label: 'В работе', count: stats.value.in_progress || 0, percent: Math.round((stats.value.in_progress || 0) / total * 100), color: 'var(--warning)' },
    { key: 'closed', label: 'Закрыты', count: stats.value.closed || 0, percent: Math.round((stats.value.closed || 0) / total * 100), color: 'var(--success)' },
    { key: 'rejected', label: 'Отклонены', count: stats.value.rejected || 0, percent: Math.round((stats.value.rejected || 0) / total * 100), color: 'var(--error)' }
  ]
})

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
  loadStats()
  setTimeout(() => badgeVisible.value = true, 300)
  setTimeout(() => titleVisible.value = true, 600)
  setTimeout(() => descVisible.value = true, 900)
  setTimeout(() => actionsVisible.value = true, 1200)
  setTimeout(() => statsVisible.value = true, 1500)
})
</script>

<style scoped>
.hero-section {
  position: relative;
  background: linear-gradient(135deg, #0d0d1a 0%, #1a1a2e 50%, #0f0f20 100%);
  border-radius: var(--radius-xl);
  padding: 48px;
  margin-bottom: 32px;
  overflow: hidden;
  min-height: 500px;
}

.hero-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.particles {
  position: absolute;
  inset: 0;
}

.particle {
  position: absolute;
  background: rgba(231, 76, 60, 0.6);
  border-radius: 50%;
  animation: particleFloat linear infinite;
}

@keyframes particleFloat {
  0% { transform: translateY(0) scale(1); opacity: 0.6; }
  50% { opacity: 1; }
  100% { transform: translateY(-100vh) scale(0); opacity: 0; }
}

.tracks {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 80px;
}

.track {
  position: absolute;
  width: 100%;
  height: 100%;
}

.track-left { left: -50%; }
.track-right { left: 50%; }

.rail {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.3) 50%, transparent 100%);
}

.ties {
  display: flex;
  gap: 30px;
  justify-content: center;
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
}

.tie {
  width: 6px;
  height: 30px;
  background: rgba(255, 255, 255, 0.2);
  animation: tieBlink 1.5s ease-in-out infinite;
}

@keyframes tieBlink {
  0%, 100% { opacity: 0.2; }
  50% { opacity: 0.5; }
}

.train-container {
  position: absolute;
  bottom: 60px;
  left: 50%;
  transform: translateX(-50%);
  animation: trainMove 8s ease-in-out infinite;
}

@keyframes trainMove {
  0%, 100% { transform: translateX(-50%) translateX(-30vw); }
  50% { transform: translateX(-50%) translateX(30vw); }
}

.train {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.train-body {
  width: 120px;
  height: 40px;
  background: linear-gradient(180deg, #e74c3c 0%, #c0392b 100%);
  border-radius: 8px 8px 4px 4px;
  display: flex;
  align-items: center;
  padding: 0 12px;
  gap: 8px;
  position: relative;
}

.train-window {
  width: 20px;
  height: 20px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}

.train-lights {
  position: absolute;
  right: -8px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  gap: 4px;
}

.light-front {
  width: 6px;
  height: 6px;
  background: #fff;
  border-radius: 50%;
  box-shadow: 0 0 10px #fff, 0 0 20px #ff0;
  animation: lightBlink 0.5s ease-in-out infinite;
}

@keyframes lightBlink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.train-wheels {
  display: flex;
  gap: 20px;
  margin-top: 4px;
}

.wheel {
  width: 16px;
  height: 16px;
  background: rgba(255, 255, 255, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  animation: wheelSpin 1s linear infinite;
}

@keyframes wheelSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.smoke {
  position: absolute;
  top: -20px;
  left: 10px;
}

.smoke-puff {
  position: absolute;
  width: 20px;
  height: 20px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  animation: smokeRise 2s ease-out infinite;
}

.smoke-puff:nth-child(1) { left: 0; animation-delay: 0s; }
.smoke-puff:nth-child(2) { left: 15px; animation-delay: 0.5s; }
.smoke-puff:nth-child(3) { left: -10px; animation-delay: 1s; }

@keyframes smokeRise {
  0% { transform: scale(0.5) translateY(0); opacity: 0.5; }
  100% { transform: scale(2) translateY(-40px); opacity: 0; }
}

.glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
}

.glow-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(231, 76, 60, 0.25) 0%, transparent 70%);
  top: -150px;
  right: -100px;
  animation: glowPulse 4s ease-in-out infinite;
}

.glow-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(52, 152, 219, 0.2) 0%, transparent 70%);
  bottom: -100px;
  left: -100px;
  animation: glowPulse 5s ease-in-out infinite 1s;
}

.glow-3 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(155, 89, 182, 0.15) 0%, transparent 70%);
  top: 40%;
  left: 30%;
  animation: glowPulse 6s ease-in-out infinite 2s;
}

@keyframes glowPulse {
  0%, 100% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.2); opacity: 1; }
}

.floating-elements {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.floating-icon {
  position: absolute;
  font-size: 24px;
  color: rgba(255, 255, 255, 0.15);
  animation: floatIcon 6s ease-in-out infinite;
}

.icon-1 { top: 15%; left: 10%; animation-delay: 0s; }
.icon-2 { top: 25%; right: 15%; animation-delay: 1s; }
.icon-3 { top: 60%; left: 8%; animation-delay: 2s; }
.icon-4 { top: 70%; right: 10%; animation-delay: 3s; }
.icon-5 { top: 45%; right: 25%; animation-delay: 4s; }

@keyframes floatIcon {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(10deg); }
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  margin-bottom: 40px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 18px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-full);
  color: rgba(255, 255, 255, 0.85);
  font-size: 14px;
  margin-bottom: 24px;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease;
}

.hero-badge.visible {
  opacity: 1;
  transform: translateY(0);
}

.badge-icon {
  font-size: 18px;
}

.hero-title {
  font-family: var(--font-display);
  font-size: 64px;
  font-weight: 800;
  margin-bottom: 20px;
  line-height: 1.1;
}

.title-service {
  display: block;
  color: #fff;
  opacity: 0;
  transform: translateX(-50px);
  transition: all 0.8s ease 0.2s;
}

.title-service.visible {
  opacity: 1;
  transform: translateX(0);
}

.title-desk {
  display: block;
  background: linear-gradient(135deg, var(--accent) 0%, #ff7675 50%, var(--accent-secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  opacity: 0;
  transform: translateX(50px);
  transition: all 0.8s ease 0.4s;
}

.title-desk.visible {
  opacity: 1;
  transform: translateX(0);
}

.hero-description {
  font-size: 17px;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.7;
  margin-bottom: 32px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease;
}

.hero-description.visible {
  opacity: 1;
  transform: translateY(0);
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease;
}

.hero-actions.visible {
  opacity: 1;
  transform: translateY(0);
}

.btn-hero-primary {
  background: linear-gradient(135deg, var(--accent) 0%, #c0392b 100%);
  color: #fff;
  border: none;
  padding: 16px 32px;
  font-weight: 600;
}

.btn-hero-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(231, 76, 60, 0.45);
}

.btn-hero-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 14px 28px;
  font-weight: 600;
}

.btn-hero-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
}

.hero-stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  position: relative;
  z-index: 1;
}

.stat-card-hero {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-lg);
  backdrop-filter: blur(10px);
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.5s ease;
}

.stat-card-hero.visible {
  opacity: 1;
  transform: translateY(0);
}

.stat-card-hero:nth-child(1) { transition-delay: 0s; }
.stat-card-hero:nth-child(2) { transition-delay: 0.1s; }
.stat-card-hero:nth-child(3) { transition-delay: 0.2s; }
.stat-card-hero:nth-child(4) { transition-delay: 0.3s; }

.stat-icon-hero {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.stat-card-main .stat-icon-hero {
  background: rgba(231, 76, 60, 0.2);
  color: var(--accent);
}

.stat-card-new .stat-icon-hero {
  background: rgba(52, 152, 219, 0.2);
  color: var(--secondary);
}

.stat-card-progress .stat-icon-hero {
  background: rgba(241, 196, 15, 0.2);
  color: var(--warning);
}

.stat-card-done .stat-icon-hero {
  background: rgba(46, 204, 113, 0.2);
  color: var(--success);
}

.stat-content-hero {
  display: flex;
  flex-direction: column;
}

.stat-number-hero {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 700;
  color: #fff;
}

.stat-label-hero {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 24px;
}

.dashboard-main,
.dashboard-sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.quick-actions-section {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.quick-action-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  transition: var(--transition);
}

.quick-action-card:hover {
  border-color: var(--accent);
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.quick-action-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  background: var(--accent-light);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.quick-action-info {
  flex: 1;
}

.quick-action-info h3 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 4px;
}

.quick-action-info p {
  font-size: 13px;
  color: var(--text-secondary);
}

.quick-action-arrow {
  color: var(--text-muted);
  transition: var(--transition);
}

.quick-action-card:hover .quick-action-arrow {
  color: var(--accent);
  transform: translateX(4px);
}

.dashboard-section {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.stats-detailed-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.status-chart h3,
.priority-breakdown h3,
.type-breakdown h3 {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--text-secondary);
}

.status-bar {
  margin-bottom: 12px;
}

.status-bar-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-label {
  flex: 1;
  font-size: 13px;
  color: var(--text-secondary);
}

.status-count {
  font-family: var(--font-display);
  font-weight: 600;
}

.status-bar-track {
  height: 8px;
  background: var(--border);
  border-radius: 4px;
  overflow: hidden;
}

.status-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.priority-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.priority-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
}

.priority-num {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
}

.type-cards {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.type-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
}

.type-icon-wrap {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: var(--accent-light);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
}

.type-details {
  display: flex;
  flex-direction: column;
}

.type-num {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
}

.type-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.specialist-section {
  padding: 0;
  overflow: hidden;
}

.specialist-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-secondary) 100%);
}

.specialist-icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #fff;
  flex-shrink: 0;
  animation: iconPulse 2s ease-in-out infinite;
}

@keyframes iconPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.specialist-content {
  flex: 1;
}

.specialist-content h3 {
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 4px;
}

.specialist-content p {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
}

.btn-white {
  background: #fff;
  color: var(--accent);
  font-weight: 600;
}

.btn-white:hover {
  background: rgba(255, 255, 255, 0.9);
}

.about-section {
  text-align: center;
}

.about-hero {
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 20px;
}

.about-emblem {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  background: linear-gradient(135deg, var(--accent) 0%, #c0392b 100%);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #fff;
}

.about-hero h3 {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 4px;
}

.about-tagline {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.about-version {
  font-size: 12px;
  color: var(--text-muted);
  padding: 4px 10px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-sm);
}

.about-features-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  text-align: left;
}

.feature-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  font-size: 13px;
}

.feature-row i {
  color: var(--success);
}

.help-steps {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.help-step {
  display: flex;
  gap: 12px;
}

.help-num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}

.help-text h4 {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 2px;
}

.help-text p {
  font-size: 12px;
  color: var(--text-muted);
}

@media (max-width: 1200px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .quick-actions-grid {
    grid-template-columns: 1fr;
  }

  .stats-detailed-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 32px 20px;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-stats-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .hero-actions {
    flex-direction: column;
  }
}
</style>