<template>
  <header class="header">
    <div class="header-inner">
      <router-link to="/" class="logo">
        <span>Р</span><span>Ж</span><span>Д</span>
      </router-link>

      <nav class="nav-desktop">
        <router-link to="/" class="nav-link" :class="{ active: isActive('/') }">Главная</router-link>
        <router-link to="/tickets" class="nav-link" :class="{ active: isActive('/tickets') }">Все заявки</router-link>
        <router-link to="/my-tickets" class="nav-link" :class="{ active: isActive('/my-tickets') }">Мои заявки</router-link>
      </nav>

      <div class="header-right">
        <button class="hamburger" @click="toggleMobile" :class="{ active: menuOpen }">
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
        </button>
        
        <router-link to="/tickets/new" class="btn-new-ticket">
          <i class="fas fa-plus"></i>
        </router-link>

        <div class="user-area">
          <button class="user-avatar" @click="toggleMenu">
            {{ userInitials }}
          </button>
        </div>
      </div>
    </div>

    <transition name="fade">
      <div v-if="showMenu" class="dropdown-overlay" @click="closeMenu"></div>
    </transition>

    <div v-if="showMenu" class="dropdown-menu">
      <div class="dropdown-header">
        <div class="dropdown-user-name">{{ authStore.user?.full_name }}</div>
        <div class="dropdown-user-role">{{ userRoles[authStore.user?.role] }}</div>
      </div>
      <router-link to="/profile" class="dropdown-item" @click="closeMenu">
        <i class="fas fa-user"></i>
        Профиль
      </router-link>
      <router-link v-if="authStore.isAdmin" to="/admin" class="dropdown-item" @click="closeMenu">
        <i class="fas fa-cog"></i>
        Админ-панель
      </router-link>
      <button class="dropdown-item dropdown-item-danger" @click="handleLogout">
        <i class="fas fa-sign-out-alt"></i>
        Выйти
      </button>
    </div>

    <transition name="fade">
      <div v-if="menuOpen" class="mobile-nav-overlay" @click="closeMenu"></div>
    </transition>

    <transition name="menu-slide">
      <div v-if="menuOpen" class="mobile-nav-panel">
        <div class="mobile-nav-header">
          <div class="mobile-user-block">
            <div class="mobile-user-avatar">{{ userInitials }}</div>
            <div class="mobile-user-details">
              <div class="mobile-user-name">{{ authStore.user?.full_name }}</div>
              <div class="mobile-user-role">{{ userRoles[authStore.user?.role] }}</div>
            </div>
          </div>
        </div>

        <div class="mobile-nav-links">
          <router-link to="/" class="mobile-nav-link" @click="closeMenu">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
            <span>Главная</span>
          </router-link>
          <router-link to="/tickets" class="mobile-nav-link" @click="closeMenu">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path></svg>
            <span>Все заявки</span>
          </router-link>
          <router-link to="/my-tickets" class="mobile-nav-link" @click="closeMenu">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
            <span>Мои заявки</span>
          </router-link>
          <router-link to="/tickets/new" class="mobile-nav-link" @click="closeMenu">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
            <span>Новая заявка</span>
          </router-link>
        </div>

        <div class="mobile-nav-divider"></div>

        <div class="mobile-nav-links">
          <router-link to="/profile" class="mobile-nav-link" @click="closeMenu">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
            <span>Профиль</span>
          </router-link>
          <router-link v-if="authStore.isAdmin" to="/admin" class="mobile-nav-link" @click="closeMenu">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
            <span>Админ-панель</span>
          </router-link>
          <button class="mobile-nav-link mobile-nav-link--logout" @click="handleLogout">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
            <span>Выйти</span>
          </button>
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const menuOpen = ref(false)
const showMenu = ref(false)

const userInitials = computed(() => {
  if (!authStore.user?.full_name) return '?'
  return authStore.user.full_name.split(' ').map(n => n[0]).join('').slice(0, 2)
})

const userRoles = {
  employee: 'Сотрудник',
  specialist: 'Специалист',
  admin: 'Администратор'
}

const isActive = (path) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

const toggleMenu = () => {
  showMenu.value = !showMenu.value
}

const closeMenu = () => {
  showMenu.value = false
  menuOpen.value = false
  document.body.style.overflow = ''
}

const toggleMobile = () => {
  menuOpen.value = !menuOpen.value
  if (menuOpen.value) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
}

const closeMobileMenu = () => {
  menuOpen.value = false
  document.body.style.overflow = ''
}

const handleLogout = async () => {
  menuOpen.value = false
  showMenu.value = false
  document.body.style.overflow = ''
  await authStore.logout()
  router.push('/login')
}

const handleResize = () => {
  if (window.innerWidth >= 1024) {
    menuOpen.value = false
    showMenu.value = false
    document.body.style.overflow = ''
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  document.body.style.overflow = ''
})
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 200;
  background: #fff;
  border-bottom: 1px solid var(--border);
  height: 60px;
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 16px;
  max-width: 1400px;
  margin: 0 auto;
}

.logo {
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: 20px;
  font-weight: 700;
}

.logo span:first-child {
  color: var(--accent);
}

.nav-desktop {
  display: none;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.hamburger {
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
  padding: 0;
  border-radius: 8px;
}

@media (min-width: 1024px) {
  .hamburger {
    display: none;
  }
}

.hamburger-line {
  width: 22px;
  height: 2px;
  background: var(--text-primary);
  border-radius: 2px;
  transition: all 0.25s ease;
}

.hamburger.active .hamburger-line:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}

.hamburger.active .hamburger-line:nth-child(2) {
  opacity: 0;
}

.hamburger.active .hamburger-line:nth-child(3) {
  transform: rotate(-45deg) translate(5px, -5px);
}

.btn-new-ticket {
  display: none;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: var(--accent);
  color: #fff;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent) 0%, #c0392b 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

.dropdown-overlay {
  position: fixed;
  inset: 0;
  z-index: 50;
}

.user-area {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 200px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  z-index: 100;
  overflow: hidden;
}

.dropdown-header {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-tertiary);
}

.dropdown-user-name {
  font-weight: 600;
  font-size: 14px;
}

.dropdown-user-role {
  font-size: 12px;
  color: var(--text-muted);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  width: 100%;
  font-size: 14px;
  color: var(--text-primary);
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
}

.dropdown-item:hover {
  background: var(--bg-tertiary);
}

.dropdown-item-danger {
  color: var(--error);
}

.mobile-nav-panel {
  position: fixed;
  top: 60px;
  left: 0;
  bottom: 0;
  width: 300px;
  max-width: 85vw;
  background: #fff;
  z-index: 201;
  overflow-y: auto;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
}

.mobile-nav-header {
  padding: 20px;
  border-bottom: 1px solid var(--border);
}

.mobile-user-block {
  display: flex;
  align-items: center;
  gap: 14px;
}

.mobile-user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent) 0%, #c0392b 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
}

.mobile-user-details {
  display: flex;
  flex-direction: column;
}

.mobile-user-name {
  font-weight: 600;
  font-size: 15px;
}

.mobile-user-role {
  font-size: 13px;
  color: var(--text-muted);
}

.mobile-nav-links {
  padding: 12px;
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 500;
  color: var(--text-primary);
  text-decoration: none;
  transition: all 0.2s;
  background: none;
  border: none;
  width: 100%;
  cursor: pointer;
}

.mobile-nav-link:hover {
  background: var(--bg-tertiary);
}

.mobile-nav-link svg {
  flex-shrink: 0;
}

.mobile-nav-divider {
  height: 1px;
  background: var(--border);
  margin: 4px 20px;
}

.mobile-nav-link--logout {
  color: var(--error);
}

.mobile-nav-overlay {
  position: fixed;
  top: 60px;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 199;
}

.menu-slide-enter-active,
.menu-slide-leave-active {
  transition: transform 0.3s ease;
}

.menu-slide-enter-from,
.menu-slide-leave-to {
  transform: translateX(-100%);
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (min-width: 1024px) {
  .header {
    height: 64px;
  }

  .nav-desktop {
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .nav-link {
    padding: 10px 16px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 500;
    color: var(--text-secondary);
    text-decoration: none;
    transition: all 0.2s;
  }

  .nav-link:hover {
    color: var(--text-primary);
    background: var(--bg-tertiary);
  }

  .nav-link.active {
    color: var(--accent);
    background: rgba(231, 76, 60, 0.1);
  }

  .btn-new-ticket {
    display: flex;
  }

  .header-right {
    gap: 12px;
  }
}

@media (min-width: 1200px) {
  .header-inner {
    padding: 0 24px;
  }
}
</style>