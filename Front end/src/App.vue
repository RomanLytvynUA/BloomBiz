<script setup>
import { onMounted, watch } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import { useSuppliersStore } from '@/stores/suppliers'
import { useExpensesStore } from '@/stores/expenses'
import { useGoodsStore } from '@/stores/goods'
import { useOrdersStore } from '@/stores/orders'
import { useSettingsStore } from '@/stores/settings'
import { useCustomersStore } from './stores/customers'
import { useAuthStore } from './stores/auth'

import Navbar from './components/Navbar.vue'

import { useI18n } from 'vue-i18n';
const { locale } = useI18n({ useScope: 'global' })


onMounted(() => {
  locale.value = localStorage.getItem('lang') || locale.value;
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
