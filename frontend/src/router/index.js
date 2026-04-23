import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

let authChecked = false

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/tickets',
    name: 'Tickets',
    component: () => import('../views/Tickets.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/tickets/new',
    name: 'NewTicket',
    component: () => import('../views/TicketForm.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/tickets/:id',
    name: 'TicketDetail',
    component: () => import('../views/TicketDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/my-tickets',
    name: 'MyTickets',
    component: () => import('../views/MyTickets.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresGuest && authStore.user) {
    return next('/')
  }
  
  if (to.meta.requiresGuest) {
    return next()
  }
  
  if (to.path === '/login') {
    return next()
  }

  if (!authStore.user && !authChecked) {
    try {
      await authStore.checkAuth()
      authChecked = true
    } catch (e) {
      authChecked = true
    }
  }

  if (to.meta.requiresAuth && !authStore.user) {
    return next('/login')
  }

  if (to.meta.requiresAdmin && authStore.user?.role !== 'admin') {
    return next('/')
  }

  next()
})

export default router