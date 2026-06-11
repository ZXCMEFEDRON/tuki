import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/userStore'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/LoginView.vue') },
  { path: '/', redirect: '/groups' },
  { path: '/groups', name: 'Groups', component: () => import('../views/GroupsView.vue'), meta: { requiresAuth: true } },
  { path: '/honey', name: 'Honey', component: () => import('../views/HoneyView.vue'), meta: { requiresAuth: true } },
  { path: '/stock', name: 'Stock', component: () => import('../views/StockView.vue'), meta: { requiresAuth: true } },
  { path: '/orders', name: 'Orders', component: () => import('../views/OrdersView.vue'), meta: { requiresAuth: true } },
  { path: '/feedback', name: 'Feedback', component: () => import('../views/FeedbackView.vue'), meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  if (userStore.user === null && !userStore.loading) {
    await userStore.fetchUser()
  }

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && userStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router