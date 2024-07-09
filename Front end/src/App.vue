<script setup>
import { onMounted, watch } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import Navbar from './components/Navbar.vue'
import { useSuppliersStore } from '@/stores/suppliers'
import { useExpensesStore } from '@/stores/expenses'
import { useGoodsStore } from '@/stores/goods'
import { useOrdersStore } from '@/stores/orders'
import { useSettingsStore } from '@/stores/settings'
import { useCustomersStore } from './stores/customers'
import { useAuthStore } from './stores/auth'


onMounted(() => {
  if (useAuthStore().isAuthenticated) {
    fetchAllData();
  }
});

function fetchAllData() {
  useSuppliersStore().fetchSuppliers();
  useExpensesStore().fetchExpenses();
  useGoodsStore().fetchGoods();
  useOrdersStore().fetchOrders();
  useSettingsStore().fetchSettings();
  useCustomersStore().fetchCustomers();

}

const router = useRouter();
// function redirectBasedOnAuth(authenticated, route) {
//   if (authenticated && route.name === 'signin') {
//     router.push('/dashboard')
//     return true
//   } else if (!authenticated && route.meta.requiresAuth) {
//     router.push('/signin')
//     return true
//   }
//   return false
// }

// router.beforeEach((to, from, next) => {
//   if (!redirectBasedOnAuth(useAuthStore().isAuthenticated, to)) {
//     next();
//   }
// });
watch(() => useAuthStore().isAuthenticated, (newVal, oldVal) => {
  if (!newVal) {
    router.push('/signin')
  } else {
    router.push('/dashboard')
    fetchAllData();
  }
})
</script>

<template>
  <Navbar />
  <RouterView />
</template>
