<template>
  <div class="mobile-menu">
    <button 
      class="menu-toggle" 
      @click="isOpen = !isOpen"
      :class="{ 'active': isOpen }"
      aria-label="Меню"
    >
      <span></span>
      <span></span>
      <span></span>
    </button>

    <transition name="fade">
      <div v-show="isOpen" class="overlay" @click="closeMenu"></div>
    </transition>

    <transition name="slide">
      <nav v-if="isOpen" class="menu-panel">
        <div class="menu-header">
          <div class="menu-logo">
            <span class="rzd-icon">🚂</span>
            <span>РЖД Service Desk</span>
          </div>
          <button class="close-btn" @click="closeMenu">&times;</button>
        </div>
        
        <div class="menu-user" v-if="authStore.user">
          <div class="user-avatar">{{ userInitials }}</div>
          <div class="user-details">
            <strong>{{ authStore.user.full_name }}</strong>
            <span>{{ userRoleLabel }}</span>
          </div>
        </div>

        <ul class="menu-list">
          <li>
            <router-link to="/" @click="closeMenu">
              <i class="fas fa-home"></i> Главная
            </router-link>
          </li>
          <li>
            <router-link to="/tickets" @click="closeMenu">
              <i class="fas fa-ticket-alt"></i> Все заявки
            </router-link>
          </li>
          <li>
            <router-link to="/my-tickets" @click="closeMenu">
              <i class="fas fa-list"></i> Мои заявки
            </router-link>
          </li>
          <li>
            <router-link to="/tickets/new" @click="closeMenu">
              <i class="fas fa-plus-circle"></i> Новая заявка
            </router-link>
          </li>
          <li class="divider"></li>
          <li>
            <router-link to="/profile" @click="closeMenu">
              <i class="fas fa-user"></i> Профиль
            </router-link>
          </li>
          <li v-if="authStore.isAdmin">
            <router-link to="/admin" @click="closeMenu">
              <i class="fas fa-cog"></i> Админ-панель
            </router-link>
          </li>
        </ul>

        <div class="menu-footer">
          <button class="logout-btn" @click="handleLogout">
            <i class="fas fa-sign-out-alt"></i> Выйти
          </button>
        </div>
      </nav>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const isOpen = ref(false)

const userInitials = computed(() => {
  if (!authStore.user?.full_name) return '?'
  return authStore.user.full_name.split(' ').map(n => n[0]).join('').slice(0, 2)
})

const userRoleLabel = computed(() => {
  const roles = { employee: 'Сотрудник', specialist: 'Специалист', admin: 'Администратор' }
  return roles[authStore.user?.role] || 'Сотрудник'
})

const closeMenu = () => {
  isOpen.value = false
}

const handleLogout = async () => {
  closeMenu()
  await authStore.logout()
  router.push('/login')
}

const handleEscape = (e) => {
  if (e.key === 'Escape') closeMenu()
}

onMounted(() => document.addEventListener('keydown', handleEscape))
onUnmounted(() => document.removeEventListener('keydown', handleEscape))
</script>

<style scoped>
.mobile-menu {
  display: none;
}

.menu-toggle {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;
  width: 44px;
  height: 44px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 10px;
}

.menu-toggle span {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--text-primary);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.menu-toggle.active span:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}

.menu-toggle.active span:nth-child(2) {
  opacity: 0;
}

.menu-toggle.active span:nth-child(3) {
  transform: rotate(-45deg) translate(5px, -5px);
}

.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 998;
}

.menu-panel {
  position: fixed;
  top: 0;
  left: 0;
  width: 85vw;
  max-width: 320px;
  height: 100vh;
  background: var(--bg-secondary);
  z-index: 999;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 12px rgba(0, 0, 0, 0.15);
}

.menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, var(--accent) 0%, #c0392b 100%);
  color: white;
}

.menu-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.rzd-icon {
  font-size: 20px;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 28px;
  cursor: pointer;
  padding: 0 4px;
  line-height: 1;
}

.menu-user {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}

.user-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent) 0%, #c0392b 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-details strong {
  font-size: 14px;
}

.user-details span {
  font-size: 12px;
  color: var(--text-muted);
}

.menu-list {
  flex: 1;
  list-style: none;
  padding: 12px 0;
  margin: 0;
  overflow-y: auto;
}

.menu-list li {
  border-bottom: 1px solid var(--border);
}

.menu-list a {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 20px;
  text-decoration: none;
  color: var(--text-primary);
  font-size: 15px;
}

.menu-list a:hover,
.menu-list a.router-link-active {
  background: var(--bg-tertiary);
  color: var(--accent);
}

.menu-list a i {
  width: 20px;
  text-align: center;
}

.menu-list .divider {
  height: 1px;
  background: var(--border);
  margin: 8px 0;
}

.menu-footer {
  padding: 16px 20px;
  border-top: 1px solid var(--border);
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 12px 16px;
  background: none;
  border: none;
  color: var(--error);
  font-size: 15px;
  cursor: pointer;
  text-align: left;
}

.logout-btn:hover {
  background: var(--error-light);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}

@media (min-width: 1024px) {
  .mobile-menu {
    display: none;
  }
}
</style>