import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/dashboard',
      name: 'Кабінет',
      component: () => import('../views/DashboardView.vue')
    },
    {
      path: '/crm',
      name: 'Клієнти',
      component: () => import('../views/CustomersView.vue')
    },
    {
      path: '/suppliers',
      name: 'Постачальники',
      component: () => import('../views/SuppliersView.vue')
    },
    {
      path: '/expenses',
      name: 'Витрати',
      component: () => import('../views/ExpensesView.vue')
    },
    {
      path: '/stock',
      name: 'Склад',
      component: () => import('../views/StockView.vue')
    },
    {
      path: '/orders',
      name: 'Замовлення',
      component: () => import('../views/OrdersView.vue')
    },
  ]
})

export default router
