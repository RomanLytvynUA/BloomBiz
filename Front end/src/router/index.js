import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignInView from '../views/SignInView.vue'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: false }
    },
    {
      path: '/signin',
      name: 'signin',
      component: SignInView,
      meta: { requiresAuth: false }
    },
    {
      path: '/dashboard',
      name: 'Кабінет',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/crm',
      name: 'Клієнти',
      component: () => import('../views/CustomersView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/suppliers',
      name: 'Постачальники',
      component: () => import('../views/SuppliersView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/expenses',
      name: 'Витрати',
      component: () => import('../views/ExpensesView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/stock',
      name: 'Склад',
      component: () => import('../views/StockView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/orders',
      name: 'Замовлення',
      component: () => import('../views/OrdersView.vue'),
      meta: { requiresAuth: true }
    },
  ]
})

export default router
